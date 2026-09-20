import re


KNOWN_PLATFORMS = {
    "amazon.in": "Amazon",
    "amazon": "Amazon",
    "flipkart": "Flipkart",
    "meesho": "Meesho",
    "croma": "Croma",
    "reliance digital": "Reliance Digital",
    "reliancedigital": "Reliance Digital",
    "vijay sales": "Vijay Sales",
    "vijaysales": "Vijay Sales",
    "tata neu": "Tata Neu",
    "tata cliq": "Tata Cliq",
    "myntra": "Myntra",
    "poorvika": "Poorvika",
    "sangeetha": "Sangeetha",
}


def normalize_platform(store):
    if not store:
        return "Unknown"

    value = str(store).strip().lower()

    for key, platform in KNOWN_PLATFORMS.items():
        if key in value:
            return platform

    return str(store).strip()


def get_platform_comparison(products):
    """
    Group available products by platform.

    Only platforms actually returned by the search API are shown.
    No price is invented.
    """

    comparison = {}

    for product in products or []:
        store = product.get("store")
        platform = normalize_platform(store)

        if platform == "Unknown":
            continue

        price = product.get("price")

        if price is None:
            continue

        try:
            price = float(price)
        except (TypeError, ValueError):
            continue

        item = {
            "platform": platform,
            "store": store,
            "title": product.get("title", ""),
            "price": price,
            "rating": product.get("rating"),
            "reviews": product.get("reviews"),
            "link": product.get("link") or "",
            "thumbnail": product.get("thumbnail") or "",
            "ram_gb": product.get("ram_gb"),
            "storage_gb": product.get("storage_gb"),
            "gpu": product.get("gpu"),
            "brand": product.get("brand"),
        }

        if platform not in comparison:
            comparison[platform] = []

        comparison[platform].append(item)

    # Sort each platform by price
    for platform in comparison:
        comparison[platform].sort(
            key=lambda x: x["price"]
        )

    # Best/lowest offer from every platform
    platform_offers = []

    for platform, items in comparison.items():
        if not items:
            continue

        platform_offers.append(items[0])

    platform_offers.sort(
        key=lambda x: x["price"]
    )

    lowest_price = (
        platform_offers[0]["price"]
        if platform_offers
        else None
    )

    # Add price difference
    for item in platform_offers:
        if lowest_price is not None:
            item["price_difference"] = round(
                item["price"] - lowest_price,
                2,
            )
        else:
            item["price_difference"] = None

    return {
        "platform_count": len(platform_offers),
        "platforms": platform_offers,
        "lowest_price": lowest_price,
    }