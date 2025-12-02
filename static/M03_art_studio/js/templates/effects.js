// =====================================================
// Footverse Art Studio - effects.js
// (Glow / basit efekt katmanı)
// =====================================================
window.FVTemplateEffects = (function () {
  "use strict";

  /**
   * Glow efektini uygular.
   * @param {SVGElement} svg
   * @param {object} paramsObj
   * @param {object} layoutInfo
   * @param {SVGElement} shapeEl - Ana shape elementi
   */
  function apply(svg, paramsObj, layoutInfo, shapeEl) {
    if (!svg || !shapeEl) return;

    var effectParams = (paramsObj && paramsObj.effect) || {};
    var blurVal = Number(effectParams.blur || 0);
    if (!blurVal || blurVal <= 0) return;

    var colors = (paramsObj && paramsObj.colors) || {};
    var glowColor = effectParams.color || colors.fill || "#ffffff";

    var svgNS = layoutInfo.svgNS || "http://www.w3.org/2000/svg";
    var defs = svg.querySelector("defs");
    if (!defs) {
      defs = document.createElementNS(svgNS, "defs");
      svg.appendChild(defs);
    }

    var filter = document.createElementNS(svgNS, "filter");
    filter.setAttribute("id", "fv-glow");
    filter.setAttribute("x", "-50%");
    filter.setAttribute("y", "-50%");
    filter.setAttribute("width", "200%");
    filter.setAttribute("height", "200%");

    // Blur
    var feGaussian = document.createElementNS(svgNS, "feGaussianBlur");
    feGaussian.setAttribute("stdDeviation", String(blurVal));
    feGaussian.setAttribute("result", "coloredBlur");
    filter.appendChild(feGaussian);

    // Renk katmanı
    var feColor = document.createElementNS(svgNS, "feColorMatrix");
    feColor.setAttribute("type", "matrix");
    // Basit bir renk tonlaması; alpha korunuyor
    feColor.setAttribute(
      "values",
      "0 0 0 0 " +
        hexToRgbComponent(glowColor, 0) +
        " 0 0 0 0 " +
        hexToRgbComponent(glowColor, 1) +
        " 0 0 0 0 " +
        hexToRgbComponent(glowColor, 2) +
        " 0 0 0 1 0"
    );
    feColor.setAttribute("in", "coloredBlur");
    feColor.setAttribute("result", "coloredBlur");
    filter.appendChild(feColor);

    var feMerge = document.createElementNS(svgNS, "feMerge");
    var feMergeNode1 = document.createElementNS(svgNS, "feMergeNode");
    feMergeNode1.setAttribute("in", "coloredBlur");
    feMerge.appendChild(feMergeNode1);
    var feMergeNode2 = document.createElementNS(svgNS, "feMergeNode");
    feMergeNode2.setAttribute("in", "SourceGraphic");
    feMerge.appendChild(feMergeNode2);

    filter.appendChild(feMerge);
    defs.appendChild(filter);

    // SADECE FILTER, fill'e DOKUNMUYORUZ
    shapeEl.setAttribute("filter", "url(#fv-glow)");
  }

  function hexToRgbComponent(hex, index) {
    if (!hex || typeof hex !== "string") return 1;
    var clean = hex.replace("#", "");
    if (clean.length === 3) {
      clean =
        clean[0] +
        clean[0] +
        clean[1] +
        clean[1] +
        clean[2] +
        clean[2];
    }
    if (clean.length !== 6) return 1;
    var r = parseInt(clean.substr(0, 2), 16) / 255;
    var g = parseInt(clean.substr(2, 2), 16) / 255;
    var b = parseInt(clean.substr(4, 2), 16) / 255;
    var arr = [r, g, b];
    return arr[index] || 1;
  }

  return {
    apply: apply
  };
})();
