// The address is stored in two base64 parts and joined at runtime, so the
// literal string never appears in the served HTML. That stops naive harvesters,
// which is most of them — it is not a guarantee against a scraper that runs
// JavaScript.
//
// The address is rendered as selectable text with a copy button as well as a
// mailto: link, because a link alone is useless to anyone whose device has no
// mail client configured.
var MAIL_LABELS = {
  en: { copy: "Copy", copied: "Copied", fallback: "Select it above", aria: "Copy the email address" },
  es: { copy: "Copiar", copied: "Copiado", fallback: "Selecciónalo arriba", aria: "Copiar la dirección de correo" }
};

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".mail").forEach(function (el) {
    var address = atob(el.dataset.u) + String.fromCharCode(64) + atob(el.dataset.d);

    // Each language block carries its own lang attribute, so the button label
    // matches the text around it.
    var scope = el.closest("[lang]");
    var t = MAIL_LABELS[(scope && scope.getAttribute("lang")) === "es" ? "es" : "en"];

    var wrap = document.createElement("span");
    wrap.className = "mail-address";

    var link = document.createElement("a");
    link.href = "mailto:" + address + "?subject=" + encodeURIComponent("Pacheco");
    link.textContent = address;
    wrap.appendChild(link);

    var copy = document.createElement("button");
    copy.type = "button";
    copy.className = "copy";
    copy.textContent = t.copy;
    copy.setAttribute("aria-label", t.aria);
    copy.addEventListener("click", function () {
      navigator.clipboard.writeText(address).then(function () {
        copy.textContent = t.copied;
        copy.classList.add("copied");
        setTimeout(function () {
          copy.textContent = t.copy;
          copy.classList.remove("copied");
        }, 2000);
      }, function () {
        copy.textContent = t.fallback;
      });
    });
    wrap.appendChild(copy);

    el.replaceWith(wrap);
  });
});
