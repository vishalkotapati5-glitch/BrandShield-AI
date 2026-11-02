import { ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "./api/client";

type Health = { status: string; version: string };

export default function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api<Health>("/health").then(setHealth).catch((e) => setError(e.message));
  }, []);

  return (
    <main className="min-h-screen bg-navy-900 text-white flex items-center justify-center">
      <div className="rounded-2xl bg-navy-800 p-10 shadow-xl text-center space-y-3">
        <ShieldCheck className="mx-auto text-violet-500" size={48} />
        <h1 className="text-2xl font-semibold">BrandShield AI</h1>
        <p className="text-sm text-slate-300">
          {health ? `API ${health.status} (v${health.version})` : error ? `API unreachable: ${error}` : "Checking API…"}
        </p>
        <p className="text-xs text-slate-400">Stage 0 skeleton. Real pages arrive in later stages.</p>
      </div>
    </main>
  );
}
