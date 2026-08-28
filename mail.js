// The address is stored in two base64 parts and joined at runtime, so the
// literal string never appears in the served HTML. That stops naive harvesters,
// which is most of them — it is not a guarantee against a scraper that runs
// JavaScript.
//
// The address is rendered as selectable text with a copy button as well as a
// mailto: link, because a link alone is useless to anyone whose device has no
// mail client configured.
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".mail").forEach(function (el) {
    var address = atob(el.dataset.u) + String.fromCharCode(64) + atob(el.dataset.d);

    var wrap = document.createElement("span");
    wrap.className = "mail-address";

    var link = document.createElement("a");
    link.href = "mailto:" + address + "?subject=" + encodeURIComponent("Pacheco");
    link.textContent = address;
    wrap.appendChild(link);

    var copy = document.createElement("button");
    copy.type = "button";
    copy.className = "copy";
    copy.textContent = "Copy";
    copy.setAttribute("aria-label", "Copy the email address");
    copy.addEventListener("click", function () {
      navigator.clipboard.writeText(address).then(function () {
        copy.textContent = "Copied";
        copy.classList.add("copied");
        setTimeout(function () {
          copy.textContent = "Copy";
          copy.classList.remove("copied");
        }, 2000);
      }, function () {
        copy.textContent = "Select it above";
      });
    });
    wrap.appendChild(copy);

    el.replaceWith(wrap);
  });
});
