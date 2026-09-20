const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

export async function searchProducts(query) {
  if (!query || !query.trim()) {
    throw new Error("Please enter a search query.");
  }

  const response = await fetch(`${API_BASE_URL}/api/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query.trim(),
    }),
  });

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error("Backend returned invalid JSON.");
  }

  if (!response.ok) {
    throw new Error(
      data?.error ||
        data?.message ||
        `Server error: ${response.status}`
    );
  }

  if (!data.success) {
    throw new Error(
      data?.error ||
        data?.message ||
        "Search failed."
    );
  }

  return data;
}

export async function checkBackendHealth() {
  const response = await fetch(
    `${API_BASE_URL}/api/health`
  );

  if (!response.ok) {
    throw new Error("Backend is not reachable.");
  }

  return response.json();
}