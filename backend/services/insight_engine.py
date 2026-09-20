# =========================================================
# PRODUCT INSIGHT
# =========================================================

def generate_product_insight(
    product,
    requirements,
    price_data
):

    title = (
        product.get("title")
        or "Unknown Product"
    )

    price = product.get("price")

    score = product.get(
        "match_score",
        0
    )

    matched = product.get(
        "matched",
        []
    )

    warnings = product.get(
        "warnings",
        []
    )

    requirement_status = product.get(
        "requirement_status",
        "Needs Verification"
    )

    price_insight = product.get(
        "price_insight",
        {}
    )

    price_status = price_insight.get(
        "status",
        "Unknown"
    )

    position = price_insight.get(
        "position",
        "Unknown"
    )

    average_price = price_data.get(
        "average_price"
    )

    max_price = requirements.get(
        "max_price"
    )

    # =====================================================
    # BUDGET
    # =====================================================

    if price is None:

        budget_status = "Price unavailable"

    elif max_price is None:

        budget_status = "No budget specified"

    elif price <= max_price:

        budget_status = "Within budget"

    else:

        budget_status = "Above budget"

    # =====================================================
    # SPEC CHECKS
    # =====================================================

    spec_checks = []

    spec_details = product.get(
        "spec_details",
        {}
    )

    # -----------------------------------------------------
    # RAM
    # -----------------------------------------------------

    if requirements.get("ram_gb"):

        required_ram = requirements[
            "ram_gb"
        ]

        ram_status = spec_details.get(
            "ram"
        )

        if ram_status is True:

            status_text = "Matched"

        elif ram_status is False:

            status_text = "Does not match"

        else:

            status_text = "Not confirmed"

        spec_checks.append({
            "spec": f"{required_ram}GB RAM",
            "status": status_text
        })

    # -----------------------------------------------------
    # GPU
    # -----------------------------------------------------

    if requirements.get("gpu"):

        required_gpu = requirements[
            "gpu"
        ]

        gpu_status = spec_details.get(
            "gpu"
        )

        if gpu_status is True:

            status_text = "Matched"

        elif gpu_status is False:

            status_text = "Does not match"

        else:

            status_text = "Not confirmed"

        spec_checks.append({
            "spec": required_gpu,
            "status": status_text
        })

    # -----------------------------------------------------
    # STORAGE
    # -----------------------------------------------------

    if requirements.get("storage_gb"):

        required_storage = requirements[
            "storage_gb"
        ]

        storage_status = spec_details.get(
            "storage"
        )

        if storage_status is True:

            status_text = "Matched"

        elif storage_status is False:

            status_text = "Does not match"

        else:

            status_text = "Not confirmed"

        spec_checks.append({
            "spec": f"{required_storage}GB Storage",
            "status": status_text
        })

    # =====================================================
    # MARKET COMPARISON
    # =====================================================

    if (
        price is not None
        and average_price is not None
    ):

        market_difference = round(
            average_price - price,
            2
        )

        if market_difference > 0:

            market_message = (
                f"₹{market_difference:,.0f} "
                "below market average"
            )

        elif market_difference < 0:

            market_message = (
                f"₹{abs(market_difference):,.0f} "
                "above market average"
            )

        else:

            market_message = (
                "At market average"
            )

    else:

        market_difference = None

        market_message = (
            "Market comparison unavailable"
        )

    # =====================================================
    # DEAL QUALITY
    # =====================================================

    if price_status == "Great Deal":

        deal_quality = "Excellent price"

    elif price_status == "Below Market Average":

        deal_quality = "Good price"

    elif price_status == "Near Market Average":

        deal_quality = "Average price"

    elif price_status == "Above Market Average":

        deal_quality = "Above market"

    else:

        deal_quality = "Unknown"

    # =====================================================
    # SUMMARY
    # =====================================================

    if requirement_status == "Does Not Match":

        if budget_status == "Above budget":

            summary = (
                "This product does not satisfy "
                "the requested requirements and "
                "is above the requested budget."
            )

        else:

            summary = (
                "This product does not satisfy "
                "one or more requested specifications. "
                "It should not be treated as a direct match."
            )

    elif requirement_status == "Needs Verification":

        if budget_status == "Above budget":

            summary = (
                "This product may match some "
                "requested specifications, but "
                "some details could not be verified "
                "and the product is above budget."
            )

        else:

            summary = (
                "This product may match the request, "
                "but one or more specifications could "
                "not be verified from the available data."
            )

    elif (
        requirement_status == "Verified Match"
        and budget_status == "Within budget"
        and price_status == "Great Deal"
    ):

        summary = (
            "The product matches the requested "
            "specifications, is within budget, "
            "and is priced well compared with "
            "the analyzed market."
        )

    elif (
        requirement_status == "Verified Match"
        and budget_status == "Within budget"
    ):

        summary = (
            "The product matches the requested "
            "specifications and is within the "
            "requested budget."
        )

    elif (
        requirement_status == "Verified Match"
        and budget_status == "Above budget"
    ):

        summary = (
            "The requested specifications are "
            "verified, but the product is above "
            "the requested budget."
        )

    else:

        summary = (
            "Product information was analyzed "
            "against the requested requirements."
        )

    # =====================================================
    # WHY THIS PRODUCT
    # =====================================================

    why_this_product = []

    # -----------------------------------------------------
    # Requirement status
    # -----------------------------------------------------

    if requirement_status == "Verified Match":

        why_this_product.append(
            "Requested specifications verified"
        )

    elif requirement_status == "Needs Verification":

        why_this_product.append(
            "Some specifications need verification"
        )

    else:

        why_this_product.append(
            "One or more requested specifications do not match"
        )

    # -----------------------------------------------------
    # Budget
    # -----------------------------------------------------

    if budget_status == "Within budget":

        why_this_product.append(
            "Fits the requested budget"
        )

    elif budget_status == "Above budget":

        why_this_product.append(
            "Above the requested budget"
        )

    elif budget_status == "Price unavailable":

        why_this_product.append(
            "Price unavailable"
        )

    # -----------------------------------------------------
    # Matched items
    #
    # IMPORTANT:
    # Do not copy misleading positive messages from
    # `matched` when the overall product failed.
    # -----------------------------------------------------

    if requirement_status != "Does Not Match":

        for item in matched[:4]:

            if not item:
                continue

            if item in [
                "All requested specifications verified",
                "All requested specifications verified."
            ]:

                # Only allow this message for an actual
                # verified match.
                if requirement_status != "Verified Match":
                    continue

            if item not in why_this_product:

                why_this_product.append(item)

    # -----------------------------------------------------
    # Deal information
    # -----------------------------------------------------

    if price_status in [
        "Great Deal",
        "Below Market Average"
    ]:

        if price_status not in why_this_product:

            why_this_product.append(
                price_status
            )

    # -----------------------------------------------------
    # Remove duplicates
    # -----------------------------------------------------

    why_this_product = list(
        dict.fromkeys(
            why_this_product
        )
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "title":
            title,

        "summary":
            summary,

        "budget_status":
            budget_status,

        "deal_quality":
            deal_quality,

        "market_position":
            position,

        "market_message":
            market_message,

        "market_difference":
            market_difference,

        "spec_checks":
            spec_checks,

        "why_this_product":
            why_this_product,

        "warnings":
            warnings,

        "match_score":
            score,

        "requirement_status":
            requirement_status,

        "verified_specs":
            product.get(
                "verified_specs",
                False
            ),

        "hard_fail":
            product.get(
                "hard_fail",
                False
            ),
    }


# =========================================================
# MARKET SUMMARY
# =========================================================

def generate_market_summary(
    products,
    requirements,
    price_data
):

    total = len(
        products
    )

    if total == 0:

        return {

            "summary":
                "No products found.",

            "total_products":
                0,

            "budget_products":
                0,

            "great_deals":
                0,

            "average_price":
                None,

            "verified_matches":
                0,

            "needs_verification":
                0,

            "failed_matches":
                0
        }

    max_price = requirements.get(
        "max_price"
    )

    budget_products = 0
    great_deals = 0
    verified_matches = 0
    needs_verification = 0
    failed_matches = 0

    for product in products:

        price = product.get(
            "price"
        )

        price_status = (
            product.get(
                "price_insight",
                {}
            )
            .get("status")
        )

        requirement_status = product.get(
            "requirement_status"
        )

        # -------------------------------------------------
        # Budget
        # -------------------------------------------------

        if (
            max_price is not None
            and price is not None
            and price <= max_price
        ):

            budget_products += 1

        # -------------------------------------------------
        # Great deals
        # -------------------------------------------------

        if price_status == "Great Deal":

            great_deals += 1

        # -------------------------------------------------
        # Requirement status
        # -------------------------------------------------

        if requirement_status == "Verified Match":

            verified_matches += 1

        elif requirement_status == "Needs Verification":

            needs_verification += 1

        elif requirement_status == "Does Not Match":

            failed_matches += 1

    # =====================================================
    # AVERAGE PRICE
    # =====================================================

    average_price = price_data.get(
        "average_price"
    )

    if average_price is not None:

        average_text = (
            f"₹{average_price:,.0f}"
        )

    else:

        average_text = "Unavailable"

    # =====================================================
    # SUMMARY TEXT
    # =====================================================

    if max_price is not None:

        summary = (
            f"{verified_matches} of {total} products "
            f"have all requested specifications verified. "
            f"{budget_products} are within the "
            f"₹{max_price:,.0f} budget. "
            f"Current market average is "
            f"{average_text}."
        )

    else:

        summary = (
            f"{verified_matches} of {total} products "
            f"have all requested specifications verified. "
            f"Current market average is "
            f"{average_text}."
        )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "summary":
            summary,

        "total_products":
            total,

        "budget_products":
            budget_products,

        "great_deals":
            great_deals,

        "average_price":
            average_price,

        "verified_matches":
            verified_matches,

        "needs_verification":
            needs_verification,

        "failed_matches":
            failed_matches
    }