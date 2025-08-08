import pandas as pd
import re
from collections import Counter

# Load CSV
df = pd.read_csv('unique_industries.csv')

# Normalize input
industries = df['industry'].astype(str).str.strip().str.lower()

# Predefine patterns
BLANK_TERMS = {
    "", "none", "n/a", "no industry specified.", "industry not identified yet.",
    "industry information missing.", "industry information missing", "not identified yet.",
    "no industry specified", "other"
}

TYPO_PATTERNS = {
    "acounting", "accountign", "servicess", "serivces", "buisness", "adviosr",
    "comercial", "consctruction", "conscruction", "conscuction", "manufscturing",
    "manufactturing", "educaiton", "edutational", "managementt", "manafacturing"
}

GENERIC = {"b2b", "it", "msp", "cpa", "ivindustry"}

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")
NUMBER_REGEX = re.compile(r"\d{5,}")
SPECIAL_CHAR_REGEX = re.compile(r"[!@#$%^&*()_=+{}\[\];:'\"\\|<>/?]")

# Keywords to detect bloated service lists
SERVICE_KEYWORDS = {
    "staffing", "recruiting", "assessments", "consulting", "services", "solutions", 
    "architecture", "penetration testing", "vulnerability", "managed", "cybersecurity", 
    "network", "project", "advanced", "security services"
}

# === Step 1: Context-aware suspicious industry detection ===
def is_suspicious(ind):
    ind_lower = ind.lower().strip()

    # Flag if contains 'test' or 'testing' in weak context
    if "test" in ind_lower or "testing" in ind_lower:
        valid_context_keywords = [
            "software", "services", "qa", "test prep", "equipment", "drug", "lab",
            "food", "diagnostic", "bootcamp", "training", "e-learning", "education",
            "compliance", "oral health", "safety", "penetration",
            "utility", "calibration", "inspection", "certification", "regulatory", "accreditation"
        ]
        if not any(valid_kw in ind_lower for valid_kw in valid_context_keywords):
            return True, f"Contains 'test' or 'testing' in suspicious context: '{ind_lower}'"

    # Too verbose / service dump
    word_count = len(ind_lower.split())
    if word_count > 15:
        return True, f"Too verbose — contains {word_count} words"

    # Service list overload
    keyword_hits = [kw for kw in SERVICE_KEYWORDS if kw in ind_lower]
    if len(keyword_hits) >= 4:
        return True, f"Likely a service list — contains: {', '.join(keyword_hits)}"

    # Exact suspicious values
    suspicious_exact = {
        "test", "testing", "example", "sample", "unknown", "asdf", "123",
        "misc", "miscellaneous", "niche", "uncategorized", "tbd", "not listed",
        "not identified", "learning opportunity", "education unknown"
    }
    if ind_lower in suspicious_exact:
        return True, f"Exact suspicious value: '{ind_lower}'"

    return False, ""

# === Step 2: Flagging function ===
def flag_industry(ind):
    if ind in BLANK_TERMS:
        return "Blank/None/Other", "Industry not provided or marked as missing"
    if EMAIL_REGEX.search(ind):
        return "Possibly personal info", "Contains email address"
    if NUMBER_REGEX.search(ind):
        return "Possibly personal info", "Contains long number or NAICS code"
    if len(ind) < 3:
        return "Too short", "Industry name is very short"

    suspicious, reason = is_suspicious(ind)
    if suspicious:
        return "Suspicious phrase", reason

    if any(typo in ind for typo in TYPO_PATTERNS):
        matched = [t for t in TYPO_PATTERNS if t in ind][0]
        return "Possible typo", f"Possible typo detected: '{matched}'"

    if ind.replace(" ", "") in GENERIC:
        return "Generic/Unspecific", f"Generic term: '{ind.strip()}'"

    return "", ""

# Apply flagging
df['industry_cleaned'] = industries
df[['flag', 'reason']] = df['industry_cleaned'].apply(lambda x: pd.Series(flag_industry(x)))

# Filter flagged rows
flagged_df = df[df['flag'] != ""]

# Display flagged rows
print(flagged_df[['industry', 'flag', 'reason']])

# Count by flag
flag_counts = Counter(flagged_df['flag'])
print("\nFlag Summary:")
for flag, count in flag_counts.items():
    print(f"{flag}: {count}")

# Save to Excel files
flagged_df.to_excel('flagged_industries_with_reason.xlsx', index=False)
df.to_excel('all_industries_with_flags_and_reasons.xlsx', index=False)




