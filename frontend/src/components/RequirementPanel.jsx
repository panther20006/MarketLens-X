import React from "react";

export default function RequirementPanel({
  requirements,
}) {
  if (!requirements) {
    return null;
  }

  const entries =
    Object.entries(requirements);

  return (
    <section className="requirement-panel">

      <div className="panel-heading">
        <div>
          <span className="panel-icon">
            🎯
          </span>

          <h3>
            Your Requirements
          </h3>
        </div>
      </div>

      <div className="requirements-grid">

        {entries.map(
          ([key, value]) => {

            if (
              value === null ||
              value === undefined ||
              value === ""
            ) {
              return null;
            }

            const label = key
              .replaceAll("_", " ")
              .replace(
                /\b\w/g,
                (letter) =>
                  letter.toUpperCase()
              );

            return (
              <div
                className="requirement-item"
                key={key}
              >
                <span>{label}</span>

                <strong>
                  {String(value)}
                </strong>
              </div>
            );
          }
        )}

      </div>

    </section>
  );
}