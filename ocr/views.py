from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

import pytesseract
from PIL import Image

from core.models import SiteSettings
from .models import PassportScan
from .forms import PassportUploadForm, PassportReviewForm
from .mrz_parser import find_mrz_lines, parse_mrz

pytesseract.pytesseract.tesseract_cmd = django_settings.TESSERACT_CMD_PATH


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def scan_upload_view(request):
    """
    Step 1: Upload a passport image.
    Workflow: Upload -> OCR -> Extract -> Review -> Edit -> Confirm -> Save
    """
    if request.method == 'POST':
        form = PassportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            scan = PassportScan(image=form.cleaned_data['image'], created_by=request.user)
            scan.save()

            try:
                image = Image.open(scan.image.path)
                raw_text = pytesseract.image_to_string(image)
                scan.raw_ocr_text = raw_text

                line1, line2 = find_mrz_lines(raw_text)

                if line1 and line2:
                    extracted = parse_mrz(line1, line2)
                    scan.full_name = extracted['full_name']
                    scan.passport_number = extracted['passport_number']
                    scan.nationality = extracted['nationality']
                    scan.date_of_birth = extracted['date_of_birth']
                    scan.date_of_expiry = extracted['date_of_expiry']
                    scan.sex = extracted['sex']
                    scan.extraction_successful = True
                    messages.success(request, 'MRZ detected and data extracted. Please review before saving.')
                else:
                    scan.extraction_successful = False
                    messages.warning(
                        request,
                        'Could not automatically detect passport MRZ lines. '
                        'Please enter the details manually below.'
                    )

                scan.save()

            except Exception as e:
                # OCR must NEVER crash the app or lose the uploaded file.
                # If OCR fails for any reason, the scan record and image
                # are still saved, and the user can fill fields manually.
                scan.extraction_successful = False
                scan.save()
                messages.error(request, f'OCR processing failed: {e}. You can still enter details manually.')

            return redirect('ocr:scan_review', pk=scan.pk)
    else:
        form = PassportUploadForm()

    context = _base_context(request, 'status')
    context['form'] = form
    return render(request, 'ocr/upload.html', context)


@login_required
def scan_review_view(request, pk):
    """
    Step 2: Review & correct the extracted data, then confirm/save.
    Nothing here is treated as final until the user explicitly
    clicks 'Confirm & Save'.
    """
    scan = get_object_or_404(PassportScan, pk=pk)

    if request.method == 'POST':
        form = PassportReviewForm(request.POST, instance=scan)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.reviewed_and_confirmed = True
            scan.save()
            messages.success(request, 'Passport data confirmed and saved. You can now copy this into the Passport/Visa/Ticket module.')
            return redirect('ocr:scan_list')
    else:
        form = PassportReviewForm(instance=scan)

    context = _base_context(request, 'status')
    context['form'] = form
    context['scan'] = scan
    return render(request, 'ocr/review.html', context)


@login_required
def scan_list_view(request):
    """
    History of all passport scans done so far.
    """
    scans = PassportScan.objects.select_related('created_by').all()
    context = _base_context(request, 'status')
    context['scans'] = scans
    return render(request, 'ocr/scan_list.html', context)
