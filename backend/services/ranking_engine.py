import re


# =========================================================
# GPU DETECTION
# =========================================================

def detect_non_rtx_gpu(text):
    """
    Detects GPUs which are NOT RTX.
    """

    if not text:
        return None

    patterns = [
        r"\bNVIDIA\s+GeForce\s+GTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",
        r"\bGeForce\s+GTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",
        r"\bGTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        r"\bAMD\s+Radeon\s+RX\s+\d{3,4}(?:\s+XT)?\b",
        r"\bRadeon\s+RX\s+\d{3,4}(?:\s+XT)?\b",

        r"\bIntel\s+Arc\s+[A-Z]?\d{3,4}\b",

        r"\bIntel\s+(?:Iris\s+Xe|Iris|UHD|HD)\s+Graphics?\b",

        r"\bAMD\s+Radeon\s+(?:Graphics|Integrated\s+Graphics)\b",

        r"\bIntegrated\s+Graphics\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0)

    return None


def detect_rtx(text):
    """
    Detect RTX GPUs.

    Supports:
    RTX
    RTX 3050
    RTX 4050
    RTX 4060
    RTX 5060
    NVIDIA GeForce RTX
    NVIDIA GeForce RTX 4050
    """

    if not text:
        return False

    pattern = (
        r"\b"
        r"(?:NVIDIA\s+GeForce\s+)?"
        r"RTX"
        r"(?:\s+\d{3,4}(?:\s+(?:Ti|SUPER))?)?"
        r"\b"
    )

    return bool(re.search(pattern, text, re.IGNORECASE))


def extract_gpu(text):
    """
    Extract GPU name from product text.
    """

    if not text:
        return None

    patterns = [

        # RTX
        r"\bNVIDIA\s+GeForce\s+RTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",
        r"\bGeForce\s+RTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",
        r"\bRTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        # Plain RTX
        r"\bNVIDIA\s+GeForce\s+RTX\b",
        r"\bGeForce\s+RTX\b",
        r"\bRTX\b",

        # GTX
        r"\bNVIDIA\s+GeForce\s+GTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",
        r"\bGeForce\s+GTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",
        r"\bGTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        # AMD
        r"\bAMD\s+Radeon\s+RX\s+\d{3,4}(?:\s+XT)?\b",
        r"\bRadeon\s+RX\s+\d{3,4}(?:\s+XT)?\b",

        # Intel
        r"\bIntel\s+Arc\s+[A-Z]?\d{3,4}\b",

        # Integrated
        r"\bIntel\s+(?:Iris\s+Xe|Iris|UHD|HD)\s+Graphics?\b",
        r"\bAMD\s+Radeon\s+(?:Graphics|Integrated\s+Graphics)\b",
        r"\bIntegrated\s+Graphics\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0)

    return None


# =========================================================
# REQUIREMENT HELPERS
# =========================================================

def _search_text(product):
    """
    Creates searchable text from normalized product.
    """

    if not product:
        return ""

    parts = []

    for key in [
        "title",
        "name",
        "description",
        "snippet",
        "product_title",
        "category",
        "brand",
        "gpu",
    ]:
        value = product.get(key)

        if value is not None:
            parts.append(str(value))

    return " ".join(parts)


def _get_price(product):
    """
    Safely gets product price.
    """

    if not product:
        return None

    price = product.get("price")

    if price is None:
        price = product.get("extracted_price")

    if price is None:
        price = product.get("amount")

    try:
        if isinstance(price, str):
            cleaned = re.sub(r"[^\d.]", "", price)

            if not cleaned:
                return None

            return float(cleaned)

        return float(price)

    except (ValueError, TypeError):
        return None


def _get_ram(product):
    """
    Gets RAM from normalized product or title text.
    """

    if not product:
        return None

    ram = product.get("ram")

    if ram is not None:
        try:
            return int(float(ram))
        except (ValueError, TypeError):
            pass

    text = _search_text(product)

    patterns = [
        r"\b(\d{1,3})\s*GB\s*(?:DDR\d)?\s*RAM\b",
        r"\b(\d{1,3})\s*GB\s*RAM\b",
        r"\bRAM\s*[:\-]?\s*(\d{1,3})\s*GB\b",
        r"\b(\d{1,3})\s*GB\s*(?:DDR\d)?\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass

    return None


def _get_storage(product):
    """
    Gets storage from normalized product or text.
    """

    if not product:
        return None

    storage = product.get("storage")

    if storage is not None:
        return str(storage)

    text = _search_text(product)

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(TB|GB)\s*(?:SSD|HDD|NVME|STORAGE)?\b",
        text,
        re.IGNORECASE,
    )

    if match:
        return f"{match.group(1)} {match.group(2).upper()}"

    return None


# =========================================================
# CATEGORY CHECK
# =========================================================

def _is_gaming_laptop(product):
    """
    Checks whether product looks like a gaming laptop.
    """

    text = _search_text(product).lower()

    gaming_keywords = [
        "gaming laptop",
        "gaming notebook",
        "gaming",
        "loq",
        "legion",
        "tuf gaming",
        "rog",
        "nitro",
        "predator",
        "victus",
        "omen",
        "katana",
        "cyborg",
        "gf63",
        "ideapad gaming",
    ]

    for keyword in gaming_keywords:
        if keyword in text:
            return True

    return False


# =========================================================
# REQUIREMENT CHECK
# =========================================================

def check_requirements(product, requirements):
    """
    Checks product against parsed requirements.

    Returns:
        {
            "status": "...",
            "matched": [...],
            "warnings": [...]
        }
    """

    matched = []
    warnings = []

    if not requirements:
        return {
            "status": "Verified Match",
            "matched": [],
            "warnings": [],
        }

    text = _search_text(product)

    # -----------------------------------------------------
    # BUDGET
    # -----------------------------------------------------

    max_price = requirements.get("max_price")

    price = _get_price(product)

    if max_price is not None:

        try:
            max_price = float(max_price)
        except (ValueError, TypeError):
            max_price = None

    if max_price is not None:

        if price is None:
            warnings.append("Price not confirmed")

        elif price > max_price:
            warnings.append("Above budget")

        else:
            matched.append("Within budget")

    # -----------------------------------------------------
    # RAM
    # -----------------------------------------------------

    required_ram = requirements.get("ram")

    if required_ram is None:
        required_ram = requirements.get("ram_gb")

    if required_ram is not None:

        try:
            required_ram = int(required_ram)
        except (ValueError, TypeError):
            required_ram = None

    if required_ram is not None:

        actual_ram = _get_ram(product)

        if actual_ram is None:

            warnings.append(
                f"{required_ram}GB RAM not confirmed"
            )

        elif actual_ram >= required_ram:

            matched.append(
                f"{required_ram}GB RAM"
            )

        else:

            warnings.append(
                f"RAM below {required_ram}GB"
            )

    # -----------------------------------------------------
    # GPU
    # -----------------------------------------------------

    required_gpu = requirements.get("gpu")

    if required_gpu:

        required_gpu_text = str(required_gpu).lower()

        product_gpu = product.get("gpu")

        if product_gpu:
            actual_gpu_text = str(product_gpu)
        else:
            actual_gpu_text = extract_gpu(text)

        combined_gpu_text = (
            f"{actual_gpu_text or ''} {text}"
        ).lower()

        wants_rtx = "rtx" in required_gpu_text

        if wants_rtx:

            if detect_rtx(combined_gpu_text):

                matched.append("RTX GPU")

            else:

                warnings.append(
                    "RTX not confirmed"
                )

        else:

            if actual_gpu_text:

                if required_gpu_text in actual_gpu_text.lower():

                    matched.append("Required GPU")

                else:

                    warnings.append(
                        "Required GPU not confirmed"
                    )

            else:

                warnings.append(
                    "Required GPU not confirmed"
                )

    # -----------------------------------------------------
    # STORAGE
    # -----------------------------------------------------

    required_storage = requirements.get("storage")

    if required_storage is None:
        required_storage = requirements.get("storage_gb")

    if required_storage is not None:

        storage_text = _get_storage(product)

        if storage_text:

            numbers = re.findall(
                r"\d+(?:\.\d+)?",
                storage_text
            )

            try:
                actual_storage = float(numbers[0])

                if "TB" in storage_text.upper():
                    actual_storage *= 1024

                required_storage_value = float(
                    re.sub(
                        r"[^\d.]",
                        "",
                        str(required_storage)
                    )
                )

                if actual_storage >= required_storage_value:

                    matched.append(
                        "Required storage"
                    )

                else:

                    warnings.append(
                        "Storage below requirement"
                    )

            except (ValueError, IndexError):

                warnings.append(
                    "Storage not confirmed"
                )

        else:

            warnings.append(
                "Storage not confirmed"
            )

    # -----------------------------------------------------
    # GAMING LAPTOP
    # -----------------------------------------------------

    category = requirements.get("category")

    if category is None:
        category = requirements.get("product_type")

    if category:

        category_text = str(category).lower()

        if "gaming" in category_text:

            if _is_gaming_laptop(product):

                matched.append(
                    "Gaming Laptop category"
                )

            else:

                warnings.append(
                    "Gaming Laptop category not fully confirmed"
                )

    # -----------------------------------------------------
    # FINAL STATUS
    # -----------------------------------------------------

    hard_fail = False
    hard_unknown = False

    if "Above budget" in warnings:
        hard_fail = True

    if "RAM below" in " ".join(warnings):
        hard_fail = True

    if "Storage below" in " ".join(warnings):
        hard_fail = True

    if "RTX not confirmed" in warnings:
        hard_unknown = True

    if "not confirmed" in " ".join(warnings):
        hard_unknown = True

    # -----------------------------------------------------
    # IMPORTANT FIX
    # Never mark "All requested specifications verified"
    # before final status is known.
    # -----------------------------------------------------

    if hard_fail:

        status = "Does Not Match"

    elif hard_unknown:

        status = "Needs Verification"

    else:

        status = "Verified Match"

    # -----------------------------------------------------
    # ONLY Verified Match gets this label
    # -----------------------------------------------------

    if status == "Verified Match":

        matched.append(
            "All requested specifications verified"
        )

    else:

        # Safety cleanup in case any earlier logic adds it
        matched = [
            item
            for item in matched
            if item != "All requested specifications verified"
        ]

    return {
        "status": status,
        "matched": matched,
        "warnings": warnings,
    }

def calculate_match_score(product, requirements):
    """
    Calculate a compatibility score for compare.py
    and other ranking/analysis modules.

    Score:
        100 = all requested requirements verified
        0   = no useful match
    """

    if not product:
        return 0

    requirements = requirements or {}

    check = check_requirements(
        product,
        requirements
    )

    status = check.get("status")

    # Final status has highest importance
    if status == "Verified Match":
        return 100

    if status == "Needs Verification":
        score = 60
    else:
        score = 20

    matched = check.get("matched", [])
    warnings = check.get("warnings", [])

    # Positive matches
    if matched:
        score += min(len(matched) * 8, 25)

    # Warnings reduce score
    if warnings:
        score -= min(len(warnings) * 10, 30)

    # Budget failure is especially important
    if "Above budget" in warnings:
        score -= 25

    return max(0, min(100, score))
# =========================================================
# PRODUCT RANKING
# =========================================================

def rank_products(products, requirements):
    """
    Rank products based on requirement matching.

    Priority:
        1. Verified Match
        2. Needs Verification
        3. Does Not Match

    Within same status:
        - rating
        - reviews
        - price
    """

    if not products:
        return []

    ranked = []

    for product in products:

        if not isinstance(product, dict):
            continue

        check = check_requirements(
            product,
            requirements or {}
        )

        product["requirement_status"] = check["status"]

        product["matched"] = check["matched"]

        product["warnings"] = check["warnings"]

        # -------------------------------------------------
        # Rating
        # -------------------------------------------------

        rating = product.get("rating")

        try:
            rating_value = float(rating)
        except (ValueError, TypeError):
            rating_value = 0

        # -------------------------------------------------
        # Reviews
        # -------------------------------------------------

        reviews = product.get("reviews")

        try:
            review_value = int(float(reviews))
        except (ValueError, TypeError):
            review_value = 0

        # -------------------------------------------------
        # Price
        # -------------------------------------------------

        price = _get_price(product)

        if price is None:
            price_value = float("inf")
        else:
            price_value = price

        # -------------------------------------------------
        # Status priority
        # -------------------------------------------------

        status_priority = {
            "Verified Match": 0,
            "Needs Verification": 1,
            "Does Not Match": 2,
        }

        priority = status_priority.get(
            check["status"],
            3
        )

        # -------------------------------------------------
        # Internal ranking data
        # -------------------------------------------------

        product["_ranking"] = (
            priority,
            -rating_value,
            -review_value,
            price_value,
        )

        ranked.append(product)

    # -----------------------------------------------------
    # Sort
    # -----------------------------------------------------

    ranked.sort(
        key=lambda item: item.get(
            "_ranking",
            (3, 0, 0, float("inf"))
        )
    )

    # -----------------------------------------------------
    # Remove internal ranking field
    # -----------------------------------------------------

    for product in ranked:

        product.pop("_ranking", None)

    return ranked