def analyze_reviews(product):

    rating = product.get(
        "rating"
    )

    reviews = product.get(
        "reviews"
    )


    if rating is None:

        rating_score = None

    else:

        try:

            rating_score = float(
                rating
            )

        except (
            ValueError,
            TypeError
        ):

            rating_score = None


    if reviews is None:

        review_count = 0

    else:

        try:

            review_count = int(
                reviews
            )

        except (
            ValueError,
            TypeError
        ):

            review_count = 0


    # Rating analysis
    if rating_score is None:

        rating_status = "Unknown"

    elif rating_score >= 4.5:

        rating_status = "Excellent"

    elif rating_score >= 4.0:

        rating_status = "Good"

    elif rating_score >= 3.0:

        rating_status = "Average"

    else:

        rating_status = "Low"


    # Review volume
    if review_count >= 5000:

        confidence = "Very High"

    elif review_count >= 1000:

        confidence = "High"

    elif review_count >= 100:

        confidence = "Medium"

    elif review_count > 0:

        confidence = "Low"

    else:

        confidence = "Unknown"


    if (

        rating_score is not None

        and rating_score >= 4.0

        and review_count >= 1000

    ):

        reputation = "Strong"

    elif (

        rating_score is not None

        and rating_score >= 4.0

    ):

        reputation = "Positive"

    elif (

        rating_score is not None

        and rating_score >= 3.0

    ):

        reputation = "Mixed"

    elif rating_score is not None:

        reputation = "Weak"

    else:

        reputation = "Unknown"


    return {

        "rating":
            rating_score,

        "reviews":
            review_count,

        "rating_status":
            rating_status,

        "review_confidence":
            confidence,

        "reputation":
            reputation

    }