export default function Badge({
  children,
  tone = "neutral",
}: {
  children: React.ReactNode;
  tone?: "neutral" | "brand" | "success";
}) {
  const base =
    "inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium";
  const tones: Record<string, string> = {
    neutral: "border-slate-200 bg-slate-50 text-slate-700",
    brand: "border-brand-200 bg-brand-50 text-brand-700",
    success: "border-emerald-200 bg-emerald-50 text-emerald-700",
  };

  return <span className={`${base} ${tones[tone]}`}>{children}</span>;
}
