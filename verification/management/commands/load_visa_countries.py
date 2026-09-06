from django.core.management.base import BaseCommand
from verification.models import VerificationConfig


class Command(BaseCommand):
    help = 'Loads a starter set of VERIFIED visa verification configurations for key destination countries for Bangladeshi workers/travelers.'

    def handle(self, *args, **options):
        countries = [
            {
                'country_or_provider': 'Saudi Arabia',
                'required_fields': [
                    {'name': 'visa_or_application_number', 'label': 'Visa / Application Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.mofa.gov.sa/',
                'instructions': 'MOFA visa portal. Enjaz (enjazit.com.sa) has been fully merged into MOFA.',
            },
            {
                'country_or_provider': 'United Arab Emirates (UAE)',
                'required_fields': [
                    {'name': 'passport_number', 'label': 'Passport Number'},
                    {'name': 'passport_expiry_date', 'label': 'Passport Expiry Date'},
                    {'name': 'nationality', 'label': 'Nationality'},
                ],
                'official_url': 'https://smartservices.icp.gov.ae/',
                'instructions': 'ICP Smart Services covers all Emirates except Dubai. Dubai-issued visas use GDRFA Dubai instead.',
            },
            {
                'country_or_provider': 'Qatar',
                'required_fields': [
                    {'name': 'visa_or_qid_number', 'label': 'Visa Number / QID Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://portal.moi.gov.qa/',
                'instructions': 'Ministry of Interior (MOI) e-services portal. Also available via the Metrash2 mobile app.',
            },
            {
                'country_or_provider': 'Oman',
                'required_fields': [
                    {'name': 'application_number', 'label': 'Web Application Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://evisa.rop.gov.om/',
                'instructions': 'Royal Oman Police (ROP) eVisa portal.',
            },
            {
                'country_or_provider': 'Kuwait',
                'required_fields': [
                    {'name': 'evisa_reference_number', 'label': 'eVisa Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://evisa.moi.gov.kw/',
                'instructions': 'Kuwait Ministry of Interior (MOI) e-Visa portal.',
            },
            {
                'country_or_provider': 'Bahrain',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.evisa.gov.bh/',
                'instructions': 'Managed by Nationality, Passports and Residence Affairs (NPRA).',
            },
            {
                'country_or_provider': 'Malaysia',
                'required_fields': [
                    {'name': 'passport_number', 'label': 'Passport Number'},
                    {'name': 'sticker_number', 'label': 'Sticker / Approval Number'},
                ],
                'official_url': 'https://malaysiavisa.imi.gov.my/evisa/evisa.jsp',
                'instructions': 'Official MYVISA portal by the Immigration Department of Malaysia. Beware of unofficial third-party sites.',
            },
            {
                'country_or_provider': 'Singapore',
                'required_fields': [
                    {'name': 'passport_number', 'label': 'Passport Number'},
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                ],
                'official_url': 'https://www.ica.gov.sg/',
                'instructions': 'Immigration and Checkpoints Authority (ICA) of Singapore.',
            },
                        {
                'country_or_provider': 'Egypt',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa2egypt.gov.eg/',
                'instructions': 'Official Egypt eVisa portal.',
            },
            {
                'country_or_provider': 'South Korea (EPS Worker Visa)',
                'required_fields': [
                    {'name': 'application_number', 'label': 'Application/Registration Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.eps.go.kr/',
                'instructions': 'Employment Permit System (EPS) portal for foreign worker (E-9) visas.',
            },
            {
                'country_or_provider': 'United Kingdom',
                'required_fields': [
                    {'name': 'visa_reference_number', 'label': 'Visa Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.gov.uk/view-prove-immigration-status',
                'instructions': 'UK Visas and Immigration (UKVI) — view/prove immigration status (eVisa) service.',
            },
            {
                'country_or_provider': 'USA',
                'required_fields': [
                    {'name': 'case_number', 'label': 'Visa Case Number'},
                ],
                'official_url': 'https://ceac.state.gov/CEAC/',
                'instructions': 'U.S. Department of State Consular Electronic Application Center (CEAC).',
            },
            {
                'country_or_provider': 'Canada',
                'required_fields': [
                    {'name': 'uci_or_application_number', 'label': 'UCI / Application Number'},
                    {'name': 'date_of_birth', 'label': 'Date of Birth'},
                ],
                'official_url': 'https://www.canada.ca/en/immigration-refugees-citizenship/services/application/check-status.html',
                'instructions': 'Immigration, Refugees and Citizenship Canada (IRCC) official status checker.',
            },
            {
                'country_or_provider': 'Australia (VEVO)',
                'required_fields': [
                    {'name': 'passport_number', 'label': 'Passport Number'},
                    {'name': 'reference_number', 'label': 'Transaction/Visa Grant Number'},
                ],
                'official_url': 'https://immi.homeaffairs.gov.au/visas/already-have-a-visa/check-visa-details-and-conditions/check-conditions-online',
                'instructions': 'Visa Entitlement Verification Online (VEVO) by Australian Department of Home Affairs.',
            },
        ]

        created_count = 0
        for entry in countries:
            obj, created = VerificationConfig.objects.get_or_create(
                country_or_provider=entry['country_or_provider'],
                service_type=VerificationConfig.ServiceType.VISA,
                defaults={
                    'required_fields': entry['required_fields'],
                    'method': VerificationConfig.Method.WEBSITE,
                    'official_url': entry['official_url'],
                    'instructions': entry['instructions'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {entry['country_or_provider']}"))
            else:
                self.stdout.write(f"Already exists, skipped: {entry['country_or_provider']}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. {created_count} new configuration(s) added."))