// =====================================================
// Footverse Art Studio - layout.js
// (2D Layout hesapları + preview canvas + layout box)
// =====================================================
window.FVTemplateLayout = (function () {
  "use strict";

  /**
   * Ana layout hesaplama fonksiyonu.
   * - SVG oluşturur
   * - viewBox / width / height ayarlarını yapar
   * - İstenirse şeffaf layout kutusunu çizer
   * - Ortak centerX/centerY ve padding döner
   *
   * @param {object} paramsObj - Tüm params JSON objesi
   * @param {HTMLElement} previewBox - SVG preview alanı
   * @returns {object} layoutInfo
   *          { width, height, padding, centerX, centerY, svg, svgNS, layout }
   */
  function computeLayout(paramsObj, previewBox) {
    var layout = (paramsObj && paramsObj.layout) || {};

    var width = Number(layout.width || 360);
    if (!width || width < 200) width = 360;

    var height = Number(layout.height || 360);
    if (!height || height < 200) height = 360;

    var padding = Number(layout.padding);
    if (isNaN(padding) || padding < 0) padding = 24;

    var offsetX = Number(layout.offset_x || 0);
    var offsetY = Number(layout.offset_y || 0);

    var svgNS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(svgNS, "svg");

    svg.setAttribute("viewBox", "0 0 " + width + " " + height);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");

    // Layout kutusu (sadece preview için)
    var showBox = !!layout.show_box;
    if (showBox) {
      var box = document.createElementNS(svgNS, "rect");
      box.setAttribute("x", "0");
      box.setAttribute("y", "0");
      box.setAttribute("width", String(width));
      box.setAttribute("height", String(height));
      box.setAttribute("fill", "#ffffff");
      box.setAttribute("fill-opacity", "0.02");
      box.setAttribute("stroke", "#999999");
      box.setAttribute("stroke-width", "1");
      box.setAttribute("stroke-dasharray", "4 4");
      svg.appendChild(box);
    }

    // Ortak merkez: layout ortası + offset
    var centerX = width / 2 + offsetX;
    var centerY = height / 2 + offsetY;

    return {
      width: width,
      height: height,
      padding: padding,
      centerX: centerX,
      centerY: centerY,
      svg: svg,
      svgNS: svgNS,
      layout: layout
    };
  }

  return {
    computeLayout: computeLayout
  };
})();
