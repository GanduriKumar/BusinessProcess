import { useEffect, useState } from "react";

import { fetchHealth } from "./api/health";

function App() {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    fetchHealth()
      .then((data) => setStatus(data.status || "unknown"))
      .catch(() => setStatus("unreachable"));
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-brand-50 to-white px-6 py-12">
      <div className="mx-auto max-w-4xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-semibold uppercase tracking-wide text-brand-700">Business Process</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900">React Frontend + FastAPI Backend</h1>
        <p className="mt-4 text-slate-600">
          Frontend scaffolded with Vite and Tailwind CSS. Backend health status is shown below.
        </p>

        <div className="mt-8 inline-flex items-center gap-2 rounded-full border border-slate-300 bg-slate-50 px-4 py-2">
          <span className="h-2.5 w-2.5 rounded-full bg-brand-500" />
          <span className="text-sm font-medium text-slate-700">API Status: {status}</span>
        </div>
      </div>
    </main>
  );
}

export default App;
