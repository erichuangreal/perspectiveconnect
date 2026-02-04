"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";

function formatTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

function SimpleLine({
  title,
  subtitle,
  data,
  dataKey,
  yLabel,
}: {
  title: string;
  subtitle?: string;
  data: any[];
  dataKey: string;
  yLabel?: string;
}) {
  return (
    <Card>
      <CardHeader title={title} subtitle={subtitle} />
      <CardContent>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="4 4" />
              <XAxis
                dataKey="created_at"
                tickFormatter={formatTime}
                minTickGap={24}
              />
              <YAxis width={36} />
              <Tooltip
                labelFormatter={(v) => formatTime(String(v))}
                formatter={(val) => [val, yLabel || dataKey]}
              />
              <Line
                type="monotone"
                dataKey={dataKey}
                strokeWidth={3}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

export default function AnalyticsCharts({ series }: { series: any[] }) {
  return (
    <div className="grid gap-4">
      <div className="grid gap-4 md:grid-cols-2">
        <SimpleLine
          title="Overall score"
          subtitle="0 to 100, higher is better"
          data={series}
          dataKey="overall_score"
          yLabel="score"
        />
        <SimpleLine
          title="Speech rate"
          subtitle="Syllables per second, stable 2.0 to 3.5 is ideal"
          data={series}
          dataKey="syllables_per_second"
          yLabel="syll/sec"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <SimpleLine
          title="Pitch variability"
          subtitle="Too low sounds monotone, too high sounds unstable"
          data={series}
          dataKey="pitch_std"
          yLabel="pitch std"
        />
        <SimpleLine
          title="Filler density"
          subtitle="Lower is better. Track um, uh, like, basically, you know"
          data={series}
          dataKey="filler_density"
          yLabel="fillers/word"
        />
      </div>
    </div>
  );
}
