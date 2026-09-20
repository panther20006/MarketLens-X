import React, { useState } from "react";

export default function SearchBox({
  onSearch,
  loading,
}) {
  const [query, setQuery] = useState("");

  const submit = (e) => {
    e.preventDefault();

    if (!query.trim() || loading) {
      return;
    }

    onSearch(query.trim());
  };

  const quickSearch = (value) => {
    setQuery(value);
    onSearch(value);
  };

  return (
    <div className="search-section">

      <form
        className="search-box"
        onSubmit={submit}
      >

        <div className="search-icon">
          🔍
        </div>

        <input
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
          placeholder="Search products, e.g. RTX laptop under ₹80,000..."
          disabled={loading}
        />

        <button
          type="submit"
          disabled={
            loading || !query.trim()
          }
        >
          {loading ? "Searching..." : "Search"}
        </button>

      </form>

      <div className="quick-searches">

        <span>Try:</span>

        <button
          onClick={() =>
            quickSearch(
              "gaming laptop under 70000"
            )
          }
        >
          Gaming Laptop
        </button>

        <button
          onClick={() =>
            quickSearch(
              "16GB RAM laptop under 60000"
            )
          }
        >
          16GB RAM
        </button>

        <button
          onClick={() =>
            quickSearch(
              "iPhone under 80000"
            )
          }
        >
          iPhone
        </button>

        <button
          onClick={() =>
            quickSearch(
              "laptop RTX 4050 under 100000"
            )
          }
        >
          RTX 4050
        </button>

      </div>

    </div>
  );
}