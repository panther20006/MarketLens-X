import React from "react";

export default function Dashboard({
  data,
  onNewSearch,
}) {
  return (
    <div className="dashboard-page">

      <section className="dashboard-hero">

        <div>

          <span className="small-label">
            MARKETLENS X
          </span>

          <h1>
            Product Intelligence
          </h1>

          <p>
            Search and analyze products using
            market data.
          </p>

        </div>

        <button
          className="primary-button"
          onClick={onNewSearch}
        >
          New Search
        </button>

      </section>

      {data ? (
        <div className="dashboard-summary">

          <div>
            <span>
              Last Search
            </span>

            <strong>
              {data.query}
            </strong>
          </div>

          <div>
            <span>
              Products
            </span>

            <strong>
              {data.unique_count}
            </strong>
          </div>

          <div>
            <span>
              Verified
            </span>

            <strong>
              {data.market_summary
                ?.verified_matches ?? 0}
            </strong>
          </div>

        </div>
      ) : (
        <div className="empty-dashboard">

          <div>
            🚀
          </div>

          <h2>
            Start your first search
          </h2>

          <p>
            Search laptops, phones,
            electronics and more.
          </p>

          <button
            className="primary-button"
            onClick={onNewSearch}
          >
            Start Searching
          </button>

        </div>
      )}

    </div>
  );
}