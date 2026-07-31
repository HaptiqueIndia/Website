import {
  cleanup,
  fireEvent,
  render,
  screen,
  within,
} from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { AcbossLanding } from "./acboss-landing";

afterEach(cleanup);

describe("AcbossLanding", () => {
  it("does not lead the hero with a pre-order action", () => {
    render(<AcbossLanding />);
    expect(screen.getByRole("link", { name: /see why acboss exists/i })).toHaveAttribute("href", "#founder-story");
    expect(screen.getByRole("link", { name: /watch it work/i })).toHaveAttribute("href", "#proof");
  });

  it("offers pre-order in navigation without adding it to the hero actions", () => {
    render(<AcbossLanding />);
    const navigation = screen.getByRole("navigation", { name: /primary/i });
    const hero = screen.getByRole("region", {
      name: /your ac, finally on autopilot/i,
    });

    expect(
      within(navigation).getByRole("link", { name: /pre-order/i }),
    ).toHaveAttribute("href", "#preorder");
    expect(
      within(hero).queryByRole("link", { name: /pre-order/i }),
    ).not.toBeInTheDocument();
  });

  it("uses only the approved working demo with a direct YouTube fallback", () => {
    render(<AcbossLanding />);

    expect(
      screen.getByTitle(/acboss working with a split ac/i),
    ).toHaveAttribute(
      "src",
      "https://www.youtube-nocookie.com/embed/aNUCqgTFvj8",
    );
    expect(
      screen.getByRole("link", { name: /watch the full demo on youtube/i }),
    ).toHaveAttribute("href", "https://youtu.be/aNUCqgTFvj8");
    expect(screen.getAllByTitle(/acboss working with a split ac/i)).toHaveLength(1);
  });

  it("presents the savings ceiling with evidence context and variance", () => {
    render(<AcbossLanding />);

    expect(screen.getByText(/up to 24% less energy/i)).toBeVisible();
    expect(
      screen.getByText(/no redacted electricity bill is available to publish/i),
    ).toBeVisible();
    expect(
      screen.getByText(/results vary by home, weather, ac, and use/i),
    ).toBeVisible();
    expect(
      screen.queryByAltText(/redacted electricity bill comparison/i),
    ).not.toBeInTheDocument();
  });

  it("keeps the comparison table's overflow affordance available", () => {
    render(<AcbossLanding />);

    expect(
      screen.getByText(/scroll to compare all options/i),
    ).toBeVisible();
    const comparison = screen.getByRole("region", {
      name: /ac control comparison/i,
    });
    expect(comparison).toHaveAttribute("tabindex", "0");
    expect(comparison).toHaveAttribute(
      "aria-describedby",
      "comparison-scroll-hint",
    );
  });

  it("exposes the early-build disclosure to assistive technology", () => {
    render(<AcbossLanding />);

    const disclosure = screen.getByText(/handmade & 3d-printed/i);
    expect(disclosure).toBeVisible();
    expect(disclosure.closest('[aria-hidden="true"]')).toBeNull();
  });

  it("keeps invalid pre-order fields visible with specific errors", () => {
    render(<AcbossLanding />);
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "asha@" },
    });
    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));
    expect(screen.getByText(/enter your name/i)).toBeVisible();
    expect(screen.getByText(/enter a valid email/i)).toBeVisible();
    expect(screen.getByText(/tell us your city/i)).toBeVisible();
    expect(screen.getByLabelText(/email/i)).toHaveValue("asha@");
  });

  it("clears a field's stale error when the user corrects it", () => {
    render(<AcbossLanding />);
    const name = screen.getByLabelText(/name/i);

    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));
    expect(name).toHaveAttribute("aria-invalid", "true");

    fireEvent.change(name, { target: { value: "Asha" } });
    expect(name).toHaveAttribute("aria-invalid", "false");
    expect(screen.queryByText(/enter your name/i)).not.toBeInTheDocument();
  });

  it("confirms interest without claiming payment", () => {
    render(<AcbossLanding />);
    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: "Asha" } });
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "asha@example.com" } });
    fireEvent.change(screen.getByLabelText(/city/i), { target: { value: "Pune" } });
    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));
    expect(screen.getByText(/we received your early-access interest/i)).toBeVisible();
    expect(screen.queryByText(/payment received/i)).not.toBeInTheDocument();
  });
});
