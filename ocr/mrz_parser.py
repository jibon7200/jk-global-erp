import re


def find_mrz_lines(raw_text):
    """
    Looks through OCR-extracted text for two lines that look like
    a passport MRZ (Machine Readable Zone) — TD3 format, used by
    most passports worldwide. Each MRZ line is 44 characters,
    made mostly of uppercase letters, digits, and '<' filler characters.

    Returns (line1, line2) if found, or (None, None) if not.
    """
    lines = raw_text.replace(' ', '').upper().splitlines()

    # An MRZ line is mostly A-Z, 0-9, and '<' — very few other characters.
    mrz_pattern = re.compile(r'^[A-Z0-9<]{30,44}$')

    candidates = [line.strip() for line in lines if mrz_pattern.match(line.strip())]

    if len(candidates) >= 2:
        return candidates[0], candidates[1]

    return None, None


def parse_mrz(line1, line2):
    """
    Parses the two MRZ lines according to the ICAO 9303 TD3 standard
    (used on passport bio-data pages).

    Line 1: P<COUNTRYCODE<SURNAME<<GIVEN<NAMES<<<<<<<<<<<<<<<<<<<<
    Line 2: PASSPORTNO<CHECKDIGIT NATIONALITY YYMMDD(DOB) CHECKDIGIT
            SEX YYMMDD(EXPIRY) CHECKDIGIT PERSONALNO<<CHECKDIGIT

    Returns a dict with the extracted fields. Does NOT trust the
    result blindly — this is meant to PRE-FILL a review form that
    a human then checks and corrects before anything is saved as
    a real business record.
    """
    result = {
        'full_name': '',
        'passport_number': '',
        'nationality': '',
        'date_of_birth': '',
        'date_of_expiry': '',
        'sex': '',
    }

    try:
        # ---- Line 1: Names ----
        # Format: P<COUNTRY<SURNAME<<GIVEN<NAMES<<<<<<<<<<<<<<<<<<<
        name_section = line1[5:]  # skip 'P<' + 3-letter country code
        surname_part, given_part = name_section.split('<<', 1)
        surname = surname_part.replace('<', ' ').strip()
        given_names = given_part.replace('<', ' ').strip()
        result['full_name'] = f"{given_names} {surname}".strip()

        # ---- Line 2: Passport number, nationality, DOB, sex, expiry ----
        passport_number_raw = line2[0:9].replace('<', '')
        result['passport_number'] = passport_number_raw

        nationality_raw = line2[10:13].replace('<', '')
        result['nationality'] = nationality_raw

        dob_raw = line2[13:19]  # YYMMDD
        result['date_of_birth'] = _format_mrz_date(dob_raw)

        sex_raw = line2[20:21]
        result['sex'] = sex_raw if sex_raw in ('M', 'F') else ''

        expiry_raw = line2[21:27]  # YYMMDD
        result['date_of_expiry'] = _format_mrz_date(expiry_raw)

    except (ValueError, IndexError):
        # If MRZ lines don't match the expected format, leave fields blank
        # rather than guessing — the user can still enter data manually.
        pass

    return result


def _format_mrz_date(yymmdd):
    """
    Converts an MRZ date (YYMMDD) into a readable DD-MM-YYYY string.
    Assumes years 00-30 are 2000s, and 31-99 are 1900s
    (a common convention, though not perfectly reliable —
    this is why the user must always review/confirm the result).
    """
    if len(yymmdd) != 6 or not yymmdd.isdigit():
        return ''

    yy = int(yymmdd[0:2])
    mm = yymmdd[2:4]
    dd = yymmdd[4:6]

    year = 2000 + yy if yy <= 30 else 1900 + yy

    return f"{dd}-{mm}-{year}"