import json
from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from core.ai_helper import ask_ai, generate_ai_image, check_and_increment_ai_image_quota
from django.core.files.storage import default_storage
import uuid
from django.core.files.storage import default_storage

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
            'color': '#ffffff',
            'covered': False,
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
    Step 2: Shows the uploaded image with editable text boxes,
    plus any added images/cover-boxes, positioned exactly where
    they belong in the original image's coordinate space.
    """
    doc = get_object_or_404(DocumentEdit, pk=pk)
    image = Image.open(doc.original_image.path)

    if request.method == 'POST':
        edited_json = request.POST.get('edited_blocks_json', '[]')
        elements_json = request.POST.get('added_elements_json', '[]')
        try:
            doc.edited_blocks = json.loads(edited_json)
            doc.added_elements = json.loads(elements_json)
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
    context['elements_json'] = json.dumps(doc.added_elements)
    context['ai_image_daily_limit'] = django_settings.AI_IMAGE_DAILY_LIMIT
    return render(request, 'documents/edit.html', context)


@login_required
def element_image_upload_view(request, pk):
    """
    AJAX endpoint used by the editor page: uploads a new image the
    user wants to place onto the document (e.g. a passport photo
    added to a CV), and returns its URL so JavaScript can display it.
    """
    doc = get_object_or_404(DocumentEdit, pk=pk)

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        path = default_storage.save(
            f'documents/elements/{doc.pk}/{uploaded_file.name}',
            uploaded_file
        )
        url = default_storage.url(path)
        return JsonResponse({'success': True, 'url': url})

    return JsonResponse({'success': False, 'error': 'No image provided.'}, status=400)


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
        'elements': doc.added_elements,
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

@login_required
@require_POST
def document_ai_assist_view(request, pk):
    """
    AJAX endpoint: sends the user's instruction (and optionally
    existing text) to Gemini, returns the suggested text as JSON.
    The frontend then lets the user review it and manually insert
    it into any text box — nothing is auto-applied.
    """
    doc = get_object_or_404(DocumentEdit, pk=pk)
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
@require_POST
def document_ai_image_view(request, pk):
    """
    Generates OR edits an AI image (Gemini "Nano Banana"):
    - If the user uploads a reference image, the AI EDITS that image
      according to the description (image-to-image editing).
    - If no reference image is given, the AI generates a brand-new
      image from the description alone (text-to-image).
    Enforces a small daily quota per user since this is not truly
    unlimited/free.
    """
    doc = get_object_or_404(DocumentEdit, pk=pk)
    prompt = request.POST.get('prompt', '').strip()
    reference_image = request.FILES.get('reference_image')

    if not prompt:
        return JsonResponse({'success': False, 'error': 'Please describe what you want.'}, status=400)

    if not check_and_increment_ai_image_quota(request.user):
        return JsonResponse({
            'success': False,
            'error': f'Daily AI image limit ({django_settings.AI_IMAGE_DAILY_LIMIT}) reached. Please try again tomorrow.'
        }, status=429)

    try:
        reference_bytes = reference_image.read() if reference_image else None
        image_bytes = generate_ai_image(prompt, reference_bytes)
        filename = f'documents/ai_images/{doc.pk}/{uuid.uuid4().hex}.png'
        path = default_storage.save(filename, ContentFile(image_bytes))
        url = default_storage.url(path)
        return JsonResponse({'success': True, 'url': url})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)   