from flask import Blueprint, request, jsonify

from services.serpapi_service import search_products
from services.product_normalizer import normalize_products


products_bp = Blueprint(
    "products",
    __name__
)


@products_bp.route(
    "/api/products",
    methods=["GET"]
)
def products():

    query = request.args.get(
        "q",
        ""
    ).strip()


    if not query:

        return jsonify({

            "success": False,

            "error":
                "Product query is required"

        }), 400


    try:

        results = search_products(
            query
        )


        shopping_results = (
            results.get(
                "shopping_results",
                []
            )
        )


        normalized = normalize_products(
            shopping_results
        )


        return jsonify({

            "success":
                True,

            "query":
                query,

            "count":
                len(normalized),

            "products":
                normalized

        })


    except Exception as e:

        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500