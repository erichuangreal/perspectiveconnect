"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import AuthGuard from "@/components/AuthGuard";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";

export default function SessionDetail({ params }: { params: { id: string } }) {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const d = await apiFetch(`/training/sessions/${params.id}`);
        setData(d);
      } catch (e: any) {
        setErr(e.message);
      }
    })();
  }, [params.id]);

  return (
    <AuthGuard>
      <div className="grid gap-6">
        {err ? (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {err}
          </div>
        ) : null}

        {!data ? (
          <div className="rounded-2xl border border-zinc-200 bg-white p-6 text-sm text-zinc-600">
            Loading...
          </div>
        ) : (
          <>
            <Card>
              <CardHeader
                title={`Session ${data.id}`}
                subtitle="Full transcript, coaching, and measured features."
              />
              <CardContent className="flex flex-wrap items-center gap-2">
                <Badge>{new Date(data.created_at).toLocaleString()}</Badge>
                <Badge>{data.duration_seconds?.toFixed(1) ?? "?"}s</Badge>
              </CardContent>
            </Card>

            <Card>
              <CardHeader title="Transcript" />
              <CardContent>
                <pre className="whitespace-pre-wrap text-sm text-zinc-800">
                  {data.transcript}
                </pre>
              </CardContent>
            </Card>

            <Card>
              <CardHeader title="Feedback" />
              <CardContent>
                <pre className="whitespace-pre-wrap text-sm text-zinc-800">
                  {data.feedback}
                </pre>
              </CardContent>
            </Card>

            <Card>
              <CardHeader
                title="Voice features"
                subtitle="Raw metrics stored for progress tracking."
              />
              <CardContent>
                <pre className="whitespace-pre-wrap text-xs text-zinc-700">
                  {JSON.stringify(data.voice_features, null, 2)}
                </pre>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </AuthGuard>
  );
}
