"""Capture marketing/documentation screenshots with Playwright.

Run the dev server first (``python run.py``) and seed demo data
(``flask seed-db``), then:

    python scripts/capture_screenshots.py

Screenshots are written to ``docs/screenshots``.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5000"
OUT = Path(__file__).resolve().parent.parent / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)


def _set_theme(page, theme: str) -> None:
    page.evaluate(
        "(t) => { localStorage.setItem('theme', t);"
        "document.documentElement.setAttribute('data-theme', t); }",
        theme,
    )


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 860})
        page = ctx.new_page()

        # Landing — dark
        page.goto(BASE, wait_until="networkidle")
        _set_theme(page, "dark")
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(700)
        page.screenshot(path=str(OUT / "landing-dark.png"))

        # Landing — light
        _set_theme(page, "light")
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(700)
        page.screenshot(path=str(OUT / "landing-light.png"))

        # Login page (dark)
        _set_theme(page, "dark")
        page.goto(f"{BASE}/auth/login", wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUT / "login.png"))

        # Log in as the seeded demo user, then capture the dashboard
        page.fill("#identifier", "demo")
        page.fill("#password", "demopass123")
        page.click("#submit")
        page.wait_for_url(f"{BASE}/dashboard/", wait_until="networkidle")
        page.wait_for_timeout(700)
        page.screenshot(path=str(OUT / "dashboard.png"))

        # Booking form
        page.goto(f"{BASE}/dashboard/new", wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUT / "booking-form.png"))

        # Mobile dashboard
        mobile = browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=2,
        )
        mp = mobile.new_page()
        mp.goto(f"{BASE}/auth/login", wait_until="networkidle")
        mp.fill("#identifier", "demo")
        mp.fill("#password", "demopass123")
        mp.click("#submit")
        mp.wait_for_url(f"{BASE}/dashboard/", wait_until="networkidle")
        mp.wait_for_timeout(700)
        mp.screenshot(path=str(OUT / "mobile-dashboard.png"))

        browser.close()

    print(f"Screenshots written to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
