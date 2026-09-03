import uuid
from io import BytesIO

from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST

import fitz  # PyMuPDF

from core.models import SiteSettings
from .models import PDFProject, PDFSourceFile


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
    """
    Step 1: Upload one or more PDF files. Every page from every
    uploaded file becomes one entry in the new project's page list,
    in upload order — this is the Merge starting point.
    """
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
    """
    Step 2: Shows every page as a thumbnail, in order. The user can
    drag to reorder, rotate, or delete pages, and add more files
    (to merge them in) — all directly from this page.
    """
    project = get_object_or_404(PDFProject, pk=pk)
    context = _base_context(request, 'pdf')
    context['project'] = project
    return render(request, 'pdf_editor/edit.html', context)


@login_required
def page_thumbnail_view(request, source_id, page_number):
    """
    Renders a single PDF page as a PNG image on the fly, so the
    editor can show thumbnails without pre-generating/storing them.
    """
    source = get_object_or_404(PDFSourceFile, pk=source_id)
    rotation = int(request.GET.get('rotation', 0))

    doc = fitz.open(source.file.path)
    page = doc[page_number]
    page.set_rotation(rotation)

    pixmap = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
    png_bytes = pixmap.tobytes('png')
    doc.close()

    return HttpResponse(png_bytes, content_type='image/png')


@login_required
@require_POST
def project_add_files_view(request, pk):
    """
    Adds more uploaded PDFs' pages to the END of an existing
    project's page list — used to merge additional files in later.
    """
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
            })
        doc.close()

    project.pages = pages
    project.save()

    messages.success(request, f'{len(uploaded_files)} more file(s) merged in.')
    return redirect('pdf_editor:project_edit', pk=project.pk)


@login_required
@require_POST
def project_save_state_view(request, pk):
    """
    AJAX endpoint: saves the current page order, rotations, and
    deletions (deleted pages are simply absent from the list)
    whenever the user reorders/rotates/deletes in the editor.
    """
    import json
    project = get_object_or_404(PDFProject, pk=pk)

    try:
        new_pages = json.loads(request.POST.get('pages_json', '[]'))
        project.pages = new_pages
        project.save()
        return JsonResponse({'success': True})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)


@login_required
def project_export_view(request, pk):
    """
    Builds the FINAL PDF from the current page list — in the
    current order, with each page's rotation applied. This is a
    brand-new file; none of the original uploaded PDFs are touched.
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
        output_doc.insert_pdf(
            source_doc,
            from_page=page_entry['page_number'],
            to_page=page_entry['page_number']
        )

        # Apply the saved rotation to the just-inserted page
        new_page = output_doc[-1]
        new_page.set_rotation(page_entry.get('rotation', 0))

    output_bytes = output_doc.tobytes()
    output_doc.close()
    for doc in source_docs.values():
        doc.close()

    filename = f'edited_pdf_{project.pk}.pdf'
    project.exported_file.save(filename, ContentFile(output_bytes), save=True)

    messages.success(request, f'PDF exported successfully with {len(project.pages)} page(s).')
    return redirect('pdf_editor:project_edit', pk=project.pk)
