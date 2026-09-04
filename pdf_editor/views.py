import uuid
import json
import base64

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.conf import settings as django_settings
import os
import subprocess
import tempfile
from pdf2docx import Converter

import fitz  # PyMuPDF
from weasyprint import HTML

from core.models import SiteSettings
from core.ai_helper import ask_ai
from .models import PDFProject, PDFSourceFile

RENDER_SCALE = 2.0  # used consistently for editor background + export background


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def project_list_view(request):
    projects = PDFProject.objects.select_related('created_by').all()
    context = _base_context(request, 'pdf')
    context['projects'] = projects
    return render(request, 'pdf_editor/project_list.html', context)


@login_required
def project_create_view(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')

        if not uploaded_files:
            messages.error(request, 'Please select at least one PDF file.')
            return redirect('pdf_editor:project_create')

        project = PDFProject.objects.create(created_by=request.user)
        pages = []

        for f in uploaded_files:
            source = PDFSourceFile.objects.create(
                project=project, file=f, original_name=f.name
            )
            doc = fitz.open(source.file.path)
            for page_number in range(len(doc)):
                pages.append({
                    'id': str(uuid.uuid4()),
                    'source_file_id': source.id,
                    'page_number': page_number,
                    'rotation': 0,
                    'elements': [],
                })
            doc.close()

        project.pages = pages
        project.save()

        messages.success(request, f'{len(uploaded_files)} file(s) uploaded, {len(pages)} page(s) loaded.')
        return redirect('pdf_editor:project_edit', pk=project.pk)

    context = _base_context(request, 'pdf')
    return render(request, 'pdf_editor/upload.html', context)


@login_required
def project_edit_view(request, pk):
    project = get_object_or_404(PDFProject, pk=pk)
    context = _base_context(request, 'pdf')
    context['project'] = project
    return render(request, 'pdf_editor/edit.html', context)


@login_required
def page_thumbnail_view(request, source_id, page_number):
    source = get_object_or_404(PDFSourceFile, pk=source_id)
    rotation = int(request.GET.get('rotation', 0))
    scale = float(request.GET.get('scale', 1.2))

    doc = fitz.open(source.file.path)
    page = doc[page_number]
    page.set_rotation(rotation)

    pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    png_bytes = pixmap.tobytes('png')
    doc.close()

    return HttpResponse(png_bytes, content_type='image/png')


@login_required
@require_POST
def project_add_files_view(request, pk):
    project = get_object_or_404(PDFProject, pk=pk)
    uploaded_files = request.FILES.getlist('files')

    if not uploaded_files:
        messages.error(request, 'Please select at least one PDF file.')
        return redirect('pdf_editor:project_edit', pk=project.pk)

    pages = list(project.pages)

    for f in uploaded_files:
        source = PDFSourceFile.objects.create(
            project=project, file=f, original_name=f.name
        )
        doc = fitz.open(source.file.path)
        for page_number in range(len(doc)):
            pages.append({
                'id': str(uuid.uuid4()),
                'source_file_id': source.id,
                'page_number': page_number,
                'rotation': 0,
                'elements': [],
            })
        doc.close()

    project.pages = pages
    project.save()

    messages.success(request, f'{len(uploaded_files)} more file(s) merged in.')
    return redirect('pdf_editor:project_edit', pk=project.pk)


@login_required
@require_POST
def project_save_state_view(request, pk):
    project = get_object_or_404(PDFProject, pk=pk)

    try:
        new_pages = json.loads(request.POST.get('pages_json', '[]'))
        project.pages = new_pages
        project.save()
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)


def _find_page_entry(project, page_id):
    for p in project.pages:
        if p['id'] == page_id:
            return p
    return None


@login_required
def page_editor_view(request, pk, page_id):
    """
    Full-screen editor for ONE specific page — lets the user add
    text boxes, images, and cover boxes on top of that page,
    exactly like the Document Editor, plus AI assist.
    """
    project = get_object_or_404(PDFProject, pk=pk)
    page_entry = _find_page_entry(project, page_id)

    if page_entry is None:
        messages.error(request, 'Page not found.')
        return redirect('pdf_editor:project_edit', pk=project.pk)

    if request.method == 'POST':
        elements_json = request.POST.get('elements_json', '[]')
        try:
            page_entry['elements'] = json.loads(elements_json)
            project.save()
            messages.success(request, 'Page changes saved.')
        except json.JSONDecodeError:
            messages.error(request, 'Could not save changes — invalid data.')
        return redirect('pdf_editor:page_editor', pk=project.pk, page_id=page_id)

    source = PDFSourceFile.objects.get(pk=page_entry['source_file_id'])
    doc = fitz.open(source.file.path)
    page = doc[page_entry['page_number']]
    page.set_rotation(page_entry.get('rotation', 0))
    pixel_width = int(page.rect.width * RENDER_SCALE)
    pixel_height = int(page.rect.height * RENDER_SCALE)
    doc.close()

    context = _base_context(request, 'pdf')
    context['project'] = project
    context['page_entry'] = page_entry
    context['image_width'] = pixel_width
    context['image_height'] = pixel_height
    context['elements_json'] = json.dumps(page_entry.get('elements', []))
    return render(request, 'pdf_editor/page_editor.html', context)


@login_required
def page_element_image_upload_view(request, pk):
    """AJAX endpoint: uploads an image to place onto a PDF page."""
    project = get_object_or_404(PDFProject, pk=pk)

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        path = default_storage.save(
            f'pdf_editor/elements/{project.pk}/{uploaded_file.name}',
            uploaded_file
        )
        url = default_storage.url(path)
        return JsonResponse({'success': True, 'url': url})

    return JsonResponse({'success': False, 'error': 'No image provided.'}, status=400)


@login_required
@require_POST
def pdf_ai_assist_view(request, pk):
    """AJAX endpoint: same free Gemini AI assist, reused for PDF Editor."""
    get_object_or_404(PDFProject, pk=pk)
    instruction = request.POST.get('instruction', '').strip()
    context_text = request.POST.get('context_text', '').strip()

    if not instruction:
        return JsonResponse({'success': False, 'error': 'Please enter an instruction.'}, status=400)

    try:
        result_text = ask_ai(instruction, context_text)
        return JsonResponse({'success': True, 'result': result_text})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def project_export_view(request, pk):
    """
    Builds the final PDF. Pages with NO added elements are inserted
    directly (fast, preserves original vector quality). Pages WITH
    elements are rendered as: background image of that page + the
    text/image/cover elements on top (using WeasyPrint + Noto Sans
    Bengali, same reliable method as Document Editor), then that
    single rendered page is inserted instead — so Bangla text always
    shapes correctly.
    """
    project = get_object_or_404(PDFProject, pk=pk)

    if not project.pages:
        messages.error(request, 'This project has no pages to export.')
        return redirect('pdf_editor:project_edit', pk=project.pk)

    output_doc = fitz.open()
    source_docs = {}

    for page_entry in project.pages:
        source_id = page_entry['source_file_id']

        if source_id not in source_docs:
            source_file = PDFSourceFile.objects.get(pk=source_id)
            source_docs[source_id] = fitz.open(source_file.file.path)

        source_doc = source_docs[source_id]
        elements = page_entry.get('elements', [])

        if not elements:
            # No edits on this page — insert it directly, unchanged.
            output_doc.insert_pdf(
                source_doc,
                from_page=page_entry['page_number'],
                to_page=page_entry['page_number']
            )
            new_page = output_doc[-1]
            new_page.set_rotation(page_entry.get('rotation', 0))
        else:
            # This page has edits — rasterize + overlay via WeasyPrint.
            page = source_doc[page_entry['page_number']]
            page.set_rotation(page_entry.get('rotation', 0))

            point_width = page.rect.width
            point_height = page.rect.height

            pixmap = page.get_pixmap(matrix=fitz.Matrix(RENDER_SCALE, RENDER_SCALE))
            png_bytes = pixmap.tobytes('png')
            image_base64 = base64.b64encode(png_bytes).decode('utf-8')
            image_data_uri = f"data:image/png;base64,{image_base64}"

            elements_pt = []
            for el in elements:
                elements_pt.append({
                    **el,
                    'left': el['left'] / RENDER_SCALE,
                    'top': el['top'] / RENDER_SCALE,
                    'width': el['width'] / RENDER_SCALE,
                    'height': el['height'] / RENDER_SCALE,
                    'font_size': el.get('font_size', 16) / RENDER_SCALE if el.get('type') == 'text' else None,
                })

            html_string = render_to_string('pdf_editor/page_export_template.html', {
                'image_data_uri': image_data_uri,
                'elements': elements_pt,
                'page_width': point_width,
                'page_height': point_height,
                'font_path': django_settings.BASE_DIR / 'static' / 'fonts' / 'NotoSansBengali-Regular.ttf',
            })

            rendered_pdf_bytes = HTML(
                string=html_string,
                base_url=request.build_absolute_uri('/')
            ).write_pdf()
            rendered_doc = fitz.open(stream=rendered_pdf_bytes, filetype='pdf')
            output_doc.insert_pdf(rendered_doc)
            rendered_doc.close()

    output_bytes = output_doc.tobytes()
    output_doc.close()
    for doc in source_docs.values():
        doc.close()

    filename = f'edited_pdf_{project.pk}.pdf'
    project.exported_file.save(filename, ContentFile(output_bytes), save=True)

    messages.success(request, f'PDF exported successfully with {len(project.pages)} page(s).')
    return redirect('pdf_editor:project_edit', pk=project.pk)


