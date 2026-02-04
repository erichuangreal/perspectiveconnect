import Link from "next/link";
import Button from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";

export default function Home() {
  return (
    <div className="grid gap-6">
      <Card className="overflow-hidden">
        <CardContent className="px-6 py-7">
          <div className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-medium text-brand-700">
            New
            <span className="text-brand-600">Light friendly UI</span>
          </div>

          <h1 className="mt-4 text-3xl font-semibold tracking-tight text-slate-900">
            Practice speaking with clear, actionable coaching
          </h1>

          <p className="mt-2 max-w-2xl text-sm text-slate-600">
            Record a presentation, get transcript plus delivery analysis, then
            track improvement over time. Built to help you sound clearer,
            calmer, and more confident.
          </p>

          <div className="mt-5 flex flex-wrap gap-2">
            <Link href="/practice">
              <Button size="lg">Start practice</Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="secondary">
                View dashboard
              </Button>
            </Link>
          </div>

          <div className="mt-6 grid gap-3 md:grid-cols-3">
            <div className="rounded-3xl border border-slate-200/70 bg-white/70 p-4">
              <div className="text-sm font-semibold text-slate-900">
                Transcript
              </div>
              <div className="mt-1 text-sm text-slate-600">
                See exactly what you said. Find filler words and vague sentences
                fast.
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200/70 bg-white/70 p-4">
              <div className="text-sm font-semibold text-slate-900">
                Delivery metrics
              </div>
              <div className="mt-1 text-sm text-slate-600">
                Track pacing, pitch variability, loudness stability, and
                clarity.
              </div>
            </div>

            <div className="rounded-3xl border border-slate-200/70 bg-white/70 p-4">
              <div className="text-sm font-semibold text-slate-900">
                Concrete rewrites
              </div>
              <div className="mt-1 text-sm text-slate-600">
                Not generic advice. Your exact lines are quoted and rewritten
                stronger.
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardContent className="px-6 py-6">
            <div className="text-sm font-semibold text-slate-900">
              How it works
            </div>
            <ol className="mt-2 grid gap-2 text-sm text-slate-600">
              <li>1 Record your talk in Practice</li>
              <li>2 Submit and get transcript plus coaching</li>
              <li>3 Review feedback and repeat</li>
              <li>4 Watch your progress in Dashboard</li>
            </ol>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="px-6 py-6">
            <div className="text-sm font-semibold text-slate-900">
              Best results when you
            </div>
            <ul className="mt-2 grid gap-2 text-sm text-slate-600">
              <li>Speak at least 20 to 40 seconds</li>
              <li>Use a quiet room and talk toward the mic</li>
              <li>Set the context fields on the Practice page</li>
              <li>Repeat the same topic to measure improvement</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
