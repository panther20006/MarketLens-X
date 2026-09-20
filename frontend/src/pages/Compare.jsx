import React from "react";

import CompareTable from "../components/CompareTable";

export default function Compare({
  products = [],
}) {
  return (
    <div className="page-container">

      <div className="page-heading">

        <span className="small-label">
          ANALYSIS
        </span>

        <h1>
          Compare Products
        </h1>

        <p>
          Compare products from your latest
          search.
        </p>

      </div>

      <CompareTable
        products={products}
      />

    </div>
  );
}