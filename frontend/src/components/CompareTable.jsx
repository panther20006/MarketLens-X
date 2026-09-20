import React from "react";

export default function CompareTable({
  products = [],
}) {
  if (!products.length) {
    return (
      <div className="empty-state">
        <div>📊</div>

        <h3>
          No products to compare
        </h3>

        <p>
          Perform a search first.
        </p>
      </div>
    );
  }

  return (
    <section className="compare-table-wrapper">

      <h3>
        Product Comparison
      </h3>

      <div className="table-scroll">

        <table>

          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Status</th>
              <th>RAM</th>
              <th>GPU</th>
            </tr>
          </thead>

          <tbody>

            {products
              .slice(0, 15)
              .map(
                (product, index) => (
                  <tr key={index}>

                    <td>
                      {product.title ||
                        "-"}
                    </td>

                    <td>
                      {product.price
                        ? `₹${Number(
                            product.price
                          ).toLocaleString(
                            "en-IN"
                          )}`
                        : "-"}
                    </td>

                    <td>
                      {product.requirement_status ||
                        "-"}
                    </td>

                    <td>
                      {product.ram_gb
                        ? `${product.ram_gb} GB`
                        : "-"}
                    </td>

                    <td>
                      {product.gpu ||
                        "-"}
                    </td>

                  </tr>
                )
              )}

          </tbody>

        </table>

      </div>

    </section>
  );
}