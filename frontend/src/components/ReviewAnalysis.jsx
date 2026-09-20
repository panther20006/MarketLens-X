import React from "react";

export default function ReviewAnalysis({
  product,
}) {
  const review =
    product?.review_analysis;

  if (!review) {
    return null;
  }

  return (
    <section className="review-analysis">

      <h3>
        Review Analysis
      </h3>

      {review.summary && (
        <p>
          {review.summary}
        </p>
      )}

      <div className="review-grid">

        {review.sentiment && (
          <div>
            <span>Sentiment</span>
            <strong>
              {review.sentiment}
            </strong>
          </div>
        )}

        {review.rating && (
          <div>
            <span>Rating</span>
            <strong>
              ⭐ {review.rating}
            </strong>
          </div>
        )}

      </div>

    </section>
  );
}