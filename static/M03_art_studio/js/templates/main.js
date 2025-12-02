// =====================================================
// Footverse Art Studio - Template Studio Main
// (Form + sekmeler + JSON senk + modüler preview)
// =====================================================
(function () {
  "use strict";

  var Utils = window.FVTemplateUtils || {};
  var Layout = window.FVTemplateLayout || null;
  var Shape = window.FVTemplateShape || null;
  var Icon = window.FVTemplateIcon || null;
  var Stars = window.FVTemplateStars || null;
  var Platform = window.FVTemplatePlatform || null;
  var Effects = window.FVTemplateEffects || null;

  var safeParseJSON = Utils.safeParseJSON || function (text) {
    if (!text || !String(text).trim()) return {};
    try {
      return JSON.parse(text);
    } catch (err) {
      console.warn("[TemplateStudio] JSON parse hatası (fallback):", err);
      return {};
    }
  };
  var getNested = Utils.getNested || function () {};
  var setNested = Utils.setNested || function () {};
  var deleteNested = Utils.deleteNested || function () {};

  // ----------------------------- //
  // Template kartları
  // ----------------------------- //
  function initTemplateCards() {
    var cards = document.querySelectorAll(".tpl-card-item");
    if (!cards.length) return;

    cards.forEach(function (card) {
      card.addEventListener("click", function (ev) {
        var target = ev.target;

        if (
          target.closest(".tpl-card-action") ||
          target.closest("a") ||
          target.tagName === "BUTTON"
        ) {
          return;
        }

        var url = card.getAttribute("data-detail-url");
        if (url) {
          window.location.href = url;
        }
      });
    });
  }

  // ----------------------------- //
  // Parametre sekmeleri
  // ----------------------------- //
  function initParamTabs(root) {
    var container = root || document;
    var tabs = container.querySelectorAll(".tpl-param-tab");
    var panels = container.querySelectorAll(".tpl-param-panel");
    if (!tabs.length || !panels.length) return;

    function activateTab(tabName) {
      tabs.forEach(function (tab) {
        var isTarget = tab.getAttribute("data-tab") === tabName;
        if (tab.classList.contains("is-disabled")) return;
        tab.classList.toggle("is-active", isTarget);
      });

      panels.forEach(function (panel) {
        var isTarget = panel.getAttribute("data-tab") === tabName;
        panel.classList.toggle("is-active", isTarget);
      });
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        if (tab.classList.contains("is-disabled")) return;
        var name = tab.getAttribute("data-tab");
        activateTab(name);
      });
    });

    var active = container.querySelector(".tpl-param-tab.is-active");
    if (!active) {
      var first = Array.from(tabs).find(function (t) {
        return !t.classList.contains("is-disabled");
      });
      if (first) {
        activateTab(first.getAttribute("data-tab"));
      }
    }
  }

  // ----------------------------- //
  // Template formu
  // ----------------------------- //
  function initTemplateForm() {
    var form = document.querySelector(".template-form");
    if (!form) return;

    var paramsField = form.querySelector("textarea[name='params']");
    var previewBox = document.getElementById("template-live-preview");
    var paramsObj = paramsField ? safeParseJSON(paramsField.value) : {};

    var cbStars = form.querySelector("input[name='show_stars']");
    var cbIcon = form.querySelector("input[name='show_icon']");
    var cbPlatform = form.querySelector("input[name='show_platform']");
    var cbEffects = form.querySelector("input[name='show_effects']");

    var tabMap = {
      stars: form.querySelector(".tpl-param-tab[data-tab='stars']"),
      icon: form.querySelector(".tpl-param-tab[data-tab='icon']"),
      platform: form.querySelector(".tpl-param-tab[data-tab='platform']"),
      effect: form.querySelector(".tpl-param-tab[data-tab='effects']")
    };
    var panelMap = {
      stars: form.querySelector(".tpl-param-panel[data-tab='stars']"),
      icon: form.querySelector(".tpl-param-panel[data-tab='icon']"),
      platform: form.querySelector(".tpl-param-panel[data-tab='platform']"),
      effect: form.querySelector(".tpl-param-panel[data-tab='effects']")
    };

    // -------------------------------------------------- //
    // JSON -> input doldurma
    // -------------------------------------------------- //
    function syncInputsFromParams() {
      var inputs = form.querySelectorAll(".tpl-param-input");

      inputs.forEach(function (input) {
        var path = input.getAttribute("data-param-path");
        if (!path) return;

        var val = getNested(paramsObj, path);
        if (typeof val === "undefined" || val === null) return;

        if (input.type === "color") {
          if (typeof val === "string" && val) {
            input.value = val;
          }
        } else if (input.type === "checkbox") {
          input.checked = !!val;
        } else if (input.type === "range" || input.type === "number") {
          input.value = val;
        } else if (input.tagName === "SELECT") {
          input.value = val;
        } else {
          input.value = val;
        }
      });

      updateSliderLabels();
    }

    // -------------------------------------------------- //
    // Input -> JSON (tek input)
    // -------------------------------------------------- //
    function readInputValue(input) {
      var value;
      if (input.type === "color") {
        value = input.value || null;
      } else if (input.type === "number" || input.type === "range") {
        if (input.value === "" || input.value === null) {
          value = null;
        } else {
          var num = Number(input.value);
          value = isNaN(num) ? null : num;
        }
      } else if (input.type === "checkbox") {
        value = !!input.checked;
      } else if (input.tagName === "SELECT") {
        value = input.value || null;
      } else {
        value = input.value;
      }
      return value;
    }

    function handleParamInput(ev) {
      var input = ev.target;
      if (!input.classList.contains("tpl-param-input")) return;

      var path = input.getAttribute("data-param-path");
      if (!path) return;

      if (
        (path.indexOf("icon.") === 0 && cbIcon && !cbIcon.checked) ||
        (path.indexOf("stars.") === 0 && cbStars && !cbStars.checked) ||
        (path.indexOf("platform.") === 0 && cbPlatform && !cbPlatform.checked) ||
        (path.indexOf("effect.") === 0 && cbEffects && !cbEffects.checked)
      ) {
        return;
      }

      var value = readInputValue(input);
      setNested(paramsObj, path, value);
      updateSliderLabels();
      syncParamsToTextarea();
      renderPreview();
    }

    // -------------------------------------------------- //
    // Varsayılan değerleri JSON'a basma
    // -------------------------------------------------- //
    function bootstrapDefaultsIntoParams() {
      var inputs = form.querySelectorAll(".tpl-param-input");

      inputs.forEach(function (input) {
        var path = input.getAttribute("data-param-path");
        if (!path) return;

        if (
          (path.indexOf("icon.") === 0 && cbIcon && !cbIcon.checked) ||
          (path.indexOf("stars.") === 0 && cbStars && !cbStars.checked) ||
          (path.indexOf("platform.") === 0 && cbPlatform && !cbPlatform.checked) ||
          (path.indexOf("effect.") === 0 && cbEffects && !cbEffects.checked)
        ) {
          return;
        }

        var existing = getNested(paramsObj, path);
        if (typeof existing !== "undefined") return;

        var value = readInputValue(input);
        setNested(paramsObj, path, value);
      });

      syncParamsToTextarea();
    }

    // -------------------------------------------------- //
    // Slider label'ları
    // -------------------------------------------------- //
    function updateSliderLabels() {
      var sliders = form.querySelectorAll("input[type='range'].tpl-param-input");
      sliders.forEach(function (slider) {
        var span = form.querySelector(
          "[data-slider-value-for='" + slider.id + "']"
        );
        if (span) {
          span.textContent = slider.value;
        }
      });
    }

    function initSliders() {
      var sliders = form.querySelectorAll("input[type='range'].tpl-param-input");

      sliders.forEach(function (slider) {
        var handler = function () {
          updateSliderLabels();
        };
        slider.addEventListener("input", handler);
      });

      var buttons = form.querySelectorAll(".tpl-slider-btn");
      buttons.forEach(function (btn) {
        if (btn._fvBound) return;
        btn._fvBound = true;

        btn.addEventListener("click", function () {
          var targetId = btn.getAttribute("data-slider-target");
          var step = Number(btn.getAttribute("data-slider-step") || "1");
          var slider = form.querySelector("#" + targetId);
          if (!slider) return;

          var min =
            slider.min === "" || slider.min === undefined
              ? -Infinity
              : Number(slider.min);
          var max =
            slider.max === "" || slider.max === undefined
              ? Infinity
              : Number(slider.max);
          var current = Number(slider.value || "0");
          var next = current + step;

          if (!isNaN(min)) next = Math.max(next, min);
          if (!isNaN(max)) next = Math.min(next, max);

          slider.value = String(next);
          slider.dispatchEvent(new Event("input", { bubbles: true }));
          handleParamInput({ target: slider });
        });
      });

      updateSliderLabels();
    }

    // -------------------------------------------------- //
    // Checkbox -> JSON grupları + sekmeler
    // -------------------------------------------------- //
    function toggleGroup(groupName, enabled) {
      var tab = tabMap[groupName];
      var panel = panelMap[groupName];

      if (tab) {
        tab.classList.toggle("is-disabled", !enabled);
        if (!enabled && tab.classList.contains("is-active")) {
          var fallback = form.querySelector(".tpl-param-tab:not(.is-disabled)");
          if (fallback) {
            fallback.click();
          }
        }
      }
      if (panel) {
        panel.classList.toggle("is-disabled", !enabled);
        if (!enabled) {
          panel.classList.remove("is-active");
        }
      }

      if (!enabled) {
        deleteNested(paramsObj, groupName);
      } else {
        var groupInputs = form.querySelectorAll(
          ".tpl-param-input[data-param-path^='" + groupName + ".']"
        );
        groupInputs.forEach(function (input) {
          var path = input.getAttribute("data-param-path");
          var value = readInputValue(input);
          setNested(paramsObj, path, value);
        });
      }

      syncParamsToTextarea();
      renderPreview();
      initParamTabs(form);
    }

    function bindVisibilityCheckbox(cb, groupName) {
      if (!cb) return;
      toggleGroup(groupName, cb.checked);
      cb.addEventListener("change", function () {
        toggleGroup(groupName, cb.checked);
      });
    }

    // -------------------------------------------------- //
    // JSON textarea senk
    // -------------------------------------------------- //
    function syncParamsToTextarea() {
      if (!paramsField) return;
      try {
        paramsField.value = JSON.stringify(paramsObj, null, 2);
      } catch (err) {
        console.warn("[TemplateStudio] JSON stringify hatası:", err);
      }
    }

    function handleRawJsonBlur() {
      if (!paramsField) return;
      paramsObj = safeParseJSON(paramsField.value);
      syncInputsFromParams();
      bootstrapDefaultsIntoParams();
      renderPreview();
    }

    // -------------------------------------------------- //
    // SVG Preview (Layout + Shape + Icon + Stars + Platform + Effects)
// -------------------------------------------------- //
    function renderPreview() {
      if (!previewBox) return;
      previewBox.innerHTML = "";

      if (!Layout || typeof Layout.computeLayout !== "function") {
        var empty = document.createElement("div");
        empty.className = "empty-state";
        empty.innerHTML =
          "<p>Önizleme için layout modülü yüklü değil.</p>";
        previewBox.appendChild(empty);
        return;
      }

      var layoutInfo = Layout.computeLayout(paramsObj, previewBox);
      var svg = layoutInfo.svg;
      var shapeEl = null;

      var shapeParams = (paramsObj && paramsObj.shape) || {};
      if (!shapeParams.type) {
        var empty = document.createElement("div");
        empty.className = "empty-state";
        empty.innerHTML =
          "<p>Önizleme için önce bir <strong>şekil tipi</strong> seçin.</p>";
        previewBox.appendChild(svg);
        previewBox.appendChild(empty);
        return;
      }

      if (Shape && typeof Shape.draw === "function") {
        shapeEl = Shape.draw(svg, paramsObj, layoutInfo);
      }

      if (cbIcon && cbIcon.checked && Icon && typeof Icon.draw === "function") {
        Icon.draw(svg, paramsObj, layoutInfo);
      }

      if (
        cbStars &&
        cbStars.checked &&
        Stars &&
        typeof Stars.draw === "function"
      ) {
        Stars.draw(svg, paramsObj, layoutInfo);
      }

      if (
        cbPlatform &&
        cbPlatform.checked &&
        Platform &&
        typeof Platform.draw === "function"
      ) {
        Platform.draw(svg, paramsObj, layoutInfo);
      }

      if (
        cbEffects &&
        cbEffects.checked &&
        Effects &&
        typeof Effects.apply === "function" &&
        shapeEl
      ) {
        Effects.apply(svg, paramsObj, layoutInfo, shapeEl);
      }

      previewBox.appendChild(svg);
    }

    // -------------------------------------------------- //
    // Temizle butonu
    // -------------------------------------------------- //
    function bindResetButton() {
      var resetBtn = form.querySelector("button[type='reset']");
      if (!resetBtn) return;

      resetBtn.addEventListener("click", function () {
        setTimeout(function () {
          paramsObj = {};
          syncInputsFromParams();
          bootstrapDefaultsIntoParams();
          syncInputsFromParams();
          renderPreview();
        }, 50);
      });
    }

    // Başlat
    syncInputsFromParams();
    bootstrapDefaultsIntoParams();
    syncInputsFromParams();
    initSliders();
    renderPreview();

    form.addEventListener("input", handleParamInput);
    if (paramsField) {
      paramsField.addEventListener("blur", handleRawJsonBlur);
    }

    bindVisibilityCheckbox(cbStars, "stars");
    bindVisibilityCheckbox(cbIcon, "icon");
    bindVisibilityCheckbox(cbPlatform, "platform");
    bindVisibilityCheckbox(cbEffects, "effect");

    bindResetButton();
  }

  document.addEventListener("DOMContentLoaded", function () {
    try {
      initTemplateCards();
      initTemplateForm();
      initParamTabs(document);
    } catch (err) {
      console.error("[TemplateStudio] init sırasında hata:", err);
    }
  });
})();
