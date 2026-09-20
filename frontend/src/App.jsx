import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./app.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

/* =========================================================
   NAVBAR
========================================================= */

function Navbar({ page, setPage }) {
  return (
    <nav className="navbar">

      <div
        className="brand"
        onClick={() => setPage("home")}
      >
        <div className="brand-logo">
          ML
        </div>

        <div className="brand-name">
          MarketLens <span>X</span>
        </div>
      </div>

      <div className="nav-links">

        <button
          className={
            page === "home"
              ? "nav-link active"
              : "nav-link"
          }
          onClick={() => setPage("home")}
        >
          Home
        </button>

        <button
          className={
            page === "dashboard"
              ? "nav-link active"
              : "nav-link"
          }
          onClick={() => setPage("dashboard")}
        >
          Dashboard
        </button>

        <button
          className={
            page === "results"
              ? "nav-link active"
              : "nav-link"
          }
          onClick={() => setPage("results")}
        >
          Results
        </button>

        <button
          className={
            page === "compare"
              ? "nav-link active"
              : "nav-link"
          }
          onClick={() => setPage("compare")}
        >
          Compare
        </button>

      </div>

      <div className="backend-online">
        <span className="online-dot"></span>
        Backend Online
      </div>

    </nav>
  );
}


/* =========================================================
   SEARCH BOX
========================================================= */

function SearchBox({ onSearch, loading }) {

  const [query, setQuery] = useState(
    "16GB RAM laptop under 60000"
  );

  const examples = [
    "Gaming Laptop",
    "16GB RAM",
    "iPhone",
    "RTX 4050"
  ];

  function submitSearch(e) {
    e.preventDefault();

    if (!query.trim() || loading) {
      return;
    }

    onSearch(query.trim());
  }

  function exampleSearch(value) {

    if (loading) {
      return;
    }

    setQuery(value);
    onSearch(value);
  }

  return (
    <div className="search-panel">

      <form
        className="search-box"
        onSubmit={submitSearch}
      >

        <div className="search-icon">
          🔍
        </div>

        <input
          className="search-input"
          type="text"
          value={query}
          onChange={(e) =>
            setQuery(e.target.value)
          }
          placeholder="Search products..."
          disabled={loading}
        />

        <button
          type="submit"
          className="search-button"
          disabled={loading}
        >
          {loading
            ? "Searching..."
            : "Search →"}
        </button>

      </form>

      <div className="try-row">

        <span className="try-label">
          Try:
        </span>

        {examples.map((item) => (
          <button
            key={item}
            type="button"
            className="try-chip"
            onClick={() =>
              exampleSearch(item)
            }
            disabled={loading}
          >
            {item}
          </button>
        ))}

      </div>

    </div>
  );
}


/* =========================================================
   HOME
========================================================= */

function Home({
  onSearch,
  loading
}) {

  const handleFeatureSearch = (query) => {

    if (loading) {
      return;
    }

    onSearch(query);
  };

  const focusSearch = () => {

    const input =
      document.querySelector(
        ".search-input"
      );

    if (input) {
      input.focus();

      input.scrollIntoView({
        behavior: "smooth",
        block: "center"
      });
    }
  };

  return (
    <main className="home-page">

      {/* HERO */}

      <section className="hero">

        <div className="hero-content">

          <h1>
            Search
            <br />
            Smarter.
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

        </div>

        <SearchBox
          onSearch={onSearch}
          loading={loading}
        />

      </section>


      {/* FEATURE CARDS */}

      <section className="features">

        <FeatureCard
          icon="⌕"
          title="Smart Search"
          text="Search products using natural language."
          color="purple"
          onClick={focusSearch}
        />

        <FeatureCard
          icon="◎"
          title="Requirement Matching"
          text="Check products against your requested specifications."
          color="blue"
          onClick={() =>
            handleFeatureSearch(
              "laptop 16GB RAM under 60000"
            )
          }
        />

        <FeatureCard
          icon="▤"
          title="Price Intelligence"
          text="Analyze product prices and budget matches."
          color="cyan"
          onClick={() =>
            handleFeatureSearch(
              "laptop under 60000"
            )
          }
        />

        <FeatureCard
          icon="✦"
          title="Market Insights"
          text="Understand product and market information quickly."
          color="pink"
          onClick={() =>
            handleFeatureSearch(
              "gaming laptop RTX 16GB RAM"
            )
          }
        />

      </section>

    </main>
  );
}


