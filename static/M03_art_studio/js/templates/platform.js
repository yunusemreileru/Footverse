// =====================================================
// Footverse Art Studio - platform.js
// (Alt platform bandı + text)
// =====================================================
window.FVTemplatePlatform = (function () {
  "use strict";

  function draw(svg, paramsObj, layoutInfo) {
    var platform = (paramsObj && paramsObj.platform) || {};
    var svgNS = layoutInfo.svgNS;
    var width = layoutInfo.width;
    var height = layoutInfo.height;
    var padding = layoutInfo.padding || 0;

    var pw = Number(platform.width || 150);
    var ph = Number(platform.height || 40);
    var pxOff = Number(platform.x || 0);
    var pyOff = Number(platform.y || 60);

    var basePX = width / 2 - pw / 2 + pxOff;
    var basePY = height - padding - ph + pyOff;

    var plat = document.createElementNS(svgNS, "rect");
    plat.setAttribute("x", String(basePX));
    plat.setAttribute("y", String(basePY));
    plat.setAttribute("width", String(pw));
    plat.setAttribute("height", String(ph));

    var platRadius = Math.min(ph, pw) * 0.4;
    plat.setAttribute("rx", String(platRadius));
    plat.setAttribute("ry", String(platRadius));

    // NOT: HTML'de data-param-path="platform.color"
    plat.setAttribute("fill", platform.color || "#444444");
    plat.setAttribute(
      "stroke",
      platform.border_color || "#000000"
    );
    plat.setAttribute(
      "stroke-width",
      String(platform.border_width || 2)
    );

    svg.appendChild(plat);

    if (platform.text && platform.show_text !== false) {
      var textEl = document.createElementNS(svgNS, "text");
      textEl.textContent = platform.text;
      textEl.setAttribute("x", String(width / 2 + pxOff));
      textEl.setAttribute("y", String(basePY + ph / 2 + 4));
      textEl.setAttribute("text-anchor", "middle");
      textEl.setAttribute(
        "fill",
        platform.text_color || "#ffffff"
      );
      textEl.setAttribute(
        "font-size",
        String(platform.text_size || 16)
      );
      svg.appendChild(textEl);
    }
  }

  return {
    draw: draw
  };
})();
