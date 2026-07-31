import { describe, expect, it } from "vitest";
import { metadata } from "./layout";

describe("Acboss metadata", () => {
  it("uses product-specific title and description", () => {
    expect(metadata.title).toMatch(/Acboss/i);
    expect(metadata.description).toMatch(/autopilot/i);
  });
});
