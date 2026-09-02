import json
from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.files.base import ContentFile

import pytesseract
from PIL import Image
from weasyprint import HTML

from core.models import SiteSettings
from .models import DocumentEdit
from .forms import DocumentUploadForm

pytesseract.pytesseract.tesseract_cmd = django_settings.TESSERACT_CMD_PATH


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


def _extract_text_blocks(image_path):
    """
    Uses Tesseract to detect text LINES (not individual words) along
    with their position on the image, supporting both Bangla and
    English ('ben+eng'). Returns a list of dicts:
        {text, left, top, width, height}
    Grouping by line (not word) keeps the editor usable — editing
    one word at a time would be tedious for real documents.
    """
    image = Image.open(image_path)
    data = pytesseract.image_to_data(
        image, lang='ben+eng', output_type=pytesseract.Output.DICT
    )

    lines = {}
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        text = data['text'][i].strip()
        if not text:
            continue

        key = (data['block_num'][i], data['par_num'][i], data['line_num'][i])
        left, top = data['left'][i], data['top'][i]
        width, height = data['width'][i], data['height'][i]

        if key not in lines:
            lines[key] = {
                'text': text,
                'left': left, 'top': top,
                'right': left + width, 'bottom': top + height,
            }
        else:
            lines[key]['text'] += ' ' + text
            lines[key]['right'] = max(lines[key]['right'], left + width)
            lines[key]['bottom'] = max(lines[key]['bottom'], top + height)

    blocks = []
    for line in lines.values():
        blocks.append({
            'text': line['text'],
            'left': line['left'],
            'top': line['top'],
            'width': line['right'] - line['left'],
            'height': line['bottom'] - line['top'],
        })

    return blocks, image.width, image.height


@login_required
def document_upload_view(request):
    """
    Step 1: Upload an image (JPG/PNG) of a document to edit.
    """
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = DocumentEdit(original_image=form.cleaned_data['image'], created_by=request.user)
            doc.save()

            try:
                blocks, _, _ = _extract_text_blocks(doc.original_image.path)
                doc.detected_blocks = blocks
                doc.edited_blocks = blocks  # starts as a copy; user edits this
                doc.save()
                messages.success(request, f'{len(blocks)} text lines detected. You can now edit them.')
            except Exception as e:
                messages.error(request, f'OCR text detection failed: {e}. You can still add text manually.')

            return redirect('documents:document_edit', pk=doc.pk)
    else:
        form = DocumentUploadForm()

    context = _base_context(request, 'documents')
    context['form'] = form
    return render(request, 'documents/upload.html', context)


@login_required
def document_edit_view(request, pk):
    """
    Step 2: Shows the uploaded image with editable text boxes
    positioned exactly where OCR found each line. The user can
    change any line's text; layout position is preserved.
    """
    doc = get_object_or_404(DocumentEdit, pk=pk)
    image = Image.open(doc.original_image.path)

    if request.method == 'POST':
        edited_json = request.POST.get('edited_blocks_json', '[]')
        try:
            doc.edited_blocks = json.loads(edited_json)
            doc.save()
            messages.success(request, 'Changes saved. You can now export this as a new file.')
        except json.JSONDecodeError:
            messages.error(request, 'Could not save changes — invalid data received.')
        return redirect('documents:document_edit', pk=doc.pk)

    context = _base_context(request, 'documents')
    context['doc'] = doc
    context['image_width'] = image.width
    context['image_height'] = image.height
    context['blocks_json'] = json.dumps(doc.edited_blocks)
    return render(request, 'documents/edit.html', context)


@login_required
def document_export_view(request, pk):
    """
    Step 3: Renders the edited text (using a proper Bangla Unicode
    font via WeasyPrint, so conjuncts/matras render correctly) onto
    an HTML page positioned to match the original layout, then
    converts that to a PDF. The original image is NEVER overwritten —
    this always produces a new exported file.
    """
    doc = get_object_or_404(DocumentEdit, pk=pk)
    image = Image.open(doc.original_image.path)

    html_string = render_to_string('documents/export_template.html', {
        'image_url': request.build_absolute_uri(doc.original_image.url),
        'blocks': doc.edited_blocks,
        'image_width': image.width,
        'image_height': image.height,
        'font_path': django_settings.BASE_DIR / 'static' / 'fonts' / 'NotoSansBengali-Regular.ttf',
    })

    pdf_bytes = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    filename = f'edited_document_{doc.pk}.pdf'
    doc.exported_file.save(filename, ContentFile(pdf_bytes), save=True)

    messages.success(request, 'Document exported successfully as a new PDF file.')
    return redirect('documents:document_edit', pk=doc.pk)


@login_required
def document_list_view(request):
    documents = DocumentEdit.objects.select_related('created_by').all()
    context = _base_context(request, 'documents')
    context['documents'] = documents
    return render(request, 'documents/document_list.html', context)
