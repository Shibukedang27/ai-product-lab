/**
 * Variance FAQ Chatbot — embeddable vanilla JS widget
 * No backend. Answers from a local FAQ map; lead capture logs to console.
 */
(function (global) {
  "use strict";

  var FAQ = [
    {
      keys: ["hour", "open", "timing", "time", "when", "schedule"],
      answer:
        "We’re open Mon–Fri 7:30 AM–10:00 PM and Sat–Sun 8:00 AM–11:00 PM (IST). Walk-ins welcome.",
    },
    {
      keys: ["price", "cost", "menu", "filter", "coffee", "how much", "rupee", "₹"],
      answer:
        "Popular prices: Filter coffee ₹90 · Flat white ₹180 · Pour-over from ₹220 · Light bites from ₹120. Full menu is on our site.",
    },
    {
      keys: ["contact", "phone", "email", "reach", "call", "whatsapp", "address", "location", "where"],
      answer:
        "Find us at Plot 42, Road No. 36, Jubilee Hills, Hyderabad 500033. Call +91 40 4000 1234 or email hello@roastlane.demo.",
    },
    {
      keys: ["wifi", "wi-fi", "internet", "laptop", "work"],
      answer:
        "Yes — free fast Wi-Fi, power at every table, and quieter mornings until 11 AM.",
    },
    {
      keys: ["book", "table", "reserv", "seat"],
      answer:
        "You can request a table from our contact form, or leave your name and email here and we’ll confirm by message.",
    },
    {
      keys: ["vegan", "plant", "milk", "dairy", "allerg"],
      answer:
        "Plant milk is available on request. Tell your barista about allergies — we’ll guide you on bites.",
    },
  ];

  var QUICK = ["Hours?", "Filter coffee price?", "Contact info?", "Leave my details"];

  function matchAnswer(text) {
    var q = String(text || "").toLowerCase();
    if (!q.trim()) return null;
    for (var i = 0; i < FAQ.length; i++) {
      var item = FAQ[i];
      for (var k = 0; k < item.keys.length; k++) {
        if (q.indexOf(item.keys[k]) !== -1) return item.answer;
      }
    }
    return null;
  }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function init(options) {
    options = options || {};
    var brand = options.brand || "FAQ Helper";
    var subtitle = options.subtitle || "Ask a question";
    var accent = options.accent || "#c45c26";
    var welcome =
      options.welcome ||
      "Hi! Ask about hours, pricing, or contact — or leave your details and we’ll follow up.";

    var root = document.getElementById("variance-faq-root") || document.body;
    document.documentElement.style.setProperty("--vf-accent", accent);

    var launcher = el("button", "vf-launcher", "💬");
    launcher.type = "button";
    launcher.setAttribute("aria-label", "Open chat");

    var panel = el("div", "vf-panel");
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", brand + " chat");

    var header = el("div", "vf-header");
    header.appendChild(el("h2", null, brand));
    header.appendChild(el("p", null, subtitle));

    var messages = el("div", "vf-messages");
    messages.setAttribute("aria-live", "polite");

    var quick = el("div", "vf-quick");

    var compose = el("div", "vf-compose");
    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Type a question…";
    input.setAttribute("aria-label", "Your question");
    var sendBtn = el("button", null, "Send");
    sendBtn.type = "button";
    compose.appendChild(input);
    compose.appendChild(sendBtn);

    var lead = el("div", "vf-lead");
    lead.innerHTML =
      '<label for="vf-lead-name">Name</label>' +
      '<input id="vf-lead-name" type="text" autocomplete="name" placeholder="Your name" />' +
      '<label for="vf-lead-email">Email</label>' +
      '<input id="vf-lead-email" type="email" autocomplete="email" placeholder="you@email.com" />' +
      '<div class="vf-lead-actions">' +
      '<button type="button" class="vf-lead-submit">Send details</button>' +
      '<button type="button" class="vf-lead-skip">Skip</button>' +
      "</div>";

    var credit = el("div", "vf-credit", "Built by Variance");

    panel.appendChild(header);
    panel.appendChild(messages);
    panel.appendChild(quick);
    panel.appendChild(compose);
    panel.appendChild(lead);
    panel.appendChild(credit);
    root.appendChild(panel);
    root.appendChild(launcher);

    function addBubble(text, who) {
      var bubble = el("div", "vf-bubble " + who, text);
      messages.appendChild(bubble);
      messages.scrollTop = messages.scrollHeight;
    }

    function showLead() {
      lead.classList.add("is-visible");
      addBubble("Sure — drop your name and email and we’ll get back to you. (Demo: logged to console only.)", "bot");
    }

    function hideLead() {
      lead.classList.remove("is-visible");
    }

    function handleUserText(raw) {
      var text = String(raw || "").trim();
      if (!text) return;
      addBubble(text, "user");

      var lower = text.toLowerCase();
      if (
        lower.indexOf("leave") !== -1 ||
        lower.indexOf("details") !== -1 ||
        lower.indexOf("callback") !== -1 ||
        lower.indexOf("human") !== -1 ||
        lower.indexOf("talk to") !== -1
      ) {
        showLead();
        return;
      }

      var answer = matchAnswer(text);
      if (answer) {
        addBubble(answer, "bot");
      } else {
        addBubble(
          "I’m not sure about that yet. Try asking about hours, prices, Wi-Fi, or contact — or tap “Leave my details”.",
          "bot"
        );
      }
    }

    QUICK.forEach(function (label) {
      var chip = el("button", "vf-chip", label);
      chip.type = "button";
      chip.addEventListener("click", function () {
        if (label === "Leave my details") {
          addBubble(label, "user");
          showLead();
        } else {
          handleUserText(label);
        }
      });
      quick.appendChild(chip);
    });

    function send() {
      handleUserText(input.value);
      input.value = "";
      input.focus();
    }

    sendBtn.addEventListener("click", send);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        send();
      }
    });

    launcher.addEventListener("click", function () {
      var open = panel.classList.toggle("is-open");
      launcher.textContent = open ? "✕" : "💬";
      launcher.setAttribute("aria-label", open ? "Close chat" : "Open chat");
      if (open && messages.childNodes.length === 0) {
        addBubble(welcome, "bot");
      }
    });

    lead.querySelector(".vf-lead-submit").addEventListener("click", function () {
      var name = lead.querySelector("#vf-lead-name").value.trim();
      var email = lead.querySelector("#vf-lead-email").value.trim();
      if (!name || !email) {
        addBubble("Please add both name and email.", "bot");
        return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        addBubble("That email doesn’t look valid — try again.", "bot");
        return;
      }
      console.log("[Variance FAQ demo] lead capture", { name: name, email: email, brand: brand });
      hideLead();
      addBubble("Thanks, " + name.split(" ")[0] + "! We’ll be in touch. (Demo — nothing was emailed.)", "bot");
      lead.querySelector("#vf-lead-name").value = "";
      lead.querySelector("#vf-lead-email").value = "";
    });

    lead.querySelector(".vf-lead-skip").addEventListener("click", function () {
      hideLead();
      addBubble("No problem — ask another question anytime.", "bot");
    });
  }

  global.VarianceFAQ = { init: init, faq: FAQ };
})(window);
