"use client";

import React from "react";

type Props = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  hint?: string;
  error?: string;
};

export default function Input({
  label,
  hint,
  error,
  className = "",
  ...props
}: Props) {
  return (
    <label className="grid gap-2">
      {label ? (
        <div className="text-sm font-medium text-slate-800">{label}</div>
      ) : null}
      <input
        className={
          "h-11 rounded-2xl border bg-white/90 px-4 text-sm outline-none transition " +
          "border-slate-200 focus:border-brand-300 focus:ring-2 focus:ring-brand-100 " +
          (error
            ? "border-rose-300 focus:border-rose-400 focus:ring-rose-100 "
            : "") +
          className
        }
        {...props}
      />
      {error ? <div className="text-sm text-rose-600">{error}</div> : null}
      {!error && hint ? (
        <div className="text-sm text-slate-500">{hint}</div>
      ) : null}
    </label>
  );
}
