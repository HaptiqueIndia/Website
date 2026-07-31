export type ComparisonRow = {
  label: string;
  remote: string;
  irController: string;
  smartApp: string;
  acboss: string;
};

export type HardwareDetail = { name: string; benefit: string };

export const siteContent = {
  hero: {
    headline: "Your AC, finally on autopilot.",
    supporting: "More comfort. Less energy. Zero manual fiddling.",
  },
  founder: {
    eyebrow: "Cold is not always comfortable.",
    body: "Acboss began with a familiar problem: waking up in an over-cooled, dry room and another uncomfortable morning. We built a better way to cool, one that responds to the room instead of making you keep reaching for the remote.",
  },
  proof: {
    title: "Acboss working with a Split AC",
    caption: "A working demonstration of Acboss with a Split AC.",
    demos: [
      {
        embedSrc: "https://www.youtube-nocookie.com/embed/aNUCqgTFvj8",
        fallbackHref: "https://youtu.be/aNUCqgTFvj8",
        title: "Acboss working with a Split AC",
        fallbackLabel: "Watch the full demo on YouTube",
      },
    ],
  },
  savings: {
    headline: "Designed to use up to 24% less energy for cooling.",
    evidenceNote:
      "Evidence note: no redacted electricity bill is available to publish, so no bill image is shown. Treat 24% as an upper-bound estimate, not a guarantee.",
    disclaimer: "Results vary by home, weather, AC, and use.",
  },
  comparisonRows: [
    { label: "Feels the room, not just the AC", remote: "No", irController: "No", smartApp: "No", acboss: "Yes: temperature and humidity aware" },
    { label: "Adjusts cooling by itself", remote: "No", irController: "Usually manual or scheduled", smartApp: "Usually manual or scheduled", acboss: "Yes: continuously optimizes comfort" },
    { label: "Coordinates AC and fan", remote: "No", irController: "No", smartApp: "Rarely", acboss: "Yes: optimized together" },
    { label: "Works when internet is down", remote: "Yes", irController: "Often", smartApp: "Usually no", acboss: "Yes: entirely local" },
    { label: "Learns the right cooling response", remote: "No", irController: "No", smartApp: "No", acboss: "Yes: edge logic built for Indian conditions" },
  ] satisfies ComparisonRow[],
  hardwareDetails: [
    { name: "ESP32-C5 controller", benefit: "Provides the processing foundation and supports both 5 GHz and 2.4 GHz Wi-Fi capability." },
    { name: "Human-presence sensor", benefit: "Lets Acboss understand whether a person is in the room before making comfort decisions." },
    { name: "IR transmitter and receiver", benefit: "Learns your AC remote during setup, then controls the existing Split AC." },
    { name: "Sensirion temperature and humidity sensor", benefit: "Provides accurate room-condition inputs for Acboss’s local comfort logic." },
    { name: "Matter-ready platform", benefit: "Designed for a future Matter path." },
  ] satisfies HardwareDetail[],
  faqs: [
    { question: "Will Acboss work with my AC?", answer: "Acboss is designed to learn compatible infrared Split AC remotes during setup. Early availability is limited to tested setups." },
    { question: "Does Acboss need Wi-Fi?", answer: "No. Its comfort decisions run locally, so the core experience does not depend on an internet connection." },
    { question: "What does an early unit look like?", answer: "It is a handmade, 3D-printed build from our tested prototype platform." },
  ],
  preorder: {
    earlyUnitNotice: "Early Acboss units are handmade, 3D-printed builds from our tested prototype platform.",
  },
} as const;
