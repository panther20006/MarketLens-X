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
    parse_requirements,
    build_shopping_query
)

from services.ranking_engine import (
    rank_products
)

from services.review_analyzer import (
    analyze_reviews
)

from services.platform_comparator import (
    get_platform_comparison
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
        # 2. Build Shopping Query
        # --------------------------------
        #
        # IMPORTANT:
        # Old code was converting:
        #
        # iPhone 15 128GB
        #
        # into:
        #
        # Phone
        #
        # Now we preserve the actual
        # product/model query.
        #

        shopping_query = build_shopping_query(
            query,
            requirements
        )

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


        # --------------------------------
        # 9. Select market data
        # --------------------------------
        #
        # Use comparable market average
        # when available.
        #

        insight_market_data = (
            comparable_price_data
            if comparable_price_data.get(
                "average_price"
            ) is not None
            else price_data
        )


        # --------------------------------
        # 10. Product intelligence
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
        # 11. Market summary
        # --------------------------------

        market_summary = (
            generate_market_summary(

                ranked_products,

                requirements,

                insight_market_data

            )
        )


        # --------------------------------
        # 12. Platform Comparison
        # --------------------------------
        #
        # Compare actual platforms returned
        # by SerpApi.
        #
        # Example:
        #
        # Amazon
        # Flipkart
        # Croma
        # Reliance Digital
        #
        # We DO NOT invent platforms.
        #

        platform_comparison = (
            get_platform_comparison(
                ranked_products
            )
        )


        # --------------------------------
        # 13. Save search
        # --------------------------------

        try:

            save_search(
                query
            )

        except Exception:

            pass


        # --------------------------------
        # 14. Response
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

            "platform_comparison":
                platform_comparison,

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