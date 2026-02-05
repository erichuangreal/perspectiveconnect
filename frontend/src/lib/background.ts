export type BackgroundTheme = "gradient" | "green-waves" | "blue-waves" | "tranquil-lake";

export function setBackground(theme: BackgroundTheme) {
  if (typeof window !== "undefined") {
    localStorage.setItem("pc_background", theme);
  }
}

export function getBackground(): BackgroundTheme {
  if (typeof window !== "undefined") {
    const saved = localStorage.getItem("pc_background");
    if (saved === "green-waves" || saved === "blue-waves" || saved === "gradient" || saved === "tranquil-lake") {
      return saved;
    }
  }
  return "gradient"; // default
}
