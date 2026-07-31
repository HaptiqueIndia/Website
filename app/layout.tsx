import type { Metadata } from "next";
import { headers } from "next/headers";
import "./globals.css";

export const metadata: Metadata = {
  title: "Acboss — Your AC, finally on autopilot",
  description:
    "Put your AC on autopilot for more comfort, less energy, and zero manual fiddling.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const requestHeaders = await headers();
  const host = (
    requestHeaders.get("x-forwarded-host") ??
    requestHeaders.get("host") ??
    "localhost:3000"
  )
    .split(",")[0]
    .trim();
  const forwardedProtocol = requestHeaders
    .get("x-forwarded-proto")
    ?.split(",")[0]
    .trim();
  const protocol =
    forwardedProtocol ??
    (/^(localhost|127\.0\.0\.1|\[::1\])(?::|$)/.test(host) ? "http" : "https");
  const socialImage = new URL("/og.png", `${protocol}://${host}`).toString();

  return (
    <html lang="en">
      <head>
        <meta
          property="og:title"
          content="Acboss — Your AC, finally on autopilot"
        />
        <meta
          property="og:description"
          content="More comfort. Less energy. Zero manual fiddling."
        />
        <meta property="og:type" content="website" />
        <meta property="og:image" content={socialImage} />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta
          property="og:image:alt"
          content="Acboss — Your AC, finally on autopilot"
        />
        <meta name="twitter:card" content="summary_large_image" />
        <meta
          name="twitter:title"
          content="Acboss — Your AC, finally on autopilot"
        />
        <meta
          name="twitter:description"
          content="More comfort. Less energy. Zero manual fiddling."
        />
        <meta name="twitter:image" content={socialImage} />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
