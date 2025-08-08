# import pandas as pd
# import re
# from collections import Counter

# # Load CSV
# df = pd.read_csv('unique_city.csv')

# # Normalize city values
# df['city'] = df['city'].astype(str).str.strip().str.lower()

# # === Patterns to Flag Anomalies ===
# BLANK_TERMS = {
#     "", "none", "n/a", "no city specified.", "city not identified yet.",
#     "city information missing.", "not identified yet.", "no city specified",
#     "unknown", "unkown", "null", "test", "asdf", "qwerty", "tbd", "123", "nocity"
# }

# EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")
# NUMBER_REGEX = re.compile(r"\d{5,}")
# ONLY_SPECIAL_CHAR_REGEX = re.compile(r"^[^A-Za-z0-9\s]+$")  # entire string is only punctuation/symbols

# # === Anomaly Flagging Function ===
# def flag_city(city):
#     if city in BLANK_TERMS:
#         return "Blank/Placeholder", "Common placeholder or empty value"

#     if city.isdigit():
#         return "Numeric Only", "City name contains only digits"

#     if len(city) < 2:
#         return "Too Short", "City name is very short"

#     if EMAIL_REGEX.search(city):
#         return "Possible Email", "Looks like an email address"

#     if NUMBER_REGEX.search(city):
#         return "Long Number", "Contains a long number, possibly zip code"

#     if ONLY_SPECIAL_CHAR_REGEX.match(city):
#         return "Only Special Characters", "City name contains only punctuation or symbols"

#     return "", ""

# # Apply flagging without creating extra columns
# df[['flag', 'reason']] = df['city'].apply(lambda x: pd.Series(flag_city(x)))

# # Filter only flagged entries
# flagged_df = df[df['flag'] != ""]

# # Show flagged rows
# print(flagged_df[['city', 'flag', 'reason']])

# # Show flag summary
# flag_counts = Counter(flagged_df['flag'])
# print("\nFlag Summary:")
# for flag, count in flag_counts.items():
#     print(f"{flag}: {count}")

# # Export
# flagged_df.to_csv('flagged_cities_with_reason.csv', index=False)



import pandas as pd
import re
from collections import Counter

# Load CSV
df = pd.read_csv('unique_city.csv')

# Normalize city values
df['city'] = df['city'].astype(str).str.strip().str.lower()

# === Patterns to Flag Anomalies ===
BLANK_TERMS = {
    "", "none", "n/a", "no city specified.", "city not identified yet.",
    "city information missing.", "not identified yet.", "no city specified",
    "unknown", "unkown", "null", "test", "asdf", "qwerty", "tbd", "123", "nocity"
}

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")
NUMBER_REGEX = re.compile(r"\d+")                   # flags any digits
ONLY_SPECIAL_CHAR_REGEX = re.compile(r"^[^A-Za-z0-9\s]+$")
MULTIWORD_GENERIC_REGEX = re.compile(r"(city center|corporate office|downtown|area|business district|general area|region|location)")
REPEATED_CHAR_REGEX = re.compile(r"^(.)\1{2,}$")

# === Whitelist for Valid Odd City Names ===
WHITELIST = {
    "st. louis", "washington, d.c.", "ålesund", "new york", "los angeles", "san francisco"
    # Add more here as needed
}

def flag_city(city):
    if city in WHITELIST:
        return "", ""

    if city in BLANK_TERMS:
        return "Blank/Placeholder", "Common placeholder or empty value"

    if city.isdigit():
        return "Numeric Only", "City name contains only digits"

    if len(city) < 3:
        return "Too Short", "City name is very short"

    if EMAIL_REGEX.search(city):
        return "Possible Email", "Looks like an email address"

    if NUMBER_REGEX.search(city):
        return "Contains Number", "Contains a number (possibly zip code)"
    if REPEATED_CHAR_REGEX.match(city):
        return "Repeated Characters", "City name is repeated characters"

    if ONLY_SPECIAL_CHAR_REGEX.match(city):
        return "Only Special Characters", "City name contains only punctuation or symbols"

    if MULTIWORD_GENERIC_REGEX.search(city):
        return "Generic Location", "Multi-word generic location, not a true city"

    return "", ""

# Apply flagging
df[['flag', 'reason']] = df['city'].apply(lambda x: pd.Series(flag_city(x)))

# Filter only flagged entries
flagged_df = df[df['flag'] != ""]

# Show flagged rows
print(flagged_df[['city', 'flag', 'reason']])

# Show flag summary
flag_counts = Counter(flagged_df['flag'])
print("\nFlag Summary:")
for flag, count in flag_counts.items():
    print(f"{flag}: {count}")

# # Export
# flagged_df.to_csv('flagged_cities_with_reason.csv', index=False)

# Export to Excel
flagged_df.to_excel('flagged_cities_with_reason.xlsx', index=False)
