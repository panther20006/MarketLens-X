import React from "react";

import SearchBox from "../components/SearchBox";

export default function Home({
  onSearch,
  loading,
}) {
  return (
    <div className="home-page">

      <section className="hero">

        <div className="hero-badge">
          ⚡ AI PRODUCT INTELLIGENCE
        </div>

        <h1>
          Search Smarter.
          <br />

          <span>
            Buy Better.
          </span>
        </h1>

        <p>
          MarketLens X analyzes products,
          prices, requirements and market
          intelligence to help you understand
          the market faster.
        </p>

        <SearchBox
          onSearch={onSearch}
          loading={loading}
        />

      </section>

      <section className="feature-grid">

        <div className="feature-card">
          <div>🔎</div>

          <h3>
            Smart Search
          </h3>

          <p>
            Search products using natural
            language.
          </p>
        </div>

        <div className="feature-card">
          <div>🎯</div>

          <h3>
            Requirement Matching
          </h3>

          <p>
            Check products against your
            requested specifications.
          </p>
        </div>

        <div className="feature-card">
          <div>💰</div>

          <h3>
            Price Intelligence
          </h3>

          <p>
            Analyze product prices and
            budget matches.
          </p>
        </div>

        <div className="feature-card">
          <div>🧠</div>

          <h3>
            Market Insights
          </h3>

          <p>
            Understand product and market
            information quickly.
          </p>
        </div>

      </section>

    </div>
  );
}