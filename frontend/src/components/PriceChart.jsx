import React from "react";

export default function PriceChart({
  products = [],
}) {
  const validProducts = products
    .filter(
      (product) =>
        product.price !== null &&
        product.price !== undefined &&
        !Number.isNaN(
          Number(product.price)
        )
    )
    .slice(0, 10);

  if (!validProducts.length) {
    return null;
  }

  const maxPrice = Math.max(
    ...validProducts.map((product) =>
      Number(product.price)
    )
  );

  return (
    <section className="price-chart">

      <div className="chart-heading">

        <h3>
          Price Overview
        </h3>

        <span>
          Top {validProducts.length}
        </span>

      </div>

      <div className="chart-bars">

        {validProducts.map(
          (product, index) => {

            const price =
              Number(product.price);

            const height =
              maxPrice > 0
                ? Math.max(
                    8,
                    (price / maxPrice) *
                      100
                  )
                : 8;

            return (
              <div
                className="bar-wrapper"
                key={index}
                title={
                  product.title ||
                  "Product"
                }
              >

                <div className="bar-value">
                  ₹
                  {Math.round(
                    price / 1000
                  )}
                  k
                </div>

                <div className="bar-container">
                  <div
                    className="bar"
                    style={{
                      height: `${height}%`,
                    }}
                  />
                </div>

                <div className="bar-label">
                  #{index + 1}
                </div>

              </div>
            );
          }
        )}

      </div>

    </section>
  );
}