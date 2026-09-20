import React from "react";

function formatPrice(price) {
  if (
    price === null ||
    price === undefined ||
    price === ""
  ) {
    return "Price unavailable";
  }

  const value = Number(price);

  if (Number.isNaN(value)) {
    return String(price);
  }

  return `₹${value.toLocaleString("en-IN")}`;
}

export default function ProductCard({
  product,
  index,
}) {
  const status =
    product.requirement_status ||
    product.intelligence?.requirement_status ||
    "Unknown";

  let statusClass = "failed";

  if (status === "Verified Match") {
    statusClass = "verified";
  } else if (
    status === "Needs Verification"
  ) {
    statusClass = "verification";
  }

  const matched =
    Array.isArray(product.matched)
      ? product.matched
      : [];

  const warnings =
    Array.isArray(product.warnings)
      ? product.warnings
      : [];

  const intelligence =
    product.intelligence || {};

  let insight =
    intelligence.why_this_product ||
    intelligence.summary ||
    "";

  if (typeof insight !== "string") {
    insight = JSON.stringify(insight);
  }

  return (
    <article className="product-card">

      <div className="product-rank">
        #{index + 1}
      </div>

      <div className="product-main">

        <div className="product-image">

          {product.image ? (
            <img
              src={product.image}
              alt={
                product.title ||
                "Product"
              }
            />
          ) : (
            <div className="image-placeholder">
              📦
            </div>
          )}

        </div>

        <div className="product-info">

          <h3>
            {product.title ||
              "Unnamed Product"}
          </h3>

          <div className="product-price">
            {formatPrice(product.price)}
          </div>

          <span
            className={`status-badge ${statusClass}`}
          >
            {status ===
              "Verified Match" && "✓ "}

            {status ===
              "Needs Verification" && "⚠ "}

            {status ===
              "Does Not Match" && "✕ "}

            {status}
          </span>

          {product.rating && (
            <div className="rating">
              ⭐ {product.rating}

              {product.reviews_count
                ? ` (${product.reviews_count} reviews)`
                : ""}
            </div>
          )}

        </div>

      </div>

      {matched.length > 0 && (
        <div className="product-section">

          <div className="section-title">
            ✓ Matched
          </div>

          <div className="tag-list">

            {matched.map(
              (item, itemIndex) => (
                <span
                  className="tag success-tag"
                  key={itemIndex}
                >
                  {item}
                </span>
              )
            )}

          </div>

        </div>
      )}

      {warnings.length > 0 && (
        <div className="product-section">

          <div className="section-title">
            ⚠ Warnings
          </div>

          <div className="tag-list">

            {warnings.map(
              (item, itemIndex) => (
                <span
                  className="tag warning-tag"
                  key={itemIndex}
                >
                  {item}
                </span>
              )
            )}

          </div>

        </div>
      )}

      {insight && (
        <div className="intelligence-box">

          <div className="section-title">
            🧠 MarketLens Insight
          </div>

          <p>{insight}</p>

        </div>
      )}

      {product.source && (
        <a
          href={product.source}
          target="_blank"
          rel="noreferrer"
          className="source-button"
        >
          View Product →
        </a>
      )}

    </article>
  );
}