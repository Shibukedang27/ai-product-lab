(function () {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#site-nav");
  const form = document.querySelector("#contact-form");
  const status = document.querySelector("#form-status");

  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.setAttribute("aria-label", open ? "Open menu" : "Close menu");
      nav.classList.toggle("is-open", !open);
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
        nav.classList.remove("is-open");
      });
    });
  }

  if (form && status) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      status.classList.remove("is-success", "is-error");

      const name = form.name.value.trim();
      const email = form.email.value.trim();
      const party = form.party.value;
      const message = form.message.value.trim();

      if (!name || !email) {
        status.textContent = "Please add your name and email.";
        status.classList.add("is-error");
        return;
      }

      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        status.textContent = "That email doesn’t look right — try again.";
        status.classList.add("is-error");
        return;
      }

      console.log("[Roast Lane demo] table request", {
        name: name,
        email: email,
        party: party,
        message: message,
      });

      status.textContent =
        "Thanks, " + name.split(" ")[0] + "! We’ll confirm shortly. (Demo — nothing was sent.)";
      status.classList.add("is-success");
      form.reset();
    });
  }
})();
