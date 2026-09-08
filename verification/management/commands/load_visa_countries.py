from django.core.management.base import BaseCommand
from verification.models import VerificationConfig

PLACEHOLDER = "জীবন"

DEFAULT_VISA_FIELDS = [
    {'name': 'passport_number', 'label': 'Passport Number'},
    {'name': 'visa_or_reference_number', 'label': 'Visa / Application Reference Number'},
]

# ============================================
# VISA COUNTRIES — 89 total.
# Every entry gets TWO website slots (official_url_1, official_url_2),
# both starting as the placeholder "জীবন" until you fill in the
# real links yourself. Edit these in Django Admin (/admin/) —
# Verification Configurations — changing it there updates
# everywhere it's used automatically.
# ============================================
VISA_COUNTRIES = [
    # --- Previously confirmed batch ---
    'Saudi Arabia', 'United Arab Emirates (UAE)', 'Qatar', 'Oman', 'Kuwait',
    'Bahrain', 'Malaysia', 'Singapore', 'Egypt', 'South Korea (EPS Worker Visa)',
    'United Kingdom', 'USA', 'Canada', 'Australia (VEVO)', 'Turkey', 'India',
    'Thailand', 'Sri Lanka', 'Indonesia', 'Maldives', 'Japan', 'Pakistan',
    'Hong Kong', 'Philippines', 'New Zealand', 'Italy (Schengen)',
    'Germany (Schengen)', 'France (Schengen)', 'Sweden (Schengen)',
    'Denmark (Schengen)', 'Austria (Schengen)', 'Netherlands (via Sweden Embassy)',
    'Belgium (via Sweden Embassy)', 'Finland (via Sweden Embassy)',
    'Croatia (Schengen)', 'Hungary (Schengen)', 'Poland (via Sweden Embassy)',
    'Russia', 'Uzbekistan', 'Kazakhstan', 'South Africa', 'Kenya',
    # --- New batch requested ---
    'Brunei', 'China', 'Spain (Schengen)', 'Portugal (Schengen)', 'Greece (Schengen)',
    'Switzerland', 'Norway', 'Ireland', 'Romania (Schengen)', 'Serbia',
    'Bosnia and Herzegovina', 'Cyprus', 'Ukraine', 'Mauritius', 'Seychelles',
    'Tanzania', 'Uganda', 'Nigeria', 'Ghana', 'Jordan', 'Lebanon', 'Iraq',
    'Libya', 'Sudan', 'Algeria', 'Morocco', 'Tunisia', 'Brazil', 'Argentina',
    'Mexico', 'Fiji', 'Papua New Guinea', 'Israel', 'Palestine',
    'Malta (Schengen)', 'Luxembourg (Schengen)', 'Iceland (Schengen)',
    'Czech Republic (Schengen)', 'Slovakia (Schengen)', 'Slovenia (Schengen)',
    'Bulgaria', 'Lithuania (Schengen)', 'Latvia (Schengen)', 'Estonia (Schengen)',
    'Kosovo', 'Albania', 'Myanmar', 'Cambodia',
]

# ============================================
# AIR TICKET PROVIDERS — kept with their real, previously verified
# official websites (these were confirmed working, not affected
# by this reset).
# ============================================
AIR_TICKET_PROVIDERS = [
    {'name': 'Biman Bangladesh Airlines', 'url1': 'https://www.biman-airlines.com/', 'url2': ''},
    {'name': 'US-Bangla Airlines', 'url1': 'https://usbair.com/manage-your-booking', 'url2': ''},
    {'name': 'NOVOAIR', 'url1': 'https://www.flynovoair.com/', 'url2': ''},
    {'name': 'Emirates', 'url1': 'https://www.emirates.com/english/manage-booking/', 'url2': ''},
    {'name': 'Qatar Airways', 'url1': 'https://www.qatarairways.com/en/manage-booking.html', 'url2': ''},
    {'name': 'Etihad Airways', 'url1': 'https://www.etihad.com/en/manage', 'url2': ''},
    {'name': 'Malaysia Airlines', 'url1': 'https://www.malaysiaairlines.com/', 'url2': ''},
    {'name': 'Singapore Airlines', 'url1': 'https://www.singaporeair.com/en_UK/us/plan-travel/yourbooking/', 'url2': ''},
    {'name': 'Thai Airways', 'url1': 'https://www.thaiairways.com/managebooking/detail/', 'url2': ''},
    {'name': 'Air India', 'url1': 'https://www.airindia.com/in/en/manage/booking.html', 'url2': ''},
    {'name': 'IndiGo', 'url1': 'https://www.goindigo.in/', 'url2': ''},
    {'name': 'SriLankan Airlines', 'url1': 'https://www.srilankan.com/', 'url2': ''},
    {'name': 'Cathay Pacific', 'url1': 'https://www.cathaypacific.com/mb/', 'url2': ''},
    {'name': 'Turkish Airlines', 'url1': 'https://www.turkishairlines.com/en-int/flights/manage-booking', 'url2': ''},
    {'name': 'Saudia (Saudi Arabian Airlines)', 'url1': 'https://www.saudia.com/en/manage-booking', 'url2': ''},
    {'name': 'Air Arabia', 'url1': 'https://www.airarabia.com/en/manage-bookings', 'url2': ''},
    {'name': 'flydubai', 'url1': 'https://www.flydubai.com/en/book-and-manage/view-or-change-booking', 'url2': ''},
    {'name': 'Gulf Air', 'url1': 'https://www.gulfair.com/flying-with-us/before-you-travel/manage', 'url2': ''},
    {'name': 'Oman Air', 'url1': 'https://www.omanair.com/', 'url2': ''},
    {'name': 'British Airways', 'url1': 'https://www.britishairways.com/', 'url2': ''},
]


class Command(BaseCommand):
    help = 'Loads/refreshes ALL visa-country and air-ticket-provider verification configurations.'

    def handle(self, *args, **options):
        visa_count = 0
        for country_name in VISA_COUNTRIES:
            obj, created = VerificationConfig.objects.update_or_create(
                country_or_provider=country_name,
                service_type=VerificationConfig.ServiceType.VISA,
                defaults={
                    'required_fields': DEFAULT_VISA_FIELDS,
                    'method': VerificationConfig.Method.WEBSITE,
                    'official_url_1': PLACEHOLDER,
                    'official_url_2': PLACEHOLDER,
                    'instructions': '',
                }
            )
            visa_count += 1
            self.stdout.write(f"{'Created' if created else 'Updated'}: {country_name}")

        air_count = 0
        for provider in AIR_TICKET_PROVIDERS:
            obj, created = VerificationConfig.objects.update_or_create(
                country_or_provider=provider['name'],
                service_type=VerificationConfig.ServiceType.AIR_TICKET,
                defaults={
                    'required_fields': [
                        {'name': 'pnr', 'label': 'PNR / Booking Reference'},
                        {'name': 'last_name', 'label': 'Passenger Last Name'},
                    ],
                    'method': VerificationConfig.Method.WEBSITE,
                    'official_url_1': provider['url1'],
                    'official_url_2': provider['url2'],
                    'instructions': '',
                }
            )
            air_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {visa_count} visa countries and {air_count} air ticket providers loaded/refreshed."
        ))