/* =========================================================
   FEATURE CARD
========================================================= */

function FeatureCard({
  icon,
  title,
  text,
  color,
  onClick
}) {

  return (
    <div
      className={`feature-card ${color}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {

        if (
          e.key === "Enter" ||
          e.key === " "
        ) {
          e.preventDefault();
          onClick();
        }

      }}
    >

      <div className="feature-icon">
        {icon}
      </div>

      <div className="feature-content">

        <h3>
          {title}
        </h3>

        <p>
          {text}
        </p>

      </div>

      <div className="feature-arrow">
        →
      </div>

    </div>
  );
}


/* =========================================================
   RESULTS
========================================================= */

function Results({
  data,
  query,
  onBack
}) {

  if (!data) {

    return (
      <main className="page">

        <div className="empty-page">

          <div className="empty-icon">
            🔎
          </div>

          <h2>
            No Search Yet
          </h2>

          <p>
            Go to Home and search for a product.
          </p>

          <button
            className="primary-button"
            onClick={onBack}
          >
            Start Searching
          </button>

        </div>

      </main>
    );
  }

  const results =
    data.results || [];

  return (
    <main className="page">

      {/* PAGE HEADER */}

      <div className="page-top">

        <div className="page-heading">

          <div className="small-label">
            SEARCH RESULTS
          </div>

          <h2>
            {query}
          </h2>

          <p>
            {data.unique_count ||
              results.length}{" "}
            unique products found
          </p>

        </div>

        <button
          className="secondary-button"
          onClick={onBack}
        >
          ← New Search
        </button>

      </div>


      {/* SUMMARY */}

      <div className="result-summary">

        <SummaryBox
          title="Total Found"
          value={
            data.total_found ??
            results.length
          }
        />

        <SummaryBox
          title="Unique"
          value={
            data.unique_count ??
            results.length
          }
        />

        <SummaryBox
          title="Verified"
          value={
            data.market_summary
              ?.verified_matches ?? 0
          }
        />

        <SummaryBox
          title="Needs Verification"
          value={
            data.market_summary
              ?.needs_verification ?? 0
          }
        />

      </div>


      {/* PRODUCTS */}

      <div className="products-grid">

        {results.length === 0 ? (

          <div className="empty-page">

            <div className="empty-icon">
              📦
            </div>

            <h2>
              No Products Found
            </h2>

            <p>
              Try another search query.
            </p>

          </div>

        ) : (

          results.map(
            (product, index) => (

              <ProductCard
                key={
                  product.id ||
                  product.product_id ||
                  index
                }
                product={product}
              />

            )
          )

        )}

      </div>

    </main>
  );
}


/* =========================================================
   SUMMARY BOX
========================================================= */

function SummaryBox({
  title,
  value
}) {

  return (
    <div className="summary-box">

      <span>
        {title}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


/* =========================================================
   PRODUCT CARD
========================================================= */

function ProductCard({
  product
}) {

  const intelligence =
    product.intelligence || {};

  const status =
    intelligence.match_status ||
    product.match_status ||
    "Needs Verification";

  let statusClass =
    "warning";

  if (
    status === "Verified Match"
  ) {
    statusClass = "verified";
  }

  if (
    status === "Does Not Match"
  ) {
    statusClass = "failed";
  }

  const image =
    product.image ||
    product.thumbnail ||
    product.image_url;

  const title =
    product.title ||
    product.name ||
    "Unknown Product";

  const price =
    product.price ??
    product.extracted_price ??
    "Price unavailable";

  return (
    <div className="product-card">

      {/* IMAGE */}

      <div className="product-image">

        {image ? (

          <img
            src={image}
            alt={title}
            loading="lazy"
          />

        ) : (

          <div className="no-image">
            📦
          </div>

        )}

      </div>


      {/* CONTENT */}

      <div className="product-content">

        <div
          className={`status ${statusClass}`}
        >
          {status}
        </div>

        <h3>
          {title}
        </h3>

        <div className="product-price">

          {typeof price === "number"
            ? `₹${price.toLocaleString(
                "en-IN"
              )}`
            : price}

        </div>


        {/* PRODUCT INFO */}

        <div className="product-info">

          <div>
            <span>
              RAM
            </span>

            <strong>
              {product.ram ||
                product.ram_gb ||
                "—"}
            </strong>
          </div>


          <div>
            <span>
              GPU
            </span>

            <strong>
              {product.gpu ||
                "—"}
            </strong>
          </div>


          <div>
            <span>
              Storage
            </span>

            <strong>
              {product.storage ||
                product.storage_gb ||
                "—"}
            </strong>
          </div>


          <div>
            <span>
              Source
            </span>

            <strong>
              {product.source ||
                "Shopping"}
            </strong>
          </div>

        </div>


        {/* PRODUCT LINK */}

        {product.product_link && (

          <a
            className="product-button"
            href={product.product_link}
            target="_blank"
            rel="noreferrer"
          >
            View Product →
          </a>

        )}

      </div>

    </div>
  );
}


/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard({
  data
}) {

  return (
    <main className="page">

      <div className="page-title">

        <div className="small-label">
          MARKETLENS X
        </div>

        <h2>
          Dashboard
        </h2>

        <p>
          Product search intelligence overview.
        </p>

      </div>


      {/* DASHBOARD CARDS */}

      <div className="dashboard-grid">

        <DashboardCard
          icon="🔎"
          title="Searches"
          value={
            data ? "1" : "0"
          }
        />

        <DashboardCard
          icon="📦"
          title="Products"
          value={
            data?.unique_count ||
            "0"
          }
        />

        <DashboardCard
          icon="✓"
          title="Verified"
          value={
            data?.market_summary
              ?.verified_matches ||
            "0"
          }
        />

        <DashboardCard
          icon="₹"
          title="Budget Matches"
          value={
            data?.market_summary
              ?.budget_products ||
            "0"
          }
        />

      </div>


      {/* WORKFLOW */}

      <div className="dashboard-panel">

        <h3>
          How MarketLens X works
        </h3>

        <div className="workflow">

          <Workflow
            number="01"
            title="Search"
            text="Enter a natural language product requirement."
          />

          <Workflow
            number="02"
            title="Analyze"
            text="MarketLens processes products and specifications."
          />

          <Workflow
            number="03"
            title="Compare"
            text="Compare prices, requirements and product quality."
          />

          <Workflow
            number="04"
            title="Decide"
            text="Get useful market intelligence before buying."
          />

        </div>

      </div>

    </main>
  );
}


/* =========================================================
   DASHBOARD CARD
========================================================= */

function DashboardCard({
  icon,
  title,
  value
}) {

  return (
    <div className="dashboard-card">

      <div className="dashboard-icon">
        {icon}
      </div>

      <span>
        {title}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


/* =========================================================
   WORKFLOW
========================================================= */

function Workflow({
  number,
  title,
  text
}) {

  return (
    <div className="workflow-card">

      <div className="workflow-number">
        {number}
      </div>

      <h4>
        {title}
      </h4>

      <p>
        {text}
      </p>

    </div>
  );
}


/* =========================================================
   COMPARE
========================================================= */

function Compare({
  data
}) {

  const products =
    data?.results?.slice(0, 4) || [];

  return (
    <main className="page">

      <div className="page-title">

        <div className="small-label">
          PRODUCT INTELLIGENCE
        </div>

        <h2>
          Compare Products
        </h2>

        <p>
          Compare products returned from
          your latest search.
        </p>

      </div>


      {products.length === 0 ? (

        <div className="empty-page">

          <div className="empty-icon">
            ⚖️
          </div>

          <h2>
            Nothing to Compare
          </h2>

          <p>
            Search for products first.
          </p>

        </div>

      ) : (

        <div className="compare-table-wrapper">

          <table>

            <thead>

              <tr>

                <th>
                  Specification
                </th>

                {products.map(
                  (product, index) => (

                    <th key={index}>

                      {(
                        product.title ||
                        "Product"
                      ).slice(0, 30)}

                    </th>

                  )
                )}

              </tr>

            </thead>


            <tbody>

              {/* PRICE */}

              <tr>

                <td>
                  Price
                </td>

                {products.map(
                  (p, i) => (

                    <td key={i}>

                      {p.price ||
                        p.extracted_price ||
                        "—"}

                    </td>

                  )
                )}

              </tr>


              {/* RAM */}

              <tr>

                <td>
                  RAM
                </td>

                {products.map(
                  (p, i) => (

                    <td key={i}>

                      {p.ram ||
                        p.ram_gb ||
                        "—"}

                    </td>

                  )
                )}

              </tr>


              {/* GPU */}

              <tr>

                <td>
                  GPU
                </td>

                {products.map(
                  (p, i) => (

                    <td key={i}>

                      {p.gpu ||
                        "—"}

                    </td>

                  )
                )}

              </tr>


              {/* STORAGE */}

              <tr>

                <td>
                  Storage
                </td>

                {products.map(
                  (p, i) => (

                    <td key={i}>

                      {p.storage ||
                        p.storage_gb ||
                        "—"}

                    </td>

                  )
                )}

              </tr>


              {/* STATUS */}

              <tr>

                <td>
                  Match Status
                </td>

                {products.map(
                  (p, i) => (

                    <td key={i}>

                      {p.intelligence
                        ?.match_status ||
                        p.match_status ||
                        "Needs Verification"}

                    </td>

                  )
                )}

              </tr>

            </tbody>

          </table>

        </div>

      )}

    </main>
  );
}


/* =========================================================
   APP
========================================================= */

function App() {

  const [page, setPage] =
    useState("home");

  const [loading, setLoading] =
    useState(false);

  const [data, setData] =
    useState(null);

  const [query, setQuery] =
    useState("");


  /* =======================================================
     SEARCH API
  ======================================================= */

  async function handleSearch(
    searchQuery
  ) {

    if (
      !searchQuery ||
      !searchQuery.trim()
    ) {
      return;
    }

    setLoading(true);

    setQuery(
      searchQuery.trim()
    );

    try {

      const response =
        await fetch(
          `${API_URL}/api/search`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
              query:
                searchQuery.trim()
            })
          }
        );


      const result =
        await response.json();


      if (!response.ok) {

        throw new Error(
          result.error ||
          result.message ||
          "Search request failed"
        );

      }


      setData(result);

      setPage("results");


      /* Scroll to top */

      setTimeout(() => {

        window.scrollTo({
          top: 0,
          behavior: "smooth"
        });

      }, 50);


    } catch (error) {

      console.error(
        "MarketLens Search Error:",
        error
      );

      alert(
        `Search failed: ${error.message}`
      );


    } finally {

      setLoading(false);

    }
  }


  /* =======================================================
     RENDER
  ======================================================= */

  return (
    <div className="app">

      <Navbar
        page={page}
        setPage={setPage}
      />


      {/* HOME */}

      {page === "home" && (

        <Home
          onSearch={handleSearch}
          loading={loading}
        />

      )}


      {/* RESULTS */}

      {page === "results" && (

        <Results
          data={data}
          query={query}
          onBack={() =>
            setPage("home")
          }
        />

      )}


      {/* DASHBOARD */}

      {page === "dashboard" && (

        <Dashboard
          data={data}
        />

      )}


      {/* COMPARE */}

      {page === "compare" && (

        <Compare
          data={data}
        />

      )}

    </div>
  );
}


/* =========================================================
   RENDER
========================================================= */

createRoot(
  document.getElementById("root")
).render(

  <React.StrictMode>

    <App />

  </React.StrictMode>

);