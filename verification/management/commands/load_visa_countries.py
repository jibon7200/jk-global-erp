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
                        {
                'country_or_provider': 'Turkey',
                'required_fields': [
                    {'name': 'order_id', 'label': 'Order/Application ID'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.evisa.gov.tr/',
                'instructions': 'Official Turkish e-Visa system; status check at evisa.gov.tr/en/status/.',
            },
            {
                'country_or_provider': 'India',
                'required_fields': [
                    {'name': 'application_id', 'label': 'Application ID'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://indianvisaonline.gov.in/evisa/',
                'instructions': 'Official Indian e-Visa portal (Ministry of Home Affairs).',
            },
            {
                'country_or_provider': 'Thailand',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://thaievisa.go.th/',
                'instructions': 'Royal Thai e-Visa portal.',
            },
            {
                'country_or_provider': 'Sri Lanka',
                'required_fields': [
                    {'name': 'eta_reference_number', 'label': 'ETA Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://eta.gov.lk/',
                'instructions': 'Electronic Travel Authorization (ETA) — Department of Immigration & Emigration.',
            },
            {
                'country_or_provider': 'Indonesia',
                'required_fields': [
                    {'name': 'reference_number', 'label': 'Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://evisa.imigrasi.go.id/',
                'instructions': 'Directorate General of Immigration e-Visa portal.',
            },
            {
                'country_or_provider': 'Maldives',
                'required_fields': [
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://imuga.immigration.gov.mv/traveller',
                'instructions': 'IMUGA Traveller Declaration — mandatory pre-arrival system, free of charge.',
            },
                        {
                'country_or_provider': 'Japan',
                'required_fields': [
                    {'name': 'registered_email', 'label': 'Registered Email (eVisa account)'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.evisa.mofa.go.jp/',
                'instructions': 'JAPAN eVISA — Ministry of Foreign Affairs. Only for eligible nationalities/residencies; check MOFA eligibility list first.',
            },
            {
                'country_or_provider': 'Pakistan',
                'required_fields': [
                    {'name': 'application_tracking_id', 'label': 'Application Tracking ID'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.nadra.gov.pk/',
                'instructions': 'NADRA e-Visa portal, Ministry of Interior, Pakistan.',
            },
            {
                'country_or_provider': 'Hong Kong',
                'required_fields': [
                    {'name': 'reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.immd.gov.hk/eng/e-visa.html',
                'instructions': 'Hong Kong Immigration Department (ImmD) e-Visa arrangement.',
            },
                        {
                'country_or_provider': 'Philippines',
                'required_fields': [
                    {'name': 'control_number', 'label': 'eVisa Control Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://evisa.gov.ph/',
                'instructions': 'Department of Foreign Affairs (DFA) eVisa Verifier.',
            },
            {
                'country_or_provider': 'New Zealand',
                'required_fields': [
                    {'name': 'application_number', 'label': 'Application Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.immigration.govt.nz/',
                'instructions': 'Immigration New Zealand (INZ) — requires an Immigration Online account.',
            },
            {
                'country_or_provider': 'Italy (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/ita/',
                'instructions': 'VFS Global Dhaka — official outsourced visa application/tracking partner for the Italian Embassy.',
            },
            {
                'country_or_provider': 'Germany (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/deu/',
                'instructions': 'VFS Global Dhaka — official outsourced visa application/tracking partner for the German Embassy.',
            },
            {
                'country_or_provider': 'France (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/fra/',
                'instructions': 'VFS Global Dhaka — official outsourced visa application/tracking partner for the French Embassy.',
            },
                        {
                'country_or_provider': 'Sweden (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/swe/',
                'instructions': 'VFS Global Dhaka — Embassy of Sweden also represents Netherlands, Belgium, and Finland for Schengen visas from Bangladesh.',
            },
            {
                'country_or_provider': 'Denmark (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/dnk/',
                'instructions': 'VFS Global Dhaka — official outsourced partner for the Danish Embassy.',
            },
            {
                'country_or_provider': 'Austria (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/aut/',
                'instructions': 'VFS Global Dhaka — official outsourced partner for the Austrian Embassy.',
            },
            {
                'country_or_provider': 'Netherlands (via Sweden Embassy)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/swe/',
                'instructions': 'No separate Dhaka centre — visas processed via Embassy of Sweden representation agreement.',
            },
            {
                'country_or_provider': 'Belgium (via Sweden Embassy)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/swe/',
                'instructions': 'No separate Dhaka centre — visas processed via Embassy of Sweden representation agreement.',
            },
            {
                'country_or_provider': 'Finland (via Sweden Embassy)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/swe/',
                'instructions': 'No separate Dhaka centre — visas processed via Embassy of Sweden representation agreement.',
            },
                        {
                'country_or_provider': 'Croatia (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/hrv/',
                'instructions': 'VFS Global Dhaka — official outsourced partner for the Croatian Embassy.',
            },
            {
                'country_or_provider': 'Hungary (Schengen)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/hun/',
                'instructions': 'VFS Global Dhaka — official outsourced partner for the Hungarian Embassy.',
            },
            {
                'country_or_provider': 'Poland (via Sweden Embassy)',
                'required_fields': [
                    {'name': 'application_reference_number', 'label': 'Application Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://visa.vfsglobal.com/bgd/en/swe/',
                'instructions': 'No separate Dhaka centre — visas processed via Embassy of Sweden representation agreement.',
            },
                        {
                'country_or_provider': 'Russia',
                'required_fields': [
                    {'name': 'application_id', 'label': 'Application ID'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://evisacheck.kdmid.ru/',
                'instructions': 'Consular Department, Ministry of Foreign Affairs of Russia — dedicated e-visa status checker.',
            },
            {
                'country_or_provider': 'Uzbekistan',
                'required_fields': [
                    {'name': 'application_number', 'label': 'Application Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://e-visa.gov.uz/',
                'instructions': 'Official Uzbekistan e-Visa portal.',
            },
            {
                'country_or_provider': 'Kazakhstan',
                'required_fields': [
                    {'name': 'passport_number', 'label': 'Passport Number'},
                    {'name': 'passport_expiry_date', 'label': 'Passport Expiry Date'},
                ],
                'official_url': 'https://www.vmp.gov.kz/',
                'instructions': 'Visa-Migration Portal of the Republic of Kazakhstan.',
            },
            {
                'country_or_provider': 'South Africa',
                'required_fields': [
                    {'name': 'reference_number', 'label': 'Reference Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://ehome.dha.gov.za/epermit/login',
                'instructions': 'Department of Home Affairs (DHA) ePermit portal.',
            },
            {
                'country_or_provider': 'Kenya',
                'required_fields': [
                    {'name': 'eta_application_number', 'label': 'eTA Application Number'},
                    {'name': 'passport_number', 'label': 'Passport Number'},
                ],
                'official_url': 'https://www.etakenya.go.ke/',
                'instructions': 'Electronic Travel Authorization (eTA) official portal.',
            },






            {
                'country_or_provider': 'Biman Bangladesh Airlines',
                'service_type': VerificationConfig.ServiceType.AIR_TICKET,
                'required_fields': [
                    {'name': 'pnr', 'label': 'PNR / Booking Reference'},
                    {'name': 'last_name', 'label': 'Passenger Last Name'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://www.biman-airlines.com/',
                'instructions': 'Use "Manage My Booking" with PNR and last name.',
            },
                        {
                'country_or_provider': 'US-Bangla Airlines',
                'service_type': VerificationConfig.ServiceType.AIR_TICKET,
                'required_fields': [
                    {'name': 'pnr', 'label': 'PNR / Booking Reference'},
                    {'name': 'last_name', 'label': 'Passenger Last Name'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://usbair.com/manage-your-booking',
                'instructions': 'Only works for tickets bought directly via US-Bangla website/app/sales office, not third-party agencies.',
            },
            {
                'country_or_provider': 'NOVOAIR',
                'service_type': VerificationConfig.ServiceType.AIR_TICKET,
                'required_fields': [
                    {'name': 'pnr', 'label': 'PNR / Booking Reference'},
                    {'name': 'last_name', 'label': 'Passenger Last Name'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://www.flynovoair.com/',
                'instructions': 'Domestic Bangladesh airline — use the Manage Booking / Check-in section.',
            },
            {
                'country_or_provider': 'Emirates',
                'service_type': VerificationConfig.ServiceType.AIR_TICKET,
                'required_fields': [
                    {'name': 'booking_reference', 'label': 'Booking Reference'},
                    {'name': 'last_name', 'label': 'Passenger Last Name'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://www.emirates.com/english/manage-booking/',
                'instructions': 'Official Emirates Manage Booking portal.',
            },
            {
                'country_or_provider': 'Qatar Airways',
                'service_type': VerificationConfig.ServiceType.AIR_TICKET,
                'required_fields': [
                    {'name': 'booking_reference', 'label': 'Booking Reference'},
                    {'name': 'last_name', 'label': 'Passenger Last Name'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://www.qatarairways.com/en/manage-booking.html',
                'instructions': 'Official Qatar Airways Manage Booking portal.',
            },
            {
                'country_or_provider': 'Etihad Airways',
                'service_type': VerificationConfig.ServiceType.AIR_TICKET,
                'required_fields': [
                    {'name': 'booking_reference', 'label': 'Booking Reference'},
                    {'name': 'last_name', 'label': 'Passenger Last Name'},
                ],
                'method': VerificationConfig.Method.WEBSITE,
                'official_url': 'https://www.etihad.com/en/manage',
                'instructions': 'Official Etihad Airways Manage Booking portal.',
            },

        ]

        created_count = 0
        for entry in countries:
            service_type = entry.get('service_type', VerificationConfig.ServiceType.VISA)
            method = entry.get('method', VerificationConfig.Method.WEBSITE)

            obj, created = VerificationConfig.objects.get_or_create(
                country_or_provider=entry['country_or_provider'],
                service_type=service_type,
                defaults={
                    'required_fields': entry['required_fields'],
                    'method': method,
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