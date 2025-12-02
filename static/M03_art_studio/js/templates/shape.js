// =====================================================
// Footverse Art Studio - shape.js
// (Circle / square / rounded / hexagon / polygon)
// =====================================================
window.FVTemplateShape = (function () {
  "use strict";

  function draw(svg, paramsObj, layoutInfo) {
    var shapeParams = (paramsObj && paramsObj.shape) || {};
    var colorParams = (paramsObj && paramsObj.colors) || {};
    var type = shapeParams.type || "";

    if (!type) {
      return null;
    }

    var width = layoutInfo.width;
    var height = layoutInfo.height;
    var padding = layoutInfo.padding || 0;
    var cx = layoutInfo.centerX;
    var cy = layoutInfo.centerY;
    var svgNS = layoutInfo.svgNS;

    var maxR = Math.min(width, height) / 2 - padding;
    if (maxR < 16) maxR = 16;

    var size = Number(shapeParams.size || 144);
    var rawRadius = size > 0 ? size / 2 : maxR;
    var radius = Math.min(rawRadius, maxR);

    var fill = colorParams.fill || "#ffffff";
    var stroke = colorParams.stroke || "#000000";
    var strokeWidth =
      typeof colorParams.stroke_width === "number"
        ? colorParams.stroke_width
        : 4;

    var shapeEl = null;

    if (type === "circle") {
      shapeEl = document.createElementNS(svgNS, "circle");
      shapeEl.setAttribute("cx", String(cx));
      shapeEl.setAttribute("cy", String(cy));
      shapeEl.setAttribute("r", String(radius));
    } else if (type === "square" || type === "rounded") {
      var side = radius * 2;
      var x = cx - side / 2;
      var y = cy - side / 2;
      shapeEl = document.createElementNS(svgNS, "rect");
      shapeEl.setAttribute("x", String(x));
      shapeEl.setAttribute("y", String(y));
      shapeEl.setAttribute("width", String(side));
      shapeEl.setAttribute("height", String(side));
      if (type === "rounded") {
        var rr = side * 0.2;
        shapeEl.setAttribute("rx", String(rr));
        shapeEl.setAttribute("ry", String(rr));
      }
    } else {
      // polygon / hexagon
      var sides = 6;
      if (type === "hexagon") {
        sides = 6;
      } else if (type === "polygon") {
        var maybe = Number(shapeParams.corners || shapeParams.sides || 5);
        if (isNaN(maybe) || maybe < 3) maybe = 5;
        sides = maybe;
      }

      var points = [];
      for (var i = 0; i < sides; i++) {
        var angle = (Math.PI * 2 * i) / sides - Math.PI / 2;
        var xP = cx + radius * Math.cos(angle);
        var yP = cy + radius * Math.sin(angle);
        points.push(xP.toFixed(2) + "," + yP.toFixed(2));
      }

      shapeEl = document.createElementNS(svgNS, "polygon");
      shapeEl.setAttribute("points", points.join(" "));
    }

    shapeEl.setAttribute("fill", fill);
    shapeEl.setAttribute("stroke", stroke);
    shapeEl.setAttribute("stroke-width", String(strokeWidth || 0));

    svg.appendChild(shapeEl);
    return shapeEl;
  }

  return {
    draw: draw
  };
})();
