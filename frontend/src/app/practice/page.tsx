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
  const [progress, setProgress] = useState("");

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
    setProgress("Uploading audio...");

    try {
      const form = new FormData();
      form.append("audio_file", blob, "recording.webm");
      form.append("goal", goal);
      form.append("audience", audience);
      form.append("time_limit_seconds", String(timeLimit));
      form.append("rubric", rubric);

      // Simulate progress updates based on typical processing times
      const t1 = setTimeout(() => setProgress("Converting audio format..."), 1000);
      const t2 = setTimeout(() => setProgress("Transcribing speech with AI..."), 3000);
      const t3 = setTimeout(() => setProgress("Analyzing voice features..."), 8000);
      const t4 = setTimeout(() => setProgress("Generating coaching feedback..."), 15000);

      const data = await apiFetch("/training/submit", {
        method: "POST",
        body: form,
      });
      
      // Clear any pending timeouts
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      clearTimeout(t4);
      
      setProgress("Complete! Redirecting...");
      setTimeout(() => {
        router.push(`/sessions/${data.session_id}`);
      }, 500);
    } catch (e: any) {
      setErr(e.message);
      setProgress("");
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    setBlob(null);
    setProgress("");
    setErr("");
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

            {loading && progress ? (
              <div className="rounded-2xl border border-brand-200 bg-brand-50 p-4">
                <div className="flex items-center gap-3">
                  <div className="flex gap-1">
                    <span className="h-2 w-2 animate-pulse rounded-full bg-brand-600" />
                    <span className="h-2 w-2 animate-pulse rounded-full bg-brand-600 [animation-delay:150ms]" />
                    <span className="h-2 w-2 animate-pulse rounded-full bg-brand-600 [animation-delay:300ms]" />
                  </div>
                  <div className="text-sm font-medium text-brand-900">
                    {progress}
                  </div>
                </div>
                <div className="mt-2 text-xs text-brand-700">
                  This typically takes 30-60 seconds. Please wait...
                </div>
              </div>
            ) : null}

            <div className="flex items-center justify-end gap-3">
              <Button
                variant="secondary"
                disabled={!blob || loading}
                onClick={handleClear}
              >
                Clear
              </Button>
              <Button disabled={!blob || loading} onClick={submit}>
                {loading ? "Processing..." : "Submit for feedback"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  );
}
