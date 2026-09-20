import React from "react";

import ProductCard from "../components/ProductCard";
import ReviewAnalysis from "../components/ReviewAnalysis";

export default function Product({
  product,
}) {
  if (!product) {
    return (
      <div className="empty-state">
        <div>📦</div>

        <h2>
          No Product Selected
        </h2>
      </div>
    );
  }

  return (
    <div className="page-container">

      <div className="page-heading">

        <span className="small-label">
          PRODUCT DETAILS
        </span>

        <h1>
          Product Analysis
        </h1>

      </div>

      <ProductCard
        product={product}
        index={0}
      />

      <ReviewAnalysis
        product={product}
      />

    </div>
  );
}