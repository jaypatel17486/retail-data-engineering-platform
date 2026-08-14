const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

async function request(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(`FluxGuard API error: ${response.status}`);
  }

  return response.json();
}

export function getOverview() {
  return request("/analytics/overview");
}

export function getRevenue() {
  return request("/analytics/revenue");
}

export function getPaymentStats() {
  return request("/analytics/payments");
}

export function getRiskDistribution() {
  return request("/analytics/risk-distribution");
}

export function getRecentActivity() {
  return request("/analytics/recent-activity?limit=20");
}

export function getFraudAlerts() {
  return request("/fraud/alerts?limit=10");
}
