"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import Link from "next/link";
import AuthGuard from "@/components/AuthGuard";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import Alert from "@/components/ui/Alert";
import AnalyticsCharts from "@/components/AnalyticsCharts";

type Item = {
  id: number;
  created_at: string;
  duration_seconds?: number | null;
  transcript_preview: string;
};

export default function Dashboard() {
  const [items, setItems] = useState<Item[]>([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await apiFetch("/training/sessions");
        setItems(data);
      } catch (e: any) {
        setErr(e.message);
      }
    })();
  }, []);

  return (
    <AuthGuard>
      <div className="grid gap-6">
        <Card>
          <CardHeader
            title="Dashboard"
            subtitle="Your recent training sessions."
          />
          <CardContent className="flex items-center justify-between">
            <div className="text-sm text-zinc-600">
              Practice consistently. You will see improvements in pacing and
              clarity.
            </div>
            <Link href="/practice">
              <Button>New practice</Button>
            </Link>
          </CardContent>
        </Card>

        {err ? <Alert kind="error">{err}</Alert> : null}

        <div className="grid gap-3">
          {items.map((x) => (
            <Link key={x.id} href={`/sessions/${x.id}`}>
              <div className="rounded-2xl border border-zinc-200 bg-white px-5 py-4 shadow-soft transition hover:-translate-y-0.5 hover:shadow-md">
                <div className="flex items-center justify-between gap-3">
                  <div className="font-semibold text-zinc-900">
                    Session {x.id}
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge tone="brand">
                      {new Date(x.created_at).toLocaleString()}
                    </Badge>
                    <Badge tone="success">
                      {x.duration_seconds?.toFixed(1) ?? "?"}s
                    </Badge>
                  </div>
                </div>
                <div className="mt-2 text-sm text-zinc-600 line-clamp-2">
                  {x.transcript_preview || "No transcript preview"}
                </div>
              </div>
            </Link>
          ))}
          {items.length === 0 ? (
            <div className="rounded-2xl border border-zinc-200 bg-white p-6 text-sm text-zinc-600">
              No sessions yet. Start your first practice.
            </div>
          ) : null}
        </div>
      </div>
    </AuthGuard>
  );
}
