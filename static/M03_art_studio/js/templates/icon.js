// =====================================================
// Footverse Art Studio - icon.js
// (Merkez ikon - PNG)
// =====================================================
window.FVTemplateIcon = (function () {
  "use strict";

  function draw(svg, paramsObj, layoutInfo) {
    var iconParams = (paramsObj && paramsObj.icon) || {};
    if (!iconParams.src) return null;

    var svgNS = layoutInfo.svgNS;
    var cx = layoutInfo.centerX;
    var cy = layoutInfo.centerY;

    var iconSize = Number(iconParams.size || 96);
    if (iconSize < 8) iconSize = 8;
    var iconOffsetX = Number(iconParams.offset_x || 0);
    var iconOffsetY = Number(iconParams.offset_y || 0);

    var x = cx - iconSize / 2 + iconOffsetX;
    var y = cy - iconSize / 2 + iconOffsetY;

    var img = document.createElementNS(svgNS, "image");
    // PATH DÜZELTİLDİ: img/icons
    img.setAttributeNS(
      "http://www.w3.org/1999/xlink",
      "href",
      "/static/M03_art_studio/img/icons/" + iconParams.src
    );
    img.setAttribute("x", String(x));
    img.setAttribute("y", String(y));
    img.setAttribute("width", String(iconSize));
    img.setAttribute("height", String(iconSize));

    svg.appendChild(img);
    return img;
  }

  return {
    draw: draw
  };
})();
