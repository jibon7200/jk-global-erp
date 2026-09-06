from django.core.management.base import BaseCommand
from verification.models import VerificationConfig


class Command(BaseCommand):
    help = 'Loads a starter set of VERIFIED visa verification configurations for common destination countries.'

    def handle(self, *args, **options):
        countries = [
            {
                'country_or_provider': 'Saudi Arabia',
                'service_type': VerificationConfig.ServiceType.VISA,
                'required_fields': [
                    {'name': 'visa_or_application_number', 'label': 'Visa / Application Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://visa.mofa.gov.sa/',
                'instructions': 'Verified via MOFA visa portal (visa.mofa.gov.sa). Enjaz has been merged into MOFA.',
            },
            {
                'country_or_provider': 'United Arab Emirates (UAE)',
                'service_type': VerificationConfig.ServiceType.VISA,
                'required_fields': [
                    {'name': 'passport_number', 'label': 'Passport Number'},
                    {'name': 'passport_expiry_date', 'label': 'Passport Expiry Date'},
                    {'name': 'nationality', 'label': 'Nationality'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://smartservices.icp.gov.ae/',
                'instructions': 'ICP Smart Services covers all Emirates except Dubai. For Dubai-issued visas, use GDRFA Dubai instead.',
            },
            {
                'country_or_provider': 'Qatar',
                'service_type': VerificationConfig.ServiceType.VISA,
                'required_fields': [
                    {'name': 'visa_or_qid_number', 'label': 'Visa Number / QID Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://portal.moi.gov.qa/',
                'instructions': 'Ministry of Interior (MOI) e-services portal. Also available via the Metrash2 mobile app.',
            },
        ]

        created_count = 0
        for entry in countries:
            obj, created = VerificationConfig.objects.get_or_create(
                country_or_provider=entry['country_or_provider'],
                service_type=entry['service_type'],
                defaults={
                    'required_fields': entry['required_fields'],
                    'method': entry['method'],
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