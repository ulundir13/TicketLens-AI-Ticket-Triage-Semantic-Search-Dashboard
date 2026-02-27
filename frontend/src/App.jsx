import { useEffect, useState } from "react";

export default function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [tickets, setTickets] = useState([]);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  async function loadTickets() {
    const res = await fetch("/api/tickets");
    const data = await res.json();
    setTickets(data);
  }

  useEffect(() => {
    loadTickets();
  }, []);

  async function createTicket(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/tickets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description }),
      });
      if (!res.ok) throw new Error("Failed to create ticket");
      setTitle("");
      setDescription("");
      await loadTickets();
    } finally {
      setLoading(false);
    }
  }

  async function searchTickets(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!res.ok) throw new Error("Search failed");
      const data = await res.json();
      setResults(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ fontFamily: "system-ui", maxWidth: 900, margin: "0 auto", padding: 24 }}>
      <h1>TicketLens</h1>
      <p>AI Ticket Triage + Semantic Search (FastAPI + Sentence Transformers + FAISS)</p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <section style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
          <h2>Create Ticket</h2>
          <form onSubmit={createTicket}>
            <label>Title</label>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              style={{ width: "100%", padding: 8, marginTop: 6, marginBottom: 10 }}
              placeholder="Internet down at site A"
            />

            <label>Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              style={{ width: "100%", padding: 8, marginTop: 6, minHeight: 90 }}
              placeholder="Describe the issue..."
            />

            <button
              disabled={loading}
              style={{ marginTop: 12, padding: "10px 14px", cursor: "pointer" }}
              type="submit"
            >
              {loading ? "Working..." : "Submit"}
            </button>
          </form>
        </section>

        <section style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
          <h2>Semantic Search</h2>
          <form onSubmit={searchTickets}>
            <label>Query</label>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{ width: "100%", padding: 8, marginTop: 6 }}
              placeholder="network connectivity outage"
            />
            <button
              disabled={loading}
              style={{ marginTop: 12, padding: "10px 14px", cursor: "pointer" }}
              type="submit"
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </form>

          <div style={{ marginTop: 14 }}>
            <h3>Results</h3>
            {results.length === 0 ? (
              <p style={{ color: "#666" }}>No results yet.</p>
            ) : (
              <ul>
                {results.map((r, idx) => (
                  <li key={idx} style={{ marginBottom: 10 }}>
                    <strong>{r.ticket.title}</strong>
                    <div style={{ color: "#666" }}>
                      Score: {r.score.toFixed(4)}
                    </div>
                    <div>{r.ticket.description}</div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      </div>

      <section style={{ marginTop: 20, border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
        <h2>Tickets</h2>
        {tickets.length === 0 ? (
          <p style={{ color: "#666" }}>No tickets yet.</p>
        ) : (
          <ul>
            {tickets.map((t) => (
              <li key={t.id} style={{ marginBottom: 10 }}>
                <strong>#{t.id} — {t.title}</strong>
                <div style={{ color: "#666" }}>{t.created_at}</div>
                <div>{t.description}</div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
