import re


def parse_requirements(query):

    text = query.lower().strip()

    requirements = {

        "category": None,

        "max_price": None,

        "min_price": None,

        "ram_gb": None,

        "storage_gb": None,

        "gpu": None,

        "brand": None

    }


    # -------------------------
    # PRICE
    # -------------------------

    price_patterns = [

        r"(?:under|below|less than|within|upto|up to)"
        r"\s*₹?\s*([\d,]+)\s*(k|thousand|lakh)?",

        r"₹\s*([\d,]+)\s*(k|thousand|lakh)?"

    ]


    for pattern in price_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            value = match.group(1)

            value = value.replace(
                ",",
                ""
            )

            value = float(value)

            multiplier = match.group(2)

            if multiplier in [
                "k",
                "thousand"
            ]:

                value *= 1000

            elif multiplier == "lakh":

                value *= 100000

            requirements["max_price"] = int(
                value
            )

            break


    # -------------------------
    # RAM
    # -------------------------

    ram_match = re.search(

        r"(\d+)\s*gb\s*"
        r"(?:ram|memory)",

        text

    )

    if ram_match:

        requirements["ram_gb"] = int(
            ram_match.group(1)
        )


    # -------------------------
    # STORAGE
    # -------------------------

    storage_match = re.search(

        r"(\d+)\s*(gb|tb)\s*"
        r"(?:storage|ssd|hdd)",

        text

    )

    if storage_match:

        value = int(
            storage_match.group(1)
        )

        unit = storage_match.group(2)

        if unit == "tb":

            value *= 1024

        requirements["storage_gb"] = value


    # -------------------------
    # GPU
    # -------------------------

    gpu_match = re.search(

        r"\b("
        r"rtx\s*\d*"
        r"|gtx\s*\d*"
        r"|radeon"
        r"|rx\s*\d+"
        r")\b",

        text

    )

    if gpu_match:

        requirements["gpu"] = (

            gpu_match.group(1)
            .upper()
            .strip()

        )


    # -------------------------
    # BRAND
    # -------------------------

    brands = [

        "apple",
        "samsung",
        "oneplus",
        "xiaomi",
        "redmi",
        "realme",
        "asus",
        "acer",
        "lenovo",
        "hp",
        "dell",
        "msi",
        "lg",
        "sony",
        "motorola",
        "oppo",
        "vivo"

    ]


    for brand in brands:

        if re.search(

            rf"\b{re.escape(brand)}\b",

            text

        ):

            requirements["brand"] = (
                brand.title()
            )

            break


    # -------------------------
    # CATEGORY
    # -------------------------

    categories = [

        "gaming laptop",

        "laptop",

        "smartphone",

        "phone",

        "mobile",

        "tablet",

        "headphones",

        "earbuds",

        "monitor",

        "tv",

        "smartwatch"

    ]


    for category in categories:

        if category in text:

            requirements["category"] = (
                category.title()
            )

            break


    return requirements