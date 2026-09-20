def analyze_prices(products):

    prices = [

        product.get("price")

        for product in products

        if isinstance(
            product.get("price"),
            (int, float)
        )

        and product.get("price") > 0

    ]


    if not prices:

        return {

            "lowest_price": None,

            "highest_price": None,

            "average_price": None,

            "price_range": None,

            "product_count": 0

        }


    lowest = min(
        prices
    )

    highest = max(
        prices
    )

    average = round(

        sum(prices)
        / len(prices),

        2

    )


    return {

        "lowest_price":
            lowest,

        "highest_price":
            highest,

        "average_price":
            average,

        "price_range":
            round(
                highest - lowest,
                2
            ),

        "product_count":
            len(prices)

    }


def analyze_comparable_prices(
    products,
    requirements
):

    max_price = requirements.get(
        "max_price"
    )

    comparable = []

    for product in products:

        price = product.get(
            "price"
        )

        score = product.get(
            "match_score",
            0
        )

        if price is None:
            continue

        if max_price:

            # Keep products near requested
            # market segment.

            if price <= max_price * 1.5:

                comparable.append(
                    price
                )

        elif score >= 40:

            comparable.append(
                price
            )


    if not comparable:

        return {

            "lowest_price": None,

            "highest_price": None,

            "average_price": None,

            "sample_size": 0

        }


    return {

        "lowest_price":
            min(comparable),

        "highest_price":
            max(comparable),

        "average_price":
            round(
                sum(comparable)
                / len(comparable),
                2
            ),

        "sample_size":
            len(comparable)

    }


def get_price_insight(
    price,
    market_data
):

    average = market_data.get(
        "average_price"
    )

    lowest = market_data.get(
        "lowest_price"
    )

    highest = market_data.get(
        "highest_price"
    )


    if (

        price is None

        or average is None

    ):

        return {

            "status": "Unknown",

            "difference": None,

            "percentage": None,

            "position": None

        }


    difference = round(

        average - price,

        2

    )


    if average > 0:

        percentage = round(

            (
                difference
                / average
            ) * 100,

            2

        )

    else:

        percentage = 0


    if price < average * 0.90:

        status = "Great Deal"

    elif price < average:

        status = "Below Market Average"

    elif price <= average * 1.10:

        status = "Near Market Average"

    else:

        status = "Above Market Average"


    if (

        lowest is not None

        and price == lowest

    ):

        position = "Lowest Price"

    elif (

        highest is not None

        and price == highest

    ):

        position = "Highest Price"

    elif price < average:

        position = "Below Average"

    elif price > average:

        position = "Above Average"

    else:

        position = "Market Average"


    return {

        "status":
            status,

        "difference":
            difference,

        "percentage":
            percentage,

        "position":
            position

    }