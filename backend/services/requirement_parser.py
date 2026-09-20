import re


def parse_requirements(query):
    """
    Convert natural-language product query into structured requirements.

    Example:
    "iPhone 15 128GB under 60000"

    =>
    {
        "brand": "Apple",
        "category": "Phone",
        "storage_gb": 128,
        "ram_gb": None,
        "gpu": None,
        "min_price": None,
        "max_price": 60000
    }
    """

    query = (query or "").strip()
    text = query.lower()

    requirements = {
        "brand": None,
        "category": None,
        "gpu": None,
        "ram_gb": None,
        "storage_gb": None,
        "min_price": None,
        "max_price": None,
    }

    # ---------------------------------------------------------
    # BRAND
    # ---------------------------------------------------------

    brand_patterns = {
        "Apple": [
            r"\bapple\b",
            r"\biphone\b",
            r"\bipad\b",
            r"\bmacbook\b",
        ],
        "Samsung": [r"\bsamsung\b"],
        "OnePlus": [r"\boneplus\b", r"\bone plus\b"],
        "Google": [r"\bgoogle pixel\b", r"\bpixel\b"],
        "Xiaomi": [r"\bxiaomi\b", r"\bredmi\b", r"\bmi\b"],
        "Realme": [r"\brealme\b"],
        "Oppo": [r"\boppo\b"],
        "Vivo": [r"\bvivo\b"],
        "Motorola": [r"\bmotorola\b", r"\bmoto\b"],
        "Nothing": [r"\bnothing\b"],
        "Nokia": [r"\bnokia\b"],
        "HP": [r"\bhp\b", r"\bhewlett[- ]packard\b"],
        "Dell": [r"\bdell\b"],
        "Lenovo": [r"\blenovo\b"],
        "Acer": [r"\bacer\b"],
        "ASUS": [r"\basus\b"],
        "MSI": [r"\bmsi\b"],
    }

    for brand, patterns in brand_patterns.items():
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
            requirements["brand"] = brand
            break

    # ---------------------------------------------------------
    # CATEGORY
    # ---------------------------------------------------------

    if re.search(
        r"\biphone\b|\bsmartphone\b|\bphone\b|\bmobile\b|\bandroid\b|\bpixel\b",
        text,
        re.IGNORECASE,
    ):
        requirements["category"] = "Phone"

    elif re.search(
        r"\blaptop\b|\bnotebook\b|\bmacbook\b",
        text,
        re.IGNORECASE,
    ):
        requirements["category"] = "Laptop"

    elif re.search(
        r"\btablet\b|\bipad\b",
        text,
        re.IGNORECASE,
    ):
        requirements["category"] = "Tablet"

    elif re.search(
        r"\bheadphone\b|\bearphone\b|\bearbuds\b|\btws\b",
        text,
        re.IGNORECASE,
    ):
        requirements["category"] = "Audio"

    elif re.search(
        r"\bmonitor\b|\bdisplay\b",
        text,
        re.IGNORECASE,
    ):
        requirements["category"] = "Monitor"

    elif re.search(
        r"\btv\b|\btelevision\b|\bsmart tv\b",
        text,
        re.IGNORECASE,
    ):
        requirements["category"] = "TV"

    # ---------------------------------------------------------
    # RAM
    # ---------------------------------------------------------

    ram_patterns = [
        r"\b(\d+)\s*gb\s*(?:ram|memory)\b",
        r"\bram\s*[:\-]?\s*(\d+)\s*gb\b",
        r"\bmemory\s*[:\-]?\s*(\d+)\s*gb\b",
    ]

    for pattern in ram_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            requirements["ram_gb"] = int(match.group(1))
            break

    # ---------------------------------------------------------
    # STORAGE
    # ---------------------------------------------------------

    storage_patterns = [
        r"\b(\d+(?:\.\d+)?)\s*tb\s*(?:storage|ssd|hdd|nvme)?\b",
        r"\b(\d+)\s*gb\s*(?:storage|ssd|hdd|nvme)\b",
        r"\bstorage\s*[:\-]?\s*(\d+)\s*gb\b",
    ]

    for pattern in storage_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = float(match.group(1))

            if "tb" in match.group(0).lower():
                value *= 1024

            requirements["storage_gb"] = int(value)
            break

    # ---------------------------------------------------------
    # GPU
    # ---------------------------------------------------------

    gpu_patterns = [
        r"\brtx\s*\d{3,4}(?:\s*(?:ti|super))?\b",
        r"\bgtx\s*\d{3,4}(?:\s*(?:ti|super))?\b",
        r"\bradeon\s*rx\s*\d{3,4}\b",
        r"\bintel\s*arc\s*[a-z]?\d{3}\b",
    ]

    for pattern in gpu_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            requirements["gpu"] = match.group(0).strip()
            break

    # Generic RTX query
    if requirements["gpu"] is None:
        if re.search(r"\brtx\b", text, re.IGNORECASE):
            requirements["gpu"] = "RTX"

    # ---------------------------------------------------------
    # MIN / MAX PRICE
    # ---------------------------------------------------------

    # under 60000
    match = re.search(
        r"(?:under|below|less than|max(?:imum)?|upto|up to)\s*₹?\s*([\d,]+)",
        text,
        re.IGNORECASE,
    )

    if match:
        requirements["max_price"] = int(match.group(1).replace(",", ""))

    # above 30000
    match = re.search(
        r"(?:above|over|more than|min(?:imum)?|from)\s*₹?\s*([\d,]+)",
        text,
        re.IGNORECASE,
    )

    if match:
        requirements["min_price"] = int(match.group(1).replace(",", ""))

    # 30000-60000
    match = re.search(
        r"₹?\s*([\d,]+)\s*(?:-|to)\s*₹?\s*([\d,]+)",
        text,
        re.IGNORECASE,
    )

    if match:
        requirements["min_price"] = int(match.group(1).replace(",", ""))
        requirements["max_price"] = int(match.group(2).replace(",", ""))

    return requirements


def build_shopping_query(query, requirements=None):
    """
    Preserve the user's important product terms.

    IMPORTANT:
    We do NOT reduce:
        "iPhone 15 128GB"
    to:
        "Phone"

    Instead the original product query is preserved.
    """

    original_query = (query or "").strip()

    if not original_query:
        return ""

    # Remove only obvious budget phrases.
    shopping_query = re.sub(
        r"\b(?:under|below|less than|upto|up to|max(?:imum)?)\s*₹?\s*[\d,]+",
        "",
        original_query,
        flags=re.IGNORECASE,
    )

    shopping_query = re.sub(
        r"\b(?:above|over|more than|min(?:imum)?)\s*₹?\s*[\d,]+",
        "",
        shopping_query,
        flags=re.IGNORECASE,
    )

    shopping_query = re.sub(
        r"₹?\s*[\d,]+\s*(?:-|to)\s*₹?\s*[\d,]+",
        "",
        shopping_query,
        flags=re.IGNORECASE,
    )

    shopping_query = re.sub(r"\s+", " ", shopping_query).strip()

    return shopping_query or original_query