@login_required
def project_convert_to_word_view(request, pk):
    """
    Converts the project's CURRENT exported PDF into an editable
    .docx file for download. If no export exists yet, exports one
    first automatically. The user downloads this, edits it in
    Microsoft Word or LibreOffice Writer (or any Word-compatible
    app), then can upload the edited version to convert it back.
    """
    project = get_object_or_404(PDFProject, pk=pk)

    if not project.exported_file:
        return project_export_view(request, pk)

    pdf_path = project.exported_file.path

    with tempfile.TemporaryDirectory() as tmp_dir:
        docx_path = os.path.join(tmp_dir, f'project_{project.pk}.docx')

        try:
            converter = Converter(pdf_path)
            converter.convert(docx_path)
            converter.close()
        except Exception as e:
            messages.error(request, f'Could not convert to Word: {e}')
            return redirect('pdf_editor:project_edit', pk=project.pk)

        with open(docx_path, 'rb') as f:
            docx_bytes = f.read()

    response = HttpResponse(
        docx_bytes,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="project_{project.pk}.docx"'
    return response


@login_required
def project_upload_word_view(request, pk):
    """
    Accepts an edited .docx file and converts it back into a PDF
    using LibreOffice (free, runs locally, no cloud service needed).
    The result REPLACES this project's exported_file — the original
    source PDFs used to build the project remain untouched, so the
    page-editing workflow is still available afterward if needed.
    """
    project = get_object_or_404(PDFProject, pk=pk)

    if request.method != 'POST' or not request.FILES.get('docx_file'):
        messages.error(request, 'Please select a .docx file to upload.')
        return redirect('pdf_editor:project_edit', pk=project.pk)

    uploaded_docx = request.FILES['docx_file']

    with tempfile.TemporaryDirectory() as tmp_dir:
        docx_path = os.path.join(tmp_dir, 'uploaded.docx')
        with open(docx_path, 'wb') as f:
            for chunk in uploaded_docx.chunks():
                f.write(chunk)

        try:
            result = subprocess.run(
                [
                    django_settings.LIBREOFFICE_PATH,
                    '--headless', '--convert-to', 'pdf',
                    '--outdir', tmp_dir, docx_path
                ],
                capture_output=True, text=True, timeout=120
            )
        except FileNotFoundError:
            messages.error(request, 'LibreOffice was not found. Please check LIBREOFFICE_PATH in your .env file.')
            return redirect('pdf_editor:project_edit', pk=project.pk)
        except subprocess.TimeoutExpired:
            messages.error(request, 'Conversion took too long and timed out. Please try again.')
            return redirect('pdf_editor:project_edit', pk=project.pk)

        converted_pdf_path = os.path.join(tmp_dir, 'uploaded.pdf')

        if not os.path.exists(converted_pdf_path):
            messages.error(request, f'Conversion failed: {result.stderr}')
            return redirect('pdf_editor:project_edit', pk=project.pk)

        with open(converted_pdf_path, 'rb') as f:
            pdf_bytes = f.read()

    filename = f'edited_from_word_{project.pk}.pdf'
    project.exported_file.save(filename, ContentFile(pdf_bytes), save=True)

    messages.success(request, 'Word document converted back to PDF successfully.')
    return redirect('pdf_editor:project_edit', pk=project.pk)







