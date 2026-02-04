"use client";

import { useRef, useState } from "react";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

export default function AudioRecorder({
  onRecorded,
}: {
  onRecorded: (blob: Blob) => void;
}) {
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const [recording, setRecording] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  async function start() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mr = new MediaRecorder(stream);

    chunksRef.current = [];
    mr.ondataavailable = (e) => chunksRef.current.push(e.data);

    mr.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      const url = URL.createObjectURL(blob);
      setPreviewUrl(url);
      onRecorded(blob);
      stream.getTracks().forEach((t) => t.stop());
    };

    mediaRecorderRef.current = mr;
    mr.start();
    setRecording(true);
  }

  function stop() {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }

  return (
    <div className="grid gap-4">
      <div className="flex flex-wrap items-center gap-3">
        {recording ? (
          <Button variant="danger" onClick={stop}>
            Stop
          </Button>
        ) : (
          <Button onClick={start}>Start recording</Button>
        )}

        <Badge tone={recording ? "brand" : "neutral"}>
          {recording ? "Recording..." : "Ready"}
        </Badge>

        <div className="text-sm text-slate-600">
          Tip: speak for at least 20 seconds for better feedback.
        </div>
      </div>

      <div className="rounded-3xl border border-slate-200/70 bg-white/70 px-5 py-5 shadow-soft">
        {recording ? (
          <div className="flex items-center justify-between">
            <div className="text-sm font-medium text-slate-800">
              Listening...
            </div>
            <div className="flex gap-1">
              <span className="h-2 w-2 animate-pulse rounded-full bg-brand-600" />
              <span className="h-2 w-2 animate-pulse rounded-full bg-brand-600 [animation-delay:150ms]" />
              <span className="h-2 w-2 animate-pulse rounded-full bg-brand-600 [animation-delay:300ms]" />
            </div>
          </div>
        ) : previewUrl ? (
          <div className="grid gap-2">
            <div className="text-sm font-semibold text-slate-900">Preview</div>
            <audio controls src={previewUrl} className="w-full" />
            <div className="text-xs text-slate-500">
              If the preview sounds too quiet, move closer to the mic and reduce
              background noise.
            </div>
          </div>
        ) : (
          <div className="text-sm text-slate-600">
            No recording yet. Press Start recording to begin.
          </div>
        )}
      </div>
    </div>
  );
}
