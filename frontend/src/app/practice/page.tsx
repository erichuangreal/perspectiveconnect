"use client";

import { useState } from "react";
import AudioRecorder from "@/components/AudioRecorder";
import { apiFetch } from "@/lib/api";
import { useRouter } from "next/navigation";
import AuthGuard from "@/components/AuthGuard";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";

export default function Practice() {
  const [blob, setBlob] = useState<Blob | null>(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  const [goal, setGoal] = useState("inform");
  const [audience, setAudience] = useState("classmates or interviewers");
  const [timeLimit, setTimeLimit] = useState(180);
  const [rubric, setRubric] = useState(
    "clarity, structure, technical accuracy, examples, pacing, confidence",
  );

  const router = useRouter();

  async function submit() {
    if (!blob) return;
    setErr("");
    setLoading(true);
    try {
      const form = new FormData();
      form.append("audio_file", blob, "recording.webm");
      form.append("goal", goal);
      form.append("audience", audience);
      form.append("time_limit_seconds", String(timeLimit));
      form.append("rubric", rubric);

      const data = await apiFetch("/training/submit", {
        method: "POST",
        body: form,
      });
      router.push(`/sessions/${data.session_id}`);
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthGuard>
      <div className="grid gap-6">
        <Card>
          <CardHeader
            title="Practice"
            subtitle="Record your presentation and submit it for coaching."
          />
          <CardContent className="grid gap-5">
            <AudioRecorder onRecorded={setBlob} />

            <div className="grid gap-3 rounded-3xl border border-slate-200/70 bg-white/60 p-5">
              <div className="text-sm font-semibold text-slate-900">
                Context (improves feedback)
              </div>
              <div className="grid gap-3 md:grid-cols-2">
                <Input
                  label="Goal"
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                />
                <Input
                  label="Audience"
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                />
                <Input
                  label="Time limit (seconds)"
                  type="number"
                  value={timeLimit}
                  onChange={(e) => setTimeLimit(Number(e.target.value))}
                />
                <Input
                  label="Rubric"
                  value={rubric}
                  onChange={(e) => setRubric(e.target.value)}
                />
              </div>
            </div>

            {err ? (
              <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {err}
              </div>
            ) : null}

            <div className="flex items-center justify-end gap-3">
              <Button
                variant="secondary"
                disabled={!blob || loading}
                onClick={() => setBlob(null)}
              >
                Clear
              </Button>
              <Button disabled={!blob || loading} onClick={submit}>
                {loading ? "Submitting..." : "Submit for feedback"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  );
}
