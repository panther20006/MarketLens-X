from flask import Blueprint, request, jsonify

from services.price_analyzer import (
    analyze_prices,
    get_price_insight
)

from services.insight_engine import (
    generate_product_insight,
    generate_market_summary
)

from services.ranking_engine import (
    rank_products
)

from services.requirement_parser import (
    parse_requirements
)


insights_bp = Blueprint(
    "insights",
    __name__
)


@insights_bp.route(
    "/api/insights",
    methods=["POST"]
)
def insights():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    products = data.get(
        "products",
        []
    )


    query = data.get(
        "query",
        ""
    )


    if not products:

        return jsonify({

            "success": False,

            "error":
                "Products are required"

        }), 400


    requirements = parse_requirements(
        query
    )


    ranked_products = rank_products(

        products,

        requirements

    )


    price_data = analyze_prices(
        ranked_products
    )


    for product in ranked_products:

        product[
            "price_insight"
        ] = get_price_insight(

            product.get(
                "price"
            ),

            price_data

        )


        product[
            "intelligence"
        ] = generate_product_insight(

            product,

            requirements,

            price_data

        )


    market_summary = (
        generate_market_summary(

            ranked_products,

            requirements,

            price_data

        )
    )


    return jsonify({

        "success":
            True,

        "requirements":
            requirements,

        "price_analysis":
            price_data,

        "market_summary":
            market_summary,

        "products":
            ranked_products

    })