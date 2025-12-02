// =====================================================
// Footverse Art Studio - stars.js
// (Yıldız bandı)
// =====================================================
window.FVTemplateStars = (function () {
  "use strict";

  function draw(svg, paramsObj, layoutInfo) {
    var stars = (paramsObj && paramsObj.stars) || {};
    var svgNS = layoutInfo.svgNS;
    var width = layoutInfo.width;
    var padding = layoutInfo.padding || 0;

    var count = Math.max(1, Number(stars.count || 5));
    var starSize = Number(stars.size || 24);
    var gap = Number(stars.gap || starSize * 1.5);
    var color = stars.color || "#FFD700";
    var borderColor = stars.border_color || color;
    var offsetX = Number(stars.offset_x || 0);
    var offsetY = Number(stars.offset_y || 0);

    var baseY = padding + starSize * 1.4 + offsetY;
    var totalWidth = (count - 1) * gap;
    var startX = width / 2 - totalWidth / 2 + offsetX;

    for (var i = 0; i < count; i++) {
      var sx = startX + i * gap;
      var pathData = buildStarPath(sx, baseY, starSize / 2, starSize / 4);

      var starEl = document.createElementNS(svgNS, "path");
      starEl.setAttribute("d", pathData);
      starEl.setAttribute("fill", color);
      starEl.setAttribute("stroke", borderColor);
      starEl.setAttribute("stroke-width", "1");
      svg.appendChild(starEl);
    }
  }

  function buildStarPath(cx, cy, outerR, innerR) {
    var d = "";
    for (var i = 0; i < 10; i++) {
      var angle = (Math.PI * 2 * i) / 10 - Math.PI / 2;
      var r = i % 2 === 0 ? outerR : innerR;
      var x = cx + r * Math.cos(angle);
      var y = cy + r * Math.sin(angle);
      d += (i === 0 ? "M" : "L") + x.toFixed(2) + " " + y.toFixed(2);
    }
    d += "Z";
    return d;
  }

  return {
    draw: draw
  };
})();
