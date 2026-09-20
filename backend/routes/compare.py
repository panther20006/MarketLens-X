from flask import Blueprint, request, jsonify

from services.price_analyzer import (
    analyze_prices
)

from services.ranking_engine import (
    calculate_match_score
)

from services.requirement_parser import (
    parse_requirements
)


compare_bp = Blueprint(
    "compare",
    __name__
)


@compare_bp.route(
    "/api/compare",
    methods=["POST"]
)
def compare():

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


    if not products:

        return jsonify({

            "success": False,

            "error":
                "Products are required"

        }), 400


    query = data.get(
        "query",
        ""
    )


    requirements = parse_requirements(
        query
    )


    analyzed_products = []


    for product in products:

        analysis = calculate_match_score(

            product,

            requirements

        )


        analyzed_products.append({

            **product,

            "match_score":
                analysis["score"],

            "matched":
                analysis["matched"],

            "warnings":
                analysis["warnings"]

        })


    analyzed_products.sort(

        key=lambda item:
            item.get(
                "match_score",
                0
            ),

        reverse=True

    )


    price_analysis = analyze_prices(
        analyzed_products
    )


    return jsonify({

        "success":
            True,

        "requirements":
            requirements,

        "price_analysis":
            price_analysis,

        "products":
            analyzed_products

    })