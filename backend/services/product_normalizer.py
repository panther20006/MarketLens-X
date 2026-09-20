import re


# =========================================================
# PRICE
# =========================================================

def clean_price(price):
    if price is None:
        return None

    if isinstance(price, (int, float)):
        return float(price)

    text = str(price).strip()

    if not text:
        return None

    # Remove currency symbols but keep digits, comma, decimal and minus
    text = re.sub(r"[^\d,.\-]", "", text)

    if not text:
        return None

    # Indian format:
    # 1,03,990 -> 103990
    # 70,000 -> 70000
    #
    # Normal decimal:
    # 69999.99 -> 69999.99
    if "," in text:
        text = text.replace(",", "")

    try:
        return float(text)
    except ValueError:
        return None


# =========================================================
# RATING
# =========================================================

def clean_rating(rating):
    if rating is None:
        return None

    try:
        value = float(rating)

        if value < 0:
            return None

        return value

    except (ValueError, TypeError):
        return None


# =========================================================
# REVIEWS
# =========================================================

def clean_reviews(reviews):
    if reviews is None:
        return None

    if isinstance(reviews, (int, float)):
        return int(reviews)

    text = str(reviews).strip().lower()

    if not text:
        return None

    # 1,234 reviews
    text = text.replace(",", "")

    # 1.2k reviews
    match = re.search(
        r"([\d.]+)\s*k",
        text
    )

    if match:
        try:
            return int(
                float(match.group(1)) * 1000
            )
        except ValueError:
            pass

    # 2.3m reviews
    match = re.search(
        r"([\d.]+)\s*m",
        text
    )

    if match:
        try:
            return int(
                float(match.group(1)) * 1000000
            )
        except ValueError:
            pass

    match = re.search(
        r"\d+",
        text
    )

    if match:
        try:
            return int(match.group())
        except ValueError:
            return None

    return None


# =========================================================
# TEXT HELPERS
# =========================================================

def safe_text(value):
    if value is None:
        return ""

    return str(value).strip()


def flatten_value(value):
    """
    Convert nested SerpApi data into searchable text.

    Handles:
    - string
    - number
    - list
    - tuple
    - dictionary
    """

    if value is None:
        return []

    if isinstance(value, (str, int, float)):
        return [str(value)]

    if isinstance(value, dict):
        result = []

        for key, item in value.items():
            result.append(str(key))
            result.extend(flatten_value(item))

        return result

    if isinstance(value, (list, tuple)):
        result = []

        for item in value:
            result.extend(flatten_value(item))

        return result

    return [str(value)]


def combined_product_text(product):
    """
    Build one large searchable text from the complete
    SerpApi product response.

    This helps extract RAM, storage, GPU, CPU, etc.
    even when the information is inside extensions,
    details, features or nested objects.
    """

    parts = []

    important_fields = [
        "title",
        "description",
        "snippet",
        "product_description",
        "specifications",
        "extensions",
        "details",
        "features",
        "highlights",
        "product_details",
        "attributes",
        "variants",
        "name",
    ]

    for field in important_fields:
        if field in product:
            parts.extend(
                flatten_value(product.get(field))
            )

    # Also inspect other textual/list/dict fields
    # returned by SerpApi.
    ignored_fields = {
        "price",
        "extracted_price",
        "rating",
        "reviews",
        "thumbnail",
        "link",
        "product_id",
    }

    for key, value in product.items():

        if key in ignored_fields:
            continue

        if isinstance(
            value,
            (str, int, float, list, tuple, dict)
        ):
            parts.extend(
                flatten_value(value)
            )

    return " ".join(
        safe_text(part)
        for part in parts
        if safe_text(part)
    )


# =========================================================
# RAM EXTRACTION
# =========================================================

def extract_ram(text):
    if not text:
        return None

    text = str(text)

    patterns = [

        # 16GB RAM
        r"\b(\d{1,3})\s*GB\s*(?:DDR[3456]\s*)?RAM\b",

        # 16 GB Memory
        r"\b(\d{1,3})\s*GB\s*(?:DDR[3456]\s*)?Memory\b",

        # 16GB DDR5
        r"\b(\d{1,3})\s*GB\s*DDR[3456]\b",

        # RAM: 16GB
        r"\bRAM\s*[:\-]?\s*(\d{1,3})\s*GB\b",

        # Memory: 16GB
        r"\bMemory\s*[:\-]?\s*(\d{1,3})\s*GB\b",

        # 16GB RAM Memory
        r"\b(\d{1,3})\s*GB\s*RAM\s*Memory\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            try:
                value = int(
                    match.group(1)
                )

                # Ignore unrealistic RAM values
                if 1 <= value <= 256:
                    return value

            except ValueError:
                pass

    return None


# =========================================================
# STORAGE EXTRACTION
# =========================================================

def extract_storage(text):
    """
    Extract storage capacity in GB.

    Examples:

    512GB SSD       -> 512
    1TB SSD         -> 1024
    2TB HDD         -> 2048
    256GB Pendrive  -> 256
    32GB Pen Drive  -> 32
    128GB USB       -> 128
    Storage: 512GB  -> 512
    Capacity 1TB    -> 1024
    """

    if not text:
        return None

    text = str(text)

    # Normalize common separators
    text = re.sub(
        r"[\u2013\u2014]",
        "-",
        text
    )

    patterns = [

        # -------------------------------------------------
        # SSD / HDD / NVMe
        # -------------------------------------------------

        # 1TB SSD
        # 1 TB SSD
        # 2TB HDD
        # 1TB NVMe
        r"\b(\d+(?:\.\d+)?)\s*TB\s*(?:SSD|HDD|NVMe|NVME|M\.2)\b",

        # 512GB SSD
        # 512 GB SSD
        # 256GB HDD
        # 512GB NVMe
        r"\b(\d+(?:\.\d+)?)\s*GB\s*(?:SSD|HDD|NVMe|NVME|M\.2)\b",

        # SSD 512GB
        # HDD 1TB
        # NVMe 512GB
        r"\b(?:SSD|HDD|NVMe|NVME|M\.2)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*GB\b",

        # SSD 1TB
        # HDD 2TB
        r"\b(?:SSD|HDD|NVMe|NVME|M\.2)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*TB\b",

        # -------------------------------------------------
        # STORAGE / CAPACITY
        # -------------------------------------------------

        # Storage: 512GB
        # Storage 512GB
        # Capacity: 1TB
        r"\b(?:Storage|Capacity)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*GB\b",

        r"\b(?:Storage|Capacity)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*TB\b",

        # 512GB Storage
        # 1TB Storage
        r"\b(\d+(?:\.\d+)?)\s*GB\s*(?:Storage|Capacity)\b",

        r"\b(\d+(?:\.\d+)?)\s*TB\s*(?:Storage|Capacity)\b",

        # -------------------------------------------------
        # PEN DRIVE / USB
        # -------------------------------------------------

        # 256GB Pendrive
        # 32GB Pen Drive
        # 128GB USB Drive
        # 64GB Flash Drive
        r"\b(\d+(?:\.\d+)?)\s*GB\s*(?:Pen\s*Drive|Pendrive|USB\s*Drive|USB|Flash\s*Drive)\b",

        # 256GB PenDrive
        r"\b(\d+(?:\.\d+)?)\s*GB\s*(?:PenDrive|Pendrive)\b",

        # Pen Drive 256GB
        # Pendrive 32GB
        # USB Drive 128GB
        r"\b(?:Pen\s*Drive|Pendrive|USB\s*Drive|Flash\s*Drive)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*GB\b",

        # -------------------------------------------------
        # EXTERNAL / PORTABLE DRIVE
        # -------------------------------------------------

        # 1TB External Drive
        # 2TB Portable Drive
        r"\b(\d+(?:\.\d+)?)\s*TB\s*(?:External\s+Drive|Portable\s+Drive)\b",

        # 500GB External Drive
        r"\b(\d+(?:\.\d+)?)\s*GB\s*(?:External\s+Drive|Portable\s+Drive)\b",

        # External Drive 1TB
        r"\b(?:External\s+Drive|Portable\s+Drive)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*TB\b",

        # External Drive 500GB
        r"\b(?:External\s+Drive|Portable\s+Drive)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*GB\b",

        # -------------------------------------------------
        # GENERIC "DISK"
        # -------------------------------------------------

        # 512GB Disk
        # 1TB Disk
        r"\b(\d+(?:\.\d+)?)\s*GB\s*(?:Disk|Drive)\b",

        r"\b(\d+(?:\.\d+)?)\s*TB\s*(?:Disk|Drive)\b",

        # Disk 512GB
        # Drive 1TB
        r"\b(?:Disk|Drive)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*GB\b",

        r"\b(?:Disk|Drive)\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*TB\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if not match:
            continue

        try:
            value = float(
                match.group(1)
            )

            matched_text = match.group(0).upper()

            if "TB" in matched_text:
                value *= 1024

            # Ignore unrealistic values
            if 1 <= value <= 32768:
                return int(value)

        except (ValueError, TypeError):
            pass

    return None


# =========================================================
# GPU EXTRACTION
# =========================================================

def extract_gpu(text):
    if not text:
        return None

    text = str(text)

    patterns = [

        # NVIDIA GeForce RTX 4050
        # NVIDIA GeForce RTX 4060 Ti
        # NVIDIA GeForce RTX 5070 SUPER
        r"\bNVIDIA\s+GeForce\s+RTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        # GeForce RTX 4050
        r"\bGeForce\s+RTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        # RTX 4050
        r"\bRTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        # NVIDIA GeForce RTX without model number
        r"\bNVIDIA\s+GeForce\s+RTX\b",

        # GeForce RTX without model number
        r"\bGeForce\s+RTX\b",

        # Plain RTX
        r"\bRTX\b",

        # GTX 1650 / GTX 1660 Ti
        r"\bNVIDIA\s+GeForce\s+GTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        r"\bGeForce\s+GTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        r"\bGTX\s+\d{3,4}(?:\s+(?:Ti|SUPER))?\b",

        # Radeon RX 7600 / RX 7600 XT
        r"\bAMD\s+Radeon\s+RX\s+\d{3,4}(?:\s+XT)?\b",

        r"\bRadeon\s+RX\s+\d{3,4}(?:\s+XT)?\b",

        # Intel Arc A770 / A750
        r"\bIntel\s+Arc\s+[A-Z]?\d{3,4}\b",

        # Intel integrated graphics
        r"\bIntel\s+(?:Iris\s+Xe|Iris|UHD|HD)\s+Graphics?\b",

        # AMD integrated graphics
        r"\bAMD\s+Radeon\s+(?:Graphics|Integrated\s+Graphics)\b",

        # Generic integrated graphics
        r"\bIntegrated\s+Graphics\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(0).strip()

    return None


# =========================================================
# CPU EXTRACTION
# =========================================================

def extract_cpu(text):
    if not text:
        return None

    text = str(text)

    patterns = [

        # Intel Core i5 / i7 / i9
        r"\bIntel\s+Core\s+(?:Ultra\s+)?[iI]\d(?:\s+\d{4,5}[A-Z]{0,2})?\b",

        # Core i5 / i7
        r"\bCore\s+[iI]\d(?:\s+\d{4,5}[A-Z]{0,2})?\b",

        # AMD Ryzen 5 5600H
        r"\bAMD\s+Ryzen\s+[3579]\s+\d{4,5}[A-Z]{0,2}\b",

        # Ryzen 5 5600H
        r"\bRyzen\s+[3579]\s+\d{4,5}[A-Z]{0,2}\b",

        # Apple M1 / M2 / M3 / M4 / M5
        r"\bApple\s+M[1-5](?:\s+(?:Pro|Max|Ultra))?\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(0).strip()

    return None


# =========================================================
# DISPLAY
# =========================================================

def extract_display(text):
    if not text:
        return None

    text = str(text)

    patterns = [
        r"\b(\d{2,3}(?:\.\d+)?)\s*Hz\b",
        r"\b(\d{2,3}(?:\.\d+)?)\s*inch\b",
    ]

    found = []

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            found.append(
                match.group(0).strip()
            )

    if found:
        return " / ".join(found)

    return None


# =========================================================
# BRAND
# =========================================================

def extract_brand(text):
    if not text:
        return None

    brands = [
        "Apple",
        "Samsung",
        "Dell",
        "HP",
        "Lenovo",
        "ASUS",
        "Acer",
        "MSI",
        "Gigabyte",
        "Razer",
        "Microsoft",
        "LG",
        "Sony",
        "OnePlus",
        "Xiaomi",
        "Realme",
        "Vivo",
        "Oppo",
    ]

    lower_text = text.lower()

    for brand in brands:

        if re.search(
            rf"\b{re.escape(brand.lower())}\b",
            lower_text
        ):
            return brand

    return None


# =========================================================
# NORMALIZE PRODUCT
# =========================================================

def normalize_product(product):

    title = safe_text(
        product.get("title")
    )

    combined_text = combined_product_text(
        product
    )

    # Extract once so the same value is used everywhere
    storage_gb = extract_storage(
        combined_text
    )

    ram_gb = extract_ram(
        combined_text
    )

    normalized = {

        "title":
            title,

        "price":
            clean_price(
                product.get("price")
            ),

        "rating":
            clean_rating(
                product.get("rating")
            ),

        "reviews":
            clean_reviews(
                product.get("reviews")
            ),

        "store":
            product.get("source")
            or product.get("store"),

        "link":
            product.get("link"),

        "thumbnail":
            product.get("thumbnail"),

        "product_id":
            product.get("product_id"),

        # =================================================
        # EXTRACTED SPECIFICATIONS
        # =================================================

        "brand":
            extract_brand(
                combined_text
            ),

        "ram_gb":
            ram_gb,

        "storage_gb":
            storage_gb,

        # Frontend compatibility
        "storage":
            storage_gb,

        "gpu":
            extract_gpu(
                combined_text
            ),

        "cpu":
            extract_cpu(
                combined_text
            ),

        "display":
            extract_display(
                combined_text
            ),

        # =================================================
        # USEFUL INTERNALLY
        # =================================================

        "_search_text":
            combined_text,
    }

    return normalized


# =========================================================
# NORMALIZE ALL
# =========================================================

def normalize_products(products):

    normalized = []

    for product in products:

        try:

            normalized.append(
                normalize_product(
                    product
                )
            )

        except Exception:

            continue

    return normalized


# =========================================================
# TITLE NORMALIZATION
# =========================================================

def normalize_title(title):

    if not title:
        return ""

    title = str(title).lower()

    # Keep specification information.
    # Only remove generic category words.

    replacements = [
        "mobile phone",
        "smartphone",
        "laptop computer",
        "computer",
    ]

    for word in replacements:

        title = title.replace(
            word,
            ""
        )

    title = re.sub(
        r"[^a-z0-9\s]",
        " ",
        title
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    ).strip()

    return title


# =========================================================
# DUPLICATE KEY
# =========================================================

def get_product_key(product):

    title = normalize_title(
        product.get("title")
    )

    brand = (
        product.get("brand")
        or ""
    )

    ram = (
        product.get("ram_gb")
        or ""
    )

    storage = (
        product.get("storage_gb")
        or ""
    )

    gpu = (
        product.get("gpu")
        or ""
    )

    # Use important specifications
    # so similar products can be identified.

    return (
        f"{brand}|"
        f"{title}|"
        f"{ram}|"
        f"{storage}|"
        f"{gpu}"
    )


# =========================================================
# REMOVE DUPLICATES
# =========================================================

def remove_duplicates(products):

    unique_products = {}

    duplicates = 0

    for product in products:

        key = get_product_key(
            product
        )

        if key in unique_products:

            duplicates += 1

            old_product = (
                unique_products[key]
            )

            old_price = (
                old_product.get("price")
            )

            new_price = (
                product.get("price")
            )

            # Keep lower valid price
            if (
                new_price is not None
                and (
                    old_price is None
                    or new_price < old_price
                )
            ):

                unique_products[key] = product

        else:

            unique_products[key] = product

    return (
        list(
            unique_products.values()
        ),
        duplicates
    )
    