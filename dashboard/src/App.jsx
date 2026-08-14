import { useEffect, useState } from "react";

import {
  getOverview,
  getRevenue,
  getPaymentStats,
  getRiskDistribution,
  getRecentActivity,
  getFraudAlerts,
} from "./services/api";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
} from "recharts";

import "./App.css";


function App() {
  const [overview, setOverview] = useState({});
  const [revenue, setRevenue] = useState([]);
  const [payments, setPayments] = useState({});
  const [risk, setRisk] = useState([]);
  const [activity, setActivity] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


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

      setError(null);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to FluxGuard API.");
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
      <div className="center">
        Loading FluxGuard...
      </div>
    );
  }


  return (
    <div className="app">

      <header>
        <div>
          <h1>FluxGuard</h1>
          <p>
            Real-Time E-Commerce Analytics &
            Fraud Detection
          </p>
        </div>

        <span className="live">
          ● SYSTEM LIVE
        </span>
      </header>


      {error && (
        <div className="error">
          {error}
        </div>
      )}


      <section className="cards">

        <Card
          title="Total Revenue"
          value={`$${Number(
            overview.total_revenue || 0
          ).toLocaleString()}`}
        />

        <Card
          title="Transactions"
          value={
            overview.total_transactions || 0
          }
        />

        <Card
          title="Fraud Alerts"
          value={overview.fraud_alerts || 0}
        />

        <Card
          title="Blocked"
          value={overview.blocked || 0}
        />

      </section>


      <section className="charts">

        <div className="panel">

          <h2>Revenue Trend</h2>

          <ResponsiveContainer
            width="100%"
            height={280}
          >
            <LineChart data={revenue}>

              <XAxis
                dataKey="hour"
                hide
              />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="revenue"
              />

            </LineChart>
          </ResponsiveContainer>

        </div>


        <div className="panel">

          <h2>Risk Distribution</h2>

          <ResponsiveContainer
            width="100%"
            height={280}
          >
            <PieChart>

              <Pie
                data={risk}
                dataKey="count"
                nameKey="risk_level"
                outerRadius={100}
                label
              />

              <Tooltip />

            </PieChart>
          </ResponsiveContainer>

        </div>

      </section>


      <section className="panel">

        <h2>Payment Performance</h2>

        <div className="payment-stats">

          <span>
            Successful:
            {" "}
            {payments.successful || 0}
          </span>

          <span>
            Failed:
            {" "}
            {payments.failed || 0}
          </span>

          <span>
            Success Rate:
            {" "}
            {payments.success_rate || 0}%
          </span>

        </div>

      </section>


      <section className="panel">

        <h2>Live Transactions</h2>

        <div className="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>Order</th>
                <th>Customer</th>
                <th>Amount</th>
                <th>Payment</th>
                <th>ML Probability</th>
                <th>Risk</th>
                <th>Decision</th>
              </tr>
            </thead>

            <tbody>

              {activity.map((item) => (

                <tr key={item.event_id}>

                  <td>{item.order_id}</td>

                  <td>{item.customer_id}</td>

                  <td>
                    $
                    {Number(
                      item.amount || 0
                    ).toFixed(2)}
                  </td>

                  <td>{item.event_type}</td>

                  <td>
                    {item.ml_probability != null
                      ? Number(
                          item.ml_probability
                        ).toFixed(3)
                      : "-"
                    }
                  </td>

                  <td>
                    {item.final_risk || "-"}
                  </td>

                  <td>
                    {item.final_decision || "-"}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </section>


      <section className="panel">

        <h2>Fraud Alerts</h2>

        {alerts.length === 0 ? (

          <p>No active fraud alerts.</p>

        ) : (

          alerts.map((alert) => (

            <div
              className="alert"
              key={alert.id}
            >

              <strong>
                {alert.order_id}
              </strong>

              <span>
                ${Number(
                  alert.amount || 0
                ).toFixed(2)}
              </span>

              <span>
                {alert.risk_level}
              </span>

              <span>
                {alert.decision}
              </span>

            </div>

          ))

        )}

      </section>

    </div>
  );
}


function Card({ title, value }) {
  return (
    <div className="card">
      <p>{title}</p>
      <h2>{value}</h2>
    </div>
  );
}


export default App;