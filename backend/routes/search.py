from flask import Blueprint, request, jsonify

from services.price_analyzer import (
    analyze_prices,
    analyze_comparable_prices,
    get_price_insight
)

from services.insight_engine import (
    generate_product_insight,
    generate_market_summary
)

from services.serpapi_service import (
    search_products
)

from services.product_normalizer import (
    normalize_products,
    remove_duplicates
)

from services.requirement_parser import (
    parse_requirements
)

from services.ranking_engine import (
    rank_products
)

from services.review_analyzer import (
    analyze_reviews
)

from database import save_search


search_bp = Blueprint(
    "search",
    __name__
)


@search_bp.route(
    "/api/search",
    methods=["POST"]
)
def search():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    query = (
        data.get(
            "query",
            ""
        )
        .strip()
    )


    if not query:

        return jsonify({

            "success": False,

            "error":
                "Search query is required"

        }), 400


    try:

        # --------------------------------
        # 1. Parse requirements
        # --------------------------------

        requirements = parse_requirements(
            query
        )


        # --------------------------------
        # 2. Build Shopping query
        # --------------------------------

        shopping_parts = []


        category = requirements.get(
            "category"
        )

        brand = requirements.get(
            "brand"
        )

        gpu = requirements.get(
            "gpu"
        )

        ram = requirements.get(
            "ram_gb"
        )

        storage = requirements.get(
            "storage_gb"
        )


        if category:

            shopping_parts.append(
                category
            )


        if brand:

            shopping_parts.append(
                brand
            )


        if gpu:

            shopping_parts.append(
                gpu
            )


        if ram:

            shopping_parts.append(
                f"{ram}GB RAM"
            )


        if storage:

            shopping_parts.append(
                f"{storage}GB storage"
            )


        if shopping_parts:

            shopping_query = " ".join(
                shopping_parts
            )

        else:

            shopping_query = query


        shopping_query = (
            shopping_query.strip()
        )


        # --------------------------------
        # 3. SerpApi
        # --------------------------------

        serp_results = search_products(
            shopping_query
        )


        shopping_results = (
            serp_results.get(
                "shopping_results",
                []
            )
        )


        # --------------------------------
        # 4. Normalize
        # --------------------------------

        products = normalize_products(
            shopping_results
        )


        # --------------------------------
        # 5. Remove duplicates
        # --------------------------------

        (
            unique_products,
            duplicates_removed
        ) = remove_duplicates(
            products
        )


        # --------------------------------
        # 6. Rank
        # --------------------------------

        ranked_products = rank_products(
            unique_products,
            requirements
        )


        # --------------------------------
        # 7. Overall market analysis
        # --------------------------------

        price_data = analyze_prices(
            ranked_products
        )


        # --------------------------------
        # 8. Comparable market analysis
        # --------------------------------

        comparable_price_data = (
            analyze_comparable_prices(
                ranked_products,
                requirements
            )
        )


        # Use comparable market average
        # when available.
        insight_market_data = (
            comparable_price_data
            if comparable_price_data.get(
                "average_price"
            ) is not None
            else price_data
        )


        # --------------------------------
        # 9. Product intelligence
        # --------------------------------

        for product in ranked_products:

            product[
                "price_insight"
            ] = get_price_insight(

                product.get("price"),

                insight_market_data

            )


            product[
                "review_analysis"
            ] = analyze_reviews(
                product
            )


            product[
                "intelligence"
            ] = generate_product_insight(

                product,

                requirements,

                insight_market_data

            )


        # --------------------------------
        # 10. Market summary
        # --------------------------------

        market_summary = (
            generate_market_summary(

                ranked_products,

                requirements,

                insight_market_data

            )
        )


        # --------------------------------
        # 11. Save search
        # --------------------------------

        try:

            save_search(
                query
            )

        except Exception:

            pass


        # --------------------------------
        # 12. Response
        # --------------------------------

        return jsonify({

            "success":
                True,

            "query":
                query,

            "shopping_query":
                shopping_query,

            "requirements":
                requirements,

            "total_found":
                len(shopping_results),

            "normalized_count":
                len(products),

            "unique_count":
                len(unique_products),

            "duplicates_removed":
                duplicates_removed,

            "price_analysis":
                price_data,

            "comparable_price_analysis":
                comparable_price_data,

            "market_summary":
                market_summary,

            "results":
                ranked_products

        })


    except Exception as e:

        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500