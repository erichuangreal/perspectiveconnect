"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { clearToken, getToken } from "@/lib/auth";
import { usePathname, useRouter } from "next/navigation";
import Button from "@/components/ui/Button";

function NavLink({ href, label }: { href: string; label: string }) {
  const pathname = usePathname();
  const active = pathname === href;
  return (
    <Link
      href={href}
      className={
        "rounded-2xl px-3 py-2 text-sm font-medium transition " +
        (active
          ? "bg-brand-600 text-white shadow-soft"
          : "text-slate-700 hover:bg-white/70")
      }
    >
      {label}
    </Link>
  );
}

export default function Nav() {
  const [authed, setAuthed] = useState(false);
  const router = useRouter();

  useEffect(() => {
    setAuthed(!!getToken());
  }, []);

  function logout() {
    clearToken();
    setAuthed(false);
    router.push("/login");
  }

  return (
    <div className="sticky top-0 z-10 border-b border-slate-200/60 bg-white/60 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-3">
          <div className="grid h-9 w-9 place-items-center rounded-2xl bg-brand-600 text-white shadow-soft">
            pc
          </div>
          <div className="leading-tight">
            <div className="font-semibold text-slate-900">
              perspectiveconnect
            </div>
            <div className="text-xs text-slate-500">presentation trainer</div>
          </div>
        </Link>

        <div className="flex items-center gap-2">
          {authed ? (
            <>
              <NavLink href="/dashboard" label="Dashboard" />
              <NavLink href="/practice" label="Practice" />
              <Button variant="secondary" onClick={logout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <NavLink href="/login" label="Login" />
              <NavLink href="/register" label="Register" />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
