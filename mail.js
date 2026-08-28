// The address is stored in two base64 parts and joined at runtime, so the
// literal string never appears in the served HTML. This stops naive harvesters,
// which is most of them. It is not a guarantee — anything the browser can
// assemble, a determined scraper running JavaScript can assemble too.
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".mail").forEach(function (el) {
    var address = atob(el.dataset.u) + String.fromCharCode(64) + atob(el.dataset.d);
    var link = document.createElement("a");
    link.href = "mailto:" + address + "?subject=" + encodeURIComponent("Pacheco");
    link.textContent = address;
    el.replaceWith(link);
  });
});
