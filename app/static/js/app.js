/* CineBook — progressive enhancement.
   Vanilla JS, no dependencies. Handles theme, nav, flash and loading states. */
(function () {
  "use strict";

  var root = document.documentElement;

  /* ---- Theme toggle (persisted in localStorage) ---- */
  function setTheme(theme) {
    root.setAttribute("data-theme", theme);
    try { localStorage.setItem("theme", theme); } catch (e) {}
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "light" ? "#f6f7fb" : "#0b0d17");
  }

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-theme-toggle]");
    if (toggle) {
      var current = root.getAttribute("data-theme") || "dark";
      setTheme(current === "dark" ? "light" : "dark");
    }
  });

  /* ---- Mobile nav ---- */
  var navToggle = document.querySelector("[data-nav-toggle]");
  var navLinks = document.querySelector("[data-nav-links]");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      var open = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* ---- Dismissible flash messages (auto-hide after 6s) ---- */
  document.querySelectorAll(".flash").forEach(function (flash) {
    var close = flash.querySelector("[data-flash-close]");
    function remove() {
      flash.style.transition = "opacity .3s, transform .3s";
      flash.style.opacity = "0";
      flash.style.transform = "translateY(-8px)";
      setTimeout(function () { flash.remove(); }, 300);
    }
    if (close) close.addEventListener("click", remove);
    setTimeout(remove, 6000);
  });

  /* ---- Loading state on form submit (spinner + disabled) ---- */
  document.querySelectorAll("form[data-loading]").forEach(function (form) {
    form.addEventListener("submit", function () {
      var btn = form.querySelector('button[type="submit"]');
      if (btn && !btn.disabled) {
        btn.dataset.label = btn.innerHTML;
        btn.innerHTML = '<span class="spinner"></span> Processing…';
        btn.classList.add("is-loading");
        btn.disabled = true;
      }
    });
  });
})();
