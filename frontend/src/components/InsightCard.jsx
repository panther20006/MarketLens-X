import React from "react";

export default function InsightCard({
  summary,
}) {
  if (!summary) {
    return null;
  }

  let text = "";

  if (typeof summary === "string") {
    text = summary;
  } else {
    const parts = [];

    if (
      summary.average_price !==
      undefined
    ) {
      parts.push(
        `Average price: ₹${Number(
          summary.average_price
        ).toLocaleString("en-IN")}`
      );
    }

    if (
      summary.budget_products !==
      undefined
    ) {
      parts.push(
        `Within budget: ${summary.budget_products}`
      );
    }

    if (
      summary.verified_matches !==
      undefined
    ) {
      parts.push(
        `Verified matches: ${summary.verified_matches}`
      );
    }

    if (
      summary.needs_verification !==
      undefined
    ) {
      parts.push(
        `Needs verification: ${summary.needs_verification}`
      );
    }

    if (
      summary.failed_matches !==
      undefined
    ) {
      parts.push(
        `Does not match: ${summary.failed_matches}`
      );
    }

    text =
      parts.join(" • ") ||
      "Market analysis is available.";
  }

  return (
    <section className="insight-card">

      <div className="insight-icon">
        🧠
      </div>

      <div>
        <h3>
          Market Intelligence
        </h3>

        <p>{text}</p>
      </div>

    </section>
  );
}