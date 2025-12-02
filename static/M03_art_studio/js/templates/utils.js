// =====================================================
// Footverse Art Studio - Utils
// Global helper fonksiyonlar
// =====================================================

window.FVTemplateUtils = (function () {
  "use strict";

  function safeParseJSON(text) {
    if (!text || !String(text).trim()) return {};
    try {
      return JSON.parse(text);
    } catch (err) {
      console.warn("[TemplateStudio] JSON parse hatası:", err);
      return {};
    }
  }

  function getNested(obj, path) {
    if (!obj || !path) return undefined;
    return path.split(".").reduce(function (acc, key) {
      if (acc && Object.prototype.hasOwnProperty.call(acc, key)) {
        return acc[key];
      }
      return undefined;
    }, obj);
  }

  function setNested(obj, path, value) {
    if (!obj || !path) return;
    var parts = path.split(".");
    var current = obj;

    for (var i = 0; i < parts.length; i++) {
      var key = parts[i];
      if (i === parts.length - 1) {
        current[key] = value;
      } else {
        if (
          !current[key] ||
          Object.prototype.toString.call(current[key]) !== "[object Object]"
        ) {
          current[key] = {};
        }
        current = current[key];
      }
    }
  }

  function deleteNested(obj, path) {
    if (!obj || !path) return;
    var parts = path.split(".");
    var last = parts.pop();
    var parentPath = parts.join(".");
    var parent = getNested(obj, parentPath);

    if (parent && Object.prototype.hasOwnProperty.call(parent, last)) {
      delete parent[last];
    }
  }

  return {
    safeParseJSON: safeParseJSON,
    getNested: getNested,
    setNested: setNested,
    deleteNested: deleteNested
  };
})();
