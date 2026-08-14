import { useEffect, useState } from "react";

import {
  getOverview,
  getRevenue,
  getPaymentStats,
  getRiskDistribution,
  getRecentActivity,
  getFraudAlerts,
} from "./services/api.js";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import "./App.css";


const RISK_COLORS = {
  LOW: "#22c55e",
  MEDIUM: "#f59e0b",
  HIGH: "#ef4444",
};


function App() {
  const [overview, setOverview] = useState({});
  const [revenue, setRevenue] = useState([]);
  const [payments, setPayments] = useState({});
  const [risk, setRisk] = useState([]);
  const [activity, setActivity] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);


  async function loadDashboard() {
    try {
      const [
        overviewData,
        revenueData,
        paymentData,
        riskData,
        activityData,
        alertData,
      ] = await Promise.all([
        getOverview(),
        getRevenue(),
        getPaymentStats(),
        getRiskDistribution(),
        getRecentActivity(),
        getFraudAlerts(),
      ]);

      setOverview(overviewData);
      setRevenue([...revenueData].reverse());
      setPayments(paymentData);
      setRisk(riskData);
      setActivity(activityData);
      setAlerts(alertData);

      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to the FluxGuard API."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadDashboard();

    const interval = setInterval(
      loadDashboard,
      5000
    );

    return () => clearInterval(interval);
  }, []);


  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loader" />

        <h2>FluxGuard</h2>

        <p>Loading fraud intelligence...</p>
      </div>
    );
  }


  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div>
          <div className="brand">
            <div className="logo">FG</div>

            <div>
              <h1>FluxGuard</h1>

              <p>
                Real-Time E-Commerce Fraud Intelligence
              </p>
            </div>
          </div>
        </div>


        <div className="system-status">

          <div className="live-status">
            <span className="live-dot" />
            SYSTEM LIVE
          </div>

          {lastUpdated && (
            <small>
              Updated{" "}
              {lastUpdated.toLocaleTimeString()}
            </small>
          )}

        </div>

      </header>


      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}


      {/* KPI CARDS */}

      <section className="kpi-grid">

        <MetricCard
          label="TOTAL REVENUE"
          value={formatCurrency(
            overview.total_revenue
          )}
          detail="Completed payments"
        />

        <MetricCard
          label="TRANSACTIONS"
          value={formatNumber(
            overview.total_transactions
          )}
          detail="Processed events"
        />

        <MetricCard
          label="FRAUD ALERTS"
          value={formatNumber(
            overview.fraud_alerts
          )}
          detail="Requires attention"
          variant="warning"
        />

        <MetricCard
          label="BLOCKED"
          value={formatNumber(
            overview.blocked
          )}
          detail="High-risk transactions"
          variant="danger"
        />

      </section>


      {/* CHARTS */}

      <section className="chart-grid">

        <div className="panel chart-panel">

          <PanelHeader
            title="Revenue Trend"
            subtitle="Completed payment volume"
          />

          <ResponsiveContainer
            width="100%"
            height={300}
          >
            <LineChart data={revenue}>

              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#263247"
              />

              <XAxis
                dataKey="hour"
                tickFormatter={formatHour}
                stroke="#718096"
                tick={{
                  fill: "#718096",
                  fontSize: 11,
                }}
              />

              <YAxis
                stroke="#718096"
                tick={{
                  fill: "#718096",
                  fontSize: 11,
                }}
                tickFormatter={(value) =>
                  `$${value}`
                }
              />

              <Tooltip
                contentStyle={{
                  background: "#111827",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                }}
                formatter={(value) => [
                  formatCurrency(value),
                  "Revenue",
                ]}
              />

              <Line
                type="monotone"
                dataKey="revenue"
                stroke="#38bdf8"
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 5 }}
              />

            </LineChart>
          </ResponsiveContainer>

        </div>


        <div className="panel chart-panel">

          <PanelHeader
            title="Risk Distribution"
            subtitle="Hybrid fraud classifications"
          />

          {risk.length > 0 ? (

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <PieChart>

                <Pie
                  data={risk}
                  dataKey="count"
                  nameKey="risk_level"
                  innerRadius={65}
                  outerRadius={100}
                  paddingAngle={4}
                >

                  {risk.map((item) => (
                    <Cell
                      key={item.risk_level}
                      fill={
                        RISK_COLORS[
                          item.risk_level
                        ] || "#64748b"
                      }
                    />
                  ))}

                </Pie>

                <Tooltip
                  contentStyle={{
                    background: "#111827",
                    border:
                      "1px solid #334155",
                    borderRadius: "8px",
                  }}
                />

              </PieChart>
            </ResponsiveContainer>

          ) : (
            <EmptyState text="No risk data yet" />
          )}


          <div className="risk-legend">

            {["LOW", "MEDIUM", "HIGH"].map(
              (level) => {

                const item = risk.find(
                  (entry) =>
                    entry.risk_level === level
                );

                return (
                  <div
                    className="legend-item"
                    key={level}
                  >
                    <span
                      className="legend-dot"
                      style={{
                        background:
                          RISK_COLORS[level],
                      }}
                    />

                    <span>{level}</span>

                    <strong>
                      {item?.count || 0}
                    </strong>
                  </div>
                );
              }
            )}

          </div>

        </div>

      </section>


      {/* PAYMENT HEALTH */}

      <section className="panel">

        <PanelHeader
          title="Payment Health"
          subtitle="Current payment processing performance"
        />

        <div className="payment-grid">

          <PaymentMetric
            label="Successful"
            value={payments.successful || 0}
          />

          <PaymentMetric
            label="Failed"
            value={payments.failed || 0}
          />

          <PaymentMetric
            label="Success Rate"
            value={`${payments.success_rate || 0}%`}
          />

          <PaymentMetric
            label="Failure Rate"
            value={`${payments.failure_rate || 0}%`}
          />

        </div>

      </section>


      {/* LIVE TRANSACTIONS */}

      <section className="panel">

        <PanelHeader
          title="Live Transactions"
          subtitle="Latest events processed by FluxGuard"
          live
        />

        <div className="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>ORDER</th>
                <th>CUSTOMER</th>
                <th>AMOUNT</th>
                <th>PAYMENT</th>
                <th>ML PROBABILITY</th>
                <th>RISK</th>
                <th>DECISION</th>
                <th>TIME</th>
              </tr>
            </thead>

            <tbody>

              {activity.length === 0 ? (

                <tr>
                  <td
                    colSpan="8"
                    className="empty-row"
                  >
                    Waiting for transactions...
                  </td>
                </tr>

              ) : (

                activity.map((item) => (

                  <tr key={item.event_id}>

                    <td className="order-id">
                      {item.order_id}
                    </td>

                    <td>
                      {item.customer_id}
                    </td>

                    <td className="amount">
                      {formatCurrency(
                        item.amount
                      )}
                    </td>

                    <td>
                      <PaymentBadge
                        type={item.event_type}
                      />
                    </td>

                    <td>
                      <ProbabilityBar
                        value={
                          item.ml_probability
                        }
                      />
                    </td>

                    <td>
                      <RiskBadge
                        risk={item.final_risk}
                      />
                    </td>

                    <td>
                      <DecisionBadge
                        decision={
                          item.final_decision
                        }
                      />
                    </td>

                    <td className="timestamp">
                      {formatTime(
                        item.event_timestamp
                      )}
                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </section>


      {/* FRAUD ALERTS */}

      <section className="panel">

        <PanelHeader
          title="Recent Fraud Alerts"
          subtitle="Transactions requiring investigation"
        />

        {alerts.length === 0 ? (

          <EmptyState
            text="No active fraud alerts"
          />

        ) : (

          <div className="alert-list">

            {alerts.map((alert) => (

              <div
                className="fraud-alert"
                key={alert.id}
              >

                <div className="alert-main">

                  <div
                    className={`alert-icon ${
                      alert.risk_level
                        ?.toLowerCase() || ""
                    }`}
                  >
                    !
                  </div>

                  <div>
                    <strong>
                      {alert.order_id}
                    </strong>

                    <p>
                      Customer{" "}
                      {alert.customer_id}
                    </p>
                  </div>

                </div>


                <div className="alert-amount">
                  {formatCurrency(
                    alert.amount
                  )}
                </div>


                <RiskBadge
                  risk={alert.risk_level}
                />


                <DecisionBadge
                  decision={alert.decision}
                />

              </div>

            ))}

          </div>

        )}

      </section>


      <footer>

        <span>
          FluxGuard v1.0
        </span>

        <span>
          Kafka • Spark • PyTorch • PostgreSQL • FastAPI
        </span>

      </footer>

    </div>
  );
}


/* ========================================================
   COMPONENTS
======================================================== */


function MetricCard({
  label,
  value,
  detail,
  variant = "",
}) {
  return (
    <div className={`metric-card ${variant}`}>

      <span className="metric-label">
        {label}
      </span>

      <strong className="metric-value">
        {value}
      </strong>

      <span className="metric-detail">
        {detail}
      </span>

    </div>
  );
}


function PanelHeader({
  title,
  subtitle,
  live = false,
}) {
  return (
    <div className="panel-header">

      <div>
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>

      {live && (
        <span className="live-pill">
          <span className="live-dot" />
          LIVE
        </span>
      )}

    </div>
  );
}


function PaymentMetric({
  label,
  value,
}) {
  return (
    <div className="payment-metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}


function RiskBadge({ risk }) {
  if (!risk) {
    return (
      <span className="badge neutral">
        -
      </span>
    );
  }

  return (
    <span
      className={`badge risk-${risk.toLowerCase()}`}
    >
      {risk}
    </span>
  );
}


function DecisionBadge({ decision }) {
  if (!decision) {
    return (
      <span className="badge neutral">
        -
      </span>
    );
  }

  return (
    <span
      className={`badge decision-${decision.toLowerCase()}`}
    >
      {decision}
    </span>
  );
}


function PaymentBadge({ type }) {
  const success =
    type === "payment_completed";

  return (
    <span
      className={
        success
          ? "payment-status success"
          : "payment-status failed"
      }
    >
      {success ? "COMPLETED" : "FAILED"}
    </span>
  );
}


function ProbabilityBar({ value }) {
  if (value == null) {
    return <span>-</span>;
  }

  const probability = Number(value);

  const percentage =
    Math.min(
      Math.max(probability * 100, 0),
      100
    );

  return (
    <div className="probability">

      <span>
        {probability.toFixed(3)}
      </span>

      <div className="probability-track">
        <div
          className="probability-fill"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>

    </div>
  );
}


function EmptyState({ text }) {
  return (
    <div className="empty-state">
      {text}
    </div>
  );
}


/* ========================================================
   FORMATTERS
======================================================== */


function formatCurrency(value) {
  return new Intl.NumberFormat(
    "en-US",
    {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 2,
    }
  ).format(Number(value || 0));
}


function formatNumber(value) {
  return Number(
    value || 0
  ).toLocaleString();
}


function formatTime(value) {
  if (!value) {
    return "-";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "-";
  }

  return date.toLocaleTimeString(
    [],
    {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }
  );
}


function formatHour(value) {
  if (!value) {
    return "";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleTimeString(
    [],
    {
      hour: "numeric",
    }
  );
}


export default App;