import { describe, expect, it } from "vitest";
import { siteContent } from "./site-content";

describe("Acboss customer claims", () => {
  it("caps the headline savings claim at 24% and retains the variance disclaimer", () => {
    expect(siteContent.savings.headline).toContain("up to 24%");
    expect(siteContent.savings.disclaimer).toMatch(/results vary/i);
  });

  it("keeps Matter language future-facing and avoids certification claims", () => {
    const matter = siteContent.hardwareDetails.find(
      (item) => item.name === "Matter-ready platform",
    );
    expect(matter?.name).toMatch(/Matter-ready/i);
    expect(matter?.benefit).toMatch(/future Matter path/i);
    expect(matter?.benefit).not.toMatch(/Matter-certified/i);
  });

  it("makes the early-unit nature explicit", () => {
    expect(siteContent.preorder.earlyUnitNotice).toMatch(/handmade/i);
    expect(siteContent.preorder.earlyUnitNotice).toMatch(/3D-printed/i);
  });
});
