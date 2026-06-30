/* @ds-bundle: {"format":3,"namespace":"ResQRulesDesignSystem_3e3070","components":[{"name":"Button","sourcePath":"components/actions/Button.jsx"},{"name":"CfButton","sourcePath":"components/actions/CfButton.jsx"},{"name":"LangToggle","sourcePath":"components/actions/LangToggle.jsx"},{"name":"OutlinedButton","sourcePath":"components/actions/OutlinedButton.jsx"},{"name":"Card","sourcePath":"components/content/Card.jsx"},{"name":"PageCitation","sourcePath":"components/content/PageCitation.jsx"},{"name":"TierBadge","sourcePath":"components/content/TierBadge.jsx"},{"name":"UrgencyBadge","sourcePath":"components/content/UrgencyBadge.jsx"},{"name":"Icon","sourcePath":"components/core/Icon.jsx"},{"name":"LoadingBar","sourcePath":"components/feedback/LoadingBar.jsx"},{"name":"OverrideToast","sourcePath":"components/feedback/OverrideToast.jsx"},{"name":"Snackbar","sourcePath":"components/feedback/Snackbar.jsx"},{"name":"AppBar","sourcePath":"components/surfaces/AppBar.jsx"},{"name":"BottomSheet","sourcePath":"components/surfaces/BottomSheet.jsx"},{"name":"DangerPanel","sourcePath":"components/surfaces/DangerPanel.jsx"}],"sourceHashes":{"components/actions/Button.jsx":"4ed0707b8d58","components/actions/CfButton.jsx":"97b2c0b6dacb","components/actions/LangToggle.jsx":"574f04af1a29","components/actions/OutlinedButton.jsx":"adb99bbabf3b","components/content/Card.jsx":"ecd2115b6d59","components/content/PageCitation.jsx":"4d5cf404e11c","components/content/TierBadge.jsx":"0df6440aea2e","components/content/UrgencyBadge.jsx":"c95c6086cbff","components/core/Icon.jsx":"62645741e6f3","components/feedback/LoadingBar.jsx":"235253624573","components/feedback/OverrideToast.jsx":"cfa91676c994","components/feedback/Snackbar.jsx":"34e8ce27ca80","components/surfaces/AppBar.jsx":"a35e38c7455c","components/surfaces/BottomSheet.jsx":"b9c83b5e7f56","components/surfaces/DangerPanel.jsx":"b354b80c113f"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.ResQRulesDesignSystem_3e3070 = window.ResQRulesDesignSystem_3e3070 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/actions/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Button — primary ElevatedButton. Full-width, 56dp, red fill, white label.
 * States: default · pressed (primary-700) · disabled (neutral) · loading (spinner, no text).
 */
function Button({
  children,
  onClick,
  disabled = false,
  loading = false,
  fullWidth = true,
  dir,
  style = {},
  ...rest
}) {
  const [pressed, setPressed] = React.useState(false);
  const [hovered, setHovered] = React.useState(false);
  const [focused, setFocused] = React.useState(false);
  const inert = disabled || loading;
  let background = 'var(--primary-600)';
  if (disabled) background = 'var(--neutral-300)';else if (pressed) background = 'var(--primary-700)';else if (hovered) background = 'var(--primary-400)';
  const color = disabled ? 'var(--neutral-600)' : 'var(--on-primary)';
  const base = {
    appearance: 'none',
    width: fullWidth ? '100%' : 'auto',
    minHeight: 'var(--touch-min)',
    padding: '0 20px',
    border: 'none',
    borderRadius: 'var(--radius-md)',
    background,
    color,
    fontFamily: 'var(--font-sans)',
    fontSize: 'var(--text-label)',
    fontWeight: 'var(--weight-semibold)',
    lineHeight: 'var(--lh-label)',
    cursor: inert ? disabled ? 'not-allowed' : 'progress' : 'pointer',
    boxShadow: disabled ? 'none' : focused ? 'var(--focus-ring)' : 'var(--elevation-card)',
    transition: 'background 120ms ease, box-shadow 120ms ease',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    userSelect: 'none',
    direction: dir,
    ...style
  };
  const endPress = () => setPressed(false);
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    dir: dir,
    disabled: disabled,
    "aria-busy": loading || undefined,
    onClick: inert ? undefined : onClick,
    onPointerDown: () => !inert && setPressed(true),
    onPointerUp: endPress,
    onPointerLeave: () => {
      endPress();
      setHovered(false);
    },
    onPointerEnter: () => !inert && setHovered(true),
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    style: base
  }, rest), loading ? /*#__PURE__*/React.createElement("span", {
    className: "rq-anim-spin",
    "aria-hidden": "true",
    style: {
      width: 20,
      height: 20,
      borderRadius: '50%',
      border: '2.5px solid rgba(255,255,255,0.45)',
      borderTopColor: 'var(--on-primary)',
      animation: 'rq-spin 0.7s linear infinite'
    }
  }) : children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/actions/Button.jsx", error: String((e && e.message) || e) }); }

// components/actions/CfButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const CF_LEVEL = {
  certain: {
    color: 'var(--success-700)',
    cf: '+1.00'
  },
  likely: {
    color: 'var(--success-700)',
    cf: '+0.60'
  },
  unsure: {
    color: 'var(--warning-600)',
    cf: '+0.20'
  },
  none: {
    color: 'var(--primary-600)',
    cf: '\u22121.00'
  }
};

/**
 * CfButton — certainty-factor confidence option. Outlined, full-width, 56dp.
 * Label on one side, CF value on the other. Border + text recolor per level:
 * certain/likely → green, unsure → orange, none → red.
 */
function CfButton({
  children,
  level = 'certain',
  cf,
  onClick,
  disabled = false,
  fullWidth = true,
  dir,
  style = {},
  ...rest
}) {
  const [pressed, setPressed] = React.useState(false);
  const [focused, setFocused] = React.useState(false);
  const spec = CF_LEVEL[level] || CF_LEVEL.certain;
  const accent = disabled ? 'var(--neutral-300)' : spec.color;
  const cfText = cf != null ? cf : spec.cf;
  const base = {
    appearance: 'none',
    width: fullWidth ? '100%' : 'auto',
    minHeight: 'var(--touch-min)',
    padding: '0 16px',
    border: `1.5px solid ${accent}`,
    borderRadius: 'var(--radius-md)',
    background: 'transparent',
    color: accent,
    fontFamily: 'var(--font-sans)',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: pressed && !disabled ? 0.9 : 1,
    boxShadow: focused && !disabled ? 'var(--focus-ring)' : 'none',
    transition: 'opacity 120ms ease, box-shadow 120ms ease',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 12,
    userSelect: 'none',
    direction: dir,
    ...style
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    dir: dir,
    disabled: disabled,
    onClick: disabled ? undefined : onClick,
    onPointerDown: () => !disabled && setPressed(true),
    onPointerUp: () => setPressed(false),
    onPointerLeave: () => setPressed(false),
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    style: base
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-label)',
      fontWeight: 'var(--weight-semibold)',
      lineHeight: 'var(--lh-label)'
    }
  }, children), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-caption)',
      fontWeight: 'var(--weight-semibold)',
      lineHeight: 'var(--lh-caption)',
      fontVariantNumeric: 'tabular-nums',
      direction: 'ltr',
      // CF value is always Latin numerals, LTR
      letterSpacing: '0.02em',
      opacity: 0.95
    }
  }, "CF ", cfText));
}
Object.assign(__ds_scope, { CfButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/actions/CfButton.jsx", error: String((e && e.message) || e) }); }

// components/actions/LangToggle.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * LangToggle — EN / ع segmented pill (72×32, radius-full). The active filled
 * pill slides between segments. Default styling is for the red AppBar
 * (white border, white active fill, red active text).
 */
function LangToggle({
  value = 'en',
  onChange,
  variant = 'onPrimary',
  // 'onPrimary' (red bg) | 'standalone' (light bg)
  style = {},
  ...rest
}) {
  const isAr = value === 'ar';
  const onPrimary = variant === 'onPrimary';
  const borderColor = onPrimary ? 'var(--on-primary)' : 'var(--primary-600)';
  const pillFill = onPrimary ? 'var(--on-primary)' : 'var(--primary-600)';
  const activeText = onPrimary ? 'var(--primary-600)' : 'var(--on-primary)';
  const inactiveText = onPrimary ? 'var(--on-primary)' : 'var(--primary-600)';
  const segStyle = active => ({
    flex: 1,
    zIndex: 1,
    appearance: 'none',
    border: 'none',
    background: 'transparent',
    color: active ? activeText : inactiveText,
    fontFamily: 'var(--font-sans)',
    fontSize: '13px',
    fontWeight: 'var(--weight-semibold)',
    lineHeight: 1,
    cursor: 'pointer',
    padding: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'color 200ms ease',
    userSelect: 'none'
  });
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "group",
    "aria-label": "Language",
    dir: "ltr",
    style: {
      position: 'relative',
      width: 72,
      height: 32,
      flexShrink: 0,
      boxSizing: 'border-box',
      border: `1.5px solid ${borderColor}`,
      borderRadius: 'var(--radius-full)',
      background: onPrimary ? 'transparent' : 'var(--neutral-000)',
      display: 'flex',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '50%',
      height: '100%',
      transform: isAr ? 'translateX(100%)' : 'translateX(0)',
      transition: 'transform 200ms ease'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 2.5,
      background: pillFill,
      borderRadius: 'var(--radius-full)'
    }
  })), /*#__PURE__*/React.createElement("button", {
    type: "button",
    style: segStyle(!isAr),
    "aria-pressed": !isAr,
    onClick: () => onChange && onChange('en')
  }, "EN"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    style: segStyle(isAr),
    "aria-pressed": isAr,
    onClick: () => onChange && onChange('ar'),
    lang: "ar"
  }, "\u0639"));
}
Object.assign(__ds_scope, { LangToggle });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/actions/LangToggle.jsx", error: String((e && e.message) || e) }); }

// components/actions/OutlinedButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const VARIENT_COLOR = {
  primary: 'var(--primary-600)',
  success: 'var(--success-700)',
  warning: 'var(--warning-600)',
  neutral: 'var(--neutral-900)'
};

/**
 * OutlinedButton — full-width 56dp, 1.5dp border, transparent fill.
 * Variants: primary | success | warning | neutral. Pressed = −10% opacity.
 */
function OutlinedButton({
  children,
  variant = 'primary',
  onClick,
  disabled = false,
  fullWidth = true,
  dir,
  style = {},
  ...rest
}) {
  const [pressed, setPressed] = React.useState(false);
  const [focused, setFocused] = React.useState(false);
  const accent = disabled ? 'var(--neutral-300)' : VARIENT_COLOR[variant] || VARIENT_COLOR.primary;
  const base = {
    appearance: 'none',
    width: fullWidth ? '100%' : 'auto',
    minHeight: 'var(--touch-min)',
    padding: '0 20px',
    border: `1.5px solid ${accent}`,
    borderRadius: 'var(--radius-md)',
    background: 'transparent',
    color: accent,
    fontFamily: 'var(--font-sans)',
    fontSize: 'var(--text-label)',
    fontWeight: 'var(--weight-semibold)',
    lineHeight: 'var(--lh-label)',
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: pressed && !disabled ? 0.9 : 1,
    boxShadow: focused && !disabled ? 'var(--focus-ring)' : 'none',
    transition: 'opacity 120ms ease, box-shadow 120ms ease',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    userSelect: 'none',
    direction: dir,
    ...style
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    dir: dir,
    disabled: disabled,
    onClick: disabled ? undefined : onClick,
    onPointerDown: () => !disabled && setPressed(true),
    onPointerUp: () => setPressed(false),
    onPointerLeave: () => setPressed(false),
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    style: base
  }, rest), children);
}
Object.assign(__ds_scope, { OutlinedButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/actions/OutlinedButton.jsx", error: String((e && e.message) || e) }); }

// components/content/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const CARD_VARIANT = {
  default: {
    background: 'var(--color-card)',
    accent: null
  },
  success: {
    background: 'var(--success-100)',
    accent: 'var(--success-700)'
  },
  stub: {
    background: 'var(--neutral-100)',
    accent: null
  },
  callout: {
    background: 'var(--color-card)',
    accent: 'var(--primary-600)'
  }
};

/**
 * Card — content surface. radius-lg, level-1 shadow, 20dp padding.
 * Variants: default · success (green accent + tint) · stub (grey, no shadow) ·
 * callout (red accent, intervention text). Accent border flips side in RTL.
 */
function Card({
  children,
  variant = 'default',
  dir,
  style = {},
  ...rest
}) {
  const spec = CARD_VARIANT[variant] || CARD_VARIANT.default;
  const isStub = variant === 'stub';
  return /*#__PURE__*/React.createElement("div", _extends({
    dir: dir,
    style: {
      boxSizing: 'border-box',
      width: '100%',
      background: spec.background,
      borderRadius: 'var(--radius-lg)',
      padding: 'var(--card-padding)',
      boxShadow: isStub ? 'none' : 'var(--elevation-card)',
      borderInlineStart: spec.accent ? `4px solid ${spec.accent}` : undefined,
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-body)',
      fontWeight: 'var(--weight-regular)',
      lineHeight: 'var(--lh-body)',
      color: 'var(--color-text)',
      textAlign: dir === 'rtl' ? 'right' : undefined,
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Card.jsx", error: String((e && e.message) || e) }); }

// components/content/PageCitation.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * PageCitation — source page reference, e.g. "p.7". Caption style, neutral-600.
 * Latin numerals always, even in AR mode. Set `absolute` to pin it 16dp from the
 * top screen edge (left in LTR, right in RTL).
 */
function PageCitation({
  page,
  children,
  dir = 'ltr',
  absolute = false,
  style = {},
  ...rest
}) {
  const isRtl = dir === 'rtl';
  const text = children != null ? children : `p.${page}`;
  const positioned = absolute ? {
    position: 'absolute',
    top: 'var(--screen-margin)',
    left: isRtl ? 'auto' : 'var(--screen-margin)',
    right: isRtl ? 'var(--screen-margin)' : 'auto'
  } : {};
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      // citation numerals stay Latin/LTR regardless of page direction
      direction: 'ltr',
      unicodeBidi: 'isolate',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-caption)',
      fontWeight: 'var(--weight-regular)',
      lineHeight: 'var(--lh-caption)',
      color: 'var(--neutral-600)',
      fontVariantNumeric: 'tabular-nums',
      ...positioned,
      ...style
    }
  }, rest), text);
}
Object.assign(__ds_scope, { PageCitation });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/PageCitation.jsx", error: String((e && e.message) || e) }); }

// components/content/TierBadge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const DOT = 8;

/**
 * TierBadge — 3-dot hemorrhage escalation progress. Always 3 dots (8dp, 6dp gap).
 * Dot states: applied (filled red) · current (filled red + primary-400 ring) ·
 * pending (empty, neutral-300 border). Caption "Tier N / 3" below.
 */
function TierBadge({
  current = 1,
  // active tier 1..3; 0 = all pending (entering)
  complete = false,
  // all tiers applied (post-terminal)
  lang = 'en',
  label,
  dir,
  style = {},
  ...rest
}) {
  const dotState = i => {
    if (complete) return 'applied';
    if (current === 0) return 'pending';
    if (i < current) return 'applied';
    if (i === current) return 'current';
    return 'pending';
  };
  const dotStyle = state => {
    const common = {
      width: DOT,
      height: DOT,
      borderRadius: '50%',
      boxSizing: 'border-box',
      flexShrink: 0
    };
    if (state === 'applied') {
      return {
        ...common,
        background: 'var(--primary-600)'
      };
    }
    if (state === 'current') {
      return {
        ...common,
        background: 'var(--primary-600)',
        // 4dp gap (white) then 2dp primary-400 ring, drawn without affecting layout
        boxShadow: '0 0 0 4px var(--neutral-000), 0 0 0 6px var(--primary-400)'
      };
    }
    // pending
    return {
      ...common,
      background: 'transparent',
      border: '2px solid var(--neutral-300)'
    };
  };
  const n = complete ? 3 : current || 1;
  const labelText = label != null ? label : lang === 'ar' ? `المستوى ${n} من 3` : `Tier ${n} / 3`;
  return /*#__PURE__*/React.createElement("div", _extends({
    dir: dir,
    style: {
      display: 'inline-flex',
      flexDirection: 'column',
      alignItems: dir === 'rtl' ? 'flex-end' : 'flex-start',
      gap: 8,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 6,
      alignItems: 'center',
      height: DOT + 12,
      padding: '0 6px'
    }
  }, [1, 2, 3].map(i => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: dotStyle(dotState(i))
  }))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-caption)',
      fontWeight: 'var(--weight-regular)',
      lineHeight: 'var(--lh-caption)',
      color: 'var(--neutral-600)',
      fontVariantNumeric: 'tabular-nums'
    }
  }, labelText));
}
Object.assign(__ds_scope, { TierBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/TierBadge.jsx", error: String((e && e.message) || e) }); }

// components/content/UrgencyBadge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const URGENCY = {
  critical: {
    color: 'var(--urgency-critical)',
    label: 'CRITICAL'
  },
  high: {
    color: 'var(--urgency-high)',
    label: 'HIGH'
  },
  standard: {
    color: 'var(--urgency-standard)',
    label: 'STANDARD'
  }
};

/**
 * UrgencyBadge — inline pill (radius-full), caption all-caps, white on the
 * urgency color. Levels: critical (red) · high (orange) · standard (grey).
 * Pass children to override the label (e.g. Arabic).
 */
function UrgencyBadge({
  level = 'critical',
  children,
  dir,
  style = {},
  ...rest
}) {
  const spec = URGENCY[level] || URGENCY.critical;
  return /*#__PURE__*/React.createElement("span", _extends({
    dir: dir,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      background: spec.color,
      color: 'var(--on-primary)',
      borderRadius: 'var(--radius-full)',
      padding: '6px 10px',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-caption)',
      fontWeight: 'var(--weight-semibold)',
      lineHeight: 1,
      letterSpacing: dir === 'rtl' ? 'normal' : '0.06em',
      textTransform: dir === 'rtl' ? 'none' : 'uppercase',
      whiteSpace: 'nowrap',
      ...style
    }
  }, rest), children || spec.label);
}
Object.assign(__ds_scope, { UrgencyBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/UrgencyBadge.jsx", error: String((e && e.message) || e) }); }

// components/core/Icon.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* Inlined Lucide (ISC-licensed) icon geometry — offline-safe, recolors via
   `currentColor`. Only the names this system uses are included. To add one,
   copy its inner markup from lucide.dev. viewBox is 0 0 24 24 for all. */
const ICONS = {
  droplet: /*#__PURE__*/React.createElement("path", {
    d: "M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"
  }),
  wind: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
    d: "M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M9.6 4.6A2 2 0 1 1 11 8H2"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M12.6 19.4A2 2 0 1 0 14 16H2"
  })),
  activity: /*#__PURE__*/React.createElement("path", {
    d: "M22 12h-4l-3 9L9 3l-3 9H2"
  }),
  user: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
    d: "M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "7",
    r: "4"
  })),
  zap: /*#__PURE__*/React.createElement("polygon", {
    points: "13 2 3 14 12 14 11 22 21 10 12 10 13 2"
  }),
  check: /*#__PURE__*/React.createElement("path", {
    d: "M20 6 9 17l-5-5"
  }),
  'arrow-left': /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
    d: "m12 19-7-7 7-7"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M19 12H5"
  })),
  'arrow-right': /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
    d: "M5 12h14"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m12 5 7 7-7 7"
  })),
  'rotate-ccw': /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("polyline", {
    points: "1 4 1 10 7 10"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"
  }))
};

/**
 * Icon — inline Lucide line icon. Strokes in `currentColor` (or `color`), so it
 * recolors cleanly: white on the red danger panel, red/green/orange inline.
 * Offline-safe (geometry is inlined, not fetched).
 */
function Icon({
  name,
  size = 20,
  color = 'currentColor',
  strokeWidth = 2,
  title,
  style = {},
  ...rest
}) {
  const px = typeof size === 'number' ? `${size}px` : size;
  return /*#__PURE__*/React.createElement("svg", _extends({
    xmlns: "http://www.w3.org/2000/svg",
    width: px,
    height: px,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: color,
    strokeWidth: strokeWidth,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    role: "img",
    "aria-label": title || name,
    "aria-hidden": title ? undefined : 'true',
    style: {
      display: 'inline-block',
      verticalAlign: 'middle',
      flexShrink: 0,
      ...style
    }
  }, rest), ICONS[name] || null);
}
Object.assign(__ds_scope, { Icon });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Icon.jsx", error: String((e && e.message) || e) }); }

// components/feedback/LoadingBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * LoadingBar — 3dp indeterminate progress, sweeping left→right. Sits directly
 * below the AppBar; content stays visible behind it (not a blocking spinner).
 * Set `frozen` to render a static mid-sweep frame for documentation/print.
 */
function LoadingBar({
  frozen = false,
  trackColor = 'transparent',
  style = {},
  ...rest
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "progressbar",
    "aria-label": "Loading",
    style: {
      position: 'relative',
      width: '100%',
      height: 'var(--loading-bar-height)',
      background: trackColor,
      overflow: 'hidden',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: frozen ? undefined : 'rq-anim-sweep',
    style: {
      position: 'absolute',
      top: 0,
      bottom: 0,
      left: frozen ? '25%' : '-40%',
      width: frozen ? '55%' : '40%',
      background: 'var(--primary-600)',
      borderRadius: 2,
      animation: frozen ? 'none' : 'rq-bar-sweep 1.1s ease-in-out infinite'
    }
  }));
}
Object.assign(__ds_scope, { LoadingBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/LoadingBar.jsx", error: String((e && e.message) || e) }); }

// components/feedback/OverrideToast.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const TOAST = {
  jump: {
    icon: 'zap',
    en: 'Switched to: Catastrophic Hemorrhage  (Salience 100)',
    ar: 'تحويل إلى: النزيف الكارثي  (الأولوية 100)'
  },
  guard: {
    icon: 'check',
    en: 'Already in CPR Adult — continuing',
    ar: 'أنت في بروتوكول CPR بالفعل — استمرار'
  }
};

/**
 * OverrideToast — full-width banner that slides down from the AppBar's top edge.
 * JUMP (guard_fired=false) announces a protocol switch; GUARD (guard_fired=true)
 * confirms you're already in the protocol. Slide 200ms ease-out / ease-in.
 */
function OverrideToast({
  variant = 'jump',
  visible = true,
  children,
  lang = 'en',
  dir,
  style = {},
  ...rest
}) {
  const spec = TOAST[variant] || TOAST.jump;
  const isRtl = dir === 'rtl' || lang === 'ar';
  const message = children != null ? children : lang === 'ar' ? spec.ar : spec.en;
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "status",
    dir: isRtl ? 'rtl' : 'ltr',
    style: {
      boxSizing: 'border-box',
      width: '100%',
      minHeight: 48,
      background: 'var(--primary-600)',
      color: 'var(--on-primary)',
      padding: '12px 16px',
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      flexDirection: isRtl ? 'row-reverse' : 'row',
      transform: visible ? 'translateY(0)' : 'translateY(-100%)',
      opacity: visible ? 1 : 0,
      transition: visible ? 'transform 200ms ease-out, opacity 200ms ease-out' : 'transform 200ms ease-in, opacity 200ms ease-in',
      boxShadow: 'var(--elevation-card)',
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: spec.icon,
    size: 18,
    color: "var(--on-primary)"
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-secondary)',
      fontWeight: 'var(--weight-semibold)',
      lineHeight: 'var(--lh-secondary)',
      textAlign: isRtl ? 'right' : 'left',
      flex: 1
    }
  }, message));
}
Object.assign(__ds_scope, { OverrideToast });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/OverrideToast.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Snackbar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Snackbar — full-width error bar (neutral-900, white text). The whole bar is
 * tappable to retry. Docks above the DangerPanel, or at screen bottom on Home.
 */
function Snackbar({
  children,
  onRetry,
  lang = 'en',
  dir,
  style = {},
  ...rest
}) {
  const [pressed, setPressed] = React.useState(false);
  const isRtl = dir === 'rtl' || lang === 'ar';
  const message = children != null ? children : lang === 'ar' ? 'خطأ في الاتصال — اضغط للمحاولة مجدداً' : 'Connection error — tap to retry';
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "button",
    tabIndex: 0,
    dir: isRtl ? 'rtl' : 'ltr',
    onClick: onRetry,
    onKeyDown: e => {
      if ((e.key === 'Enter' || e.key === ' ') && onRetry) {
        e.preventDefault();
        onRetry(e);
      }
    },
    onPointerDown: () => setPressed(true),
    onPointerUp: () => setPressed(false),
    onPointerLeave: () => setPressed(false),
    style: {
      boxSizing: 'border-box',
      width: '100%',
      minHeight: 'var(--touch-min)',
      background: 'var(--neutral-900)',
      color: 'var(--on-primary)',
      padding: '0 16px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: isRtl ? 'flex-end' : 'flex-start',
      textAlign: isRtl ? 'right' : 'left',
      cursor: 'pointer',
      userSelect: 'none',
      opacity: pressed ? 0.92 : 1,
      transition: 'opacity 120ms ease',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-secondary)',
      fontWeight: 'var(--weight-regular)',
      lineHeight: 'var(--lh-secondary)',
      ...style
    }
  }, rest), message);
}
Object.assign(__ds_scope, { Snackbar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Snackbar.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/AppBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function IconTap({
  name,
  label,
  onClick
}) {
  const [pressed, setPressed] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": label,
    onClick: onClick,
    onPointerDown: () => setPressed(true),
    onPointerUp: () => setPressed(false),
    onPointerLeave: () => setPressed(false),
    style: {
      width: 40,
      height: 40,
      flexShrink: 0,
      appearance: 'none',
      border: 'none',
      background: 'transparent',
      borderRadius: 'var(--radius-full)',
      cursor: 'pointer',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      opacity: pressed ? 0.7 : 1,
      transition: 'opacity 120ms ease'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
    name: name,
    size: 24,
    color: "var(--on-primary)"
  }));
}

/**
 * AppBar — 56dp red top bar, no shadow. Home shows the wordmark + LangToggle;
 * session shows back arrow, ellipsised chart title, LangToggle + reset. The
 * back arrow flips direction and side in RTL.
 */
function AppBar({
  variant = 'home',
  title = '',
  lang = 'en',
  onLangChange,
  onBack,
  onReset,
  dir,
  statusBar = false,
  style = {},
  ...rest
}) {
  const isRtl = dir === 'rtl' || lang === 'ar';
  const bar = /*#__PURE__*/React.createElement("div", _extends({
    dir: isRtl ? 'rtl' : 'ltr',
    style: {
      boxSizing: 'border-box',
      width: '100%',
      height: 'var(--appbar-height)',
      background: 'var(--primary-600)',
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      padding: variant === 'home' ? '0 16px' : '0 8px',
      ...style
    }
  }, rest), variant === 'home' ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-heading)',
      fontWeight: 'var(--weight-bold)',
      color: 'var(--on-primary)',
      flex: 1
    }
  }, "ResQRules"), /*#__PURE__*/React.createElement(__ds_scope.LangToggle, {
    value: lang,
    onChange: onLangChange
  })) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(IconTap, {
    name: isRtl ? 'arrow-right' : 'arrow-left',
    label: "Back",
    onClick: onBack
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      minWidth: 0,
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-heading)',
      fontWeight: 'var(--weight-semibold)',
      color: 'var(--on-primary)',
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      textAlign: 'center'
    }
  }, title), /*#__PURE__*/React.createElement(__ds_scope.LangToggle, {
    value: lang,
    onChange: onLangChange
  }), /*#__PURE__*/React.createElement(IconTap, {
    name: "rotate-ccw",
    label: "Reset session",
    onClick: onReset
  })));
  if (!statusBar) return bar;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 24,
      background: 'var(--primary-600)'
    }
  }), bar);
}
Object.assign(__ds_scope, { AppBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/AppBar.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/BottomSheet.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const STR = {
  en: {
    title: 'Reset Session',
    resetChart: 'Reset this chart',
    chooseChart: 'Choose a different chart',
    chooseSub: 'Return to chart list',
    cancel: 'Cancel'
  },
  ar: {
    title: 'إعادة تشغيل الجلسة',
    resetChart: 'إعادة ضبط هذا المخطط',
    chooseChart: 'اختر مخططاً مختلفاً',
    chooseSub: 'العودة إلى قائمة المخططات',
    cancel: 'إلغاء'
  }
};
function Divider() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      height: 1,
      background: 'var(--neutral-100)'
    }
  });
}
function Row({
  title,
  sub,
  color,
  onClick,
  isRtl
}) {
  const [pressed, setPressed] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onClick,
    onPointerDown: () => setPressed(true),
    onPointerUp: () => setPressed(false),
    onPointerLeave: () => setPressed(false),
    style: {
      appearance: 'none',
      border: 'none',
      width: '100%',
      minHeight: 64,
      background: pressed ? 'var(--neutral-100)' : 'transparent',
      cursor: 'pointer',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: isRtl ? 'flex-end' : 'flex-start',
      gap: 2,
      padding: '0 20px',
      textAlign: isRtl ? 'right' : 'left',
      transition: 'background 100ms ease'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-body-bold)',
      fontWeight: 'var(--weight-semibold)',
      lineHeight: 'var(--lh-body-bold)',
      color
    }
  }, title), sub != null && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-secondary)',
      fontWeight: 'var(--weight-regular)',
      lineHeight: 'var(--lh-secondary)',
      color: 'var(--neutral-600)'
    }
  }, sub));
}

/**
 * BottomSheet — Reset Session sheet. Slides up, radius-lg top corners, level-3
 * shadow. Handle, title, two tappable rows, and a Cancel action. Pass
 * `overlay` to render the scrim + slide-up wrapper; otherwise renders the panel.
 */
function BottomSheet({
  lang = 'en',
  dir,
  chartName = 'CPR Adult',
  onResetChart,
  onChooseChart,
  onCancel,
  overlay = false,
  visible = true,
  style = {},
  ...rest
}) {
  const isRtl = dir === 'rtl' || lang === 'ar';
  const t = STR[lang] || STR.en;
  const panel = /*#__PURE__*/React.createElement("div", _extends({
    dir: isRtl ? 'rtl' : 'ltr',
    style: {
      boxSizing: 'border-box',
      width: '100%',
      background: 'var(--neutral-000)',
      borderTopLeftRadius: 'var(--radius-lg)',
      borderTopRightRadius: 'var(--radius-lg)',
      boxShadow: 'var(--elevation-sheet)',
      paddingBottom: 8,
      transform: overlay ? visible ? 'translateY(0)' : 'translateY(100%)' : undefined,
      transition: overlay ? 'transform 240ms ease-out' : undefined,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'center',
      paddingTop: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 32,
      height: 4,
      borderRadius: 'var(--radius-full)',
      background: 'var(--neutral-300)'
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      margin: 16,
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-heading)',
      fontWeight: 'var(--weight-semibold)',
      lineHeight: 'var(--lh-heading)',
      color: 'var(--color-text)',
      textAlign: isRtl ? 'right' : 'left'
    }
  }, t.title), /*#__PURE__*/React.createElement(Divider, null), /*#__PURE__*/React.createElement(Row, {
    title: t.resetChart,
    sub: chartName,
    color: "var(--primary-600)",
    onClick: onResetChart,
    isRtl: isRtl
  }), /*#__PURE__*/React.createElement(Divider, null), /*#__PURE__*/React.createElement(Row, {
    title: t.chooseChart,
    sub: t.chooseSub,
    color: "var(--neutral-900)",
    onClick: onChooseChart,
    isRtl: isRtl
  }), /*#__PURE__*/React.createElement(Divider, null), /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onCancel,
    style: {
      appearance: 'none',
      border: 'none',
      background: 'transparent',
      width: '100%',
      minHeight: 'var(--touch-min)',
      cursor: 'pointer',
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--text-label)',
      fontWeight: 'var(--weight-semibold)',
      lineHeight: 'var(--lh-label)',
      color: 'var(--neutral-600)'
    }
  }, t.cancel));
  if (!overlay) return panel;
  return /*#__PURE__*/React.createElement("div", {
    onClick: onCancel,
    style: {
      position: 'absolute',
      inset: 0,
      background: 'var(--color-scrim)',
      display: 'flex',
      alignItems: 'flex-end',
      opacity: visible ? 1 : 0,
      transition: 'opacity 240ms ease'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%'
    },
    onClick: e => e.stopPropagation()
  }, panel));
}
Object.assign(__ds_scope, { BottomSheet });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/BottomSheet.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/DangerPanel.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const ZONES = [{
  key: 'bleeding',
  icon: 'droplet',
  en: 'Catastrophic Bleeding',
  ar: 'نزيف كارثي'
}, {
  key: 'breathing',
  icon: 'wind',
  en: 'Not Breathing',
  ar: 'لا يتنفس'
}, {
  key: 'pulse',
  icon: 'activity',
  en: 'No Pulse',
  ar: 'لا نبض'
}, {
  key: 'unconscious',
  icon: 'user',
  en: 'Unconscious',
  ar: 'فاقد الوعي'
}];

/**
 * DangerPanel — fixed bottom red bar, 64dp, level-2 (upward) shadow. Four equal
 * tap zones (icon over 10sp label), no dividers. Pressed zone darkens to
 * primary-700; `locked` dims all zones to 60% while the API responds.
 * RTL order flips automatically.
 */
function DangerPanel({
  lang = 'en',
  dir,
  locked = false,
  onZone,
  style = {},
  ...rest
}) {
  const [pressedKey, setPressedKey] = React.useState(null);
  const isRtl = dir === 'rtl' || lang === 'ar';
  return /*#__PURE__*/React.createElement("div", _extends({
    role: "group",
    "aria-label": "Emergency shortcuts",
    dir: isRtl ? 'rtl' : 'ltr',
    style: {
      boxSizing: 'border-box',
      width: '100%',
      height: 'var(--danger-panel-height)',
      background: 'var(--primary-600)',
      boxShadow: 'var(--elevation-panel)',
      display: 'flex',
      opacity: locked ? 0.6 : 1,
      pointerEvents: locked ? 'none' : 'auto',
      ...style
    }
  }, rest), ZONES.map(z => {
    const active = pressedKey === z.key;
    return /*#__PURE__*/React.createElement("button", {
      key: z.key,
      type: "button",
      "aria-label": lang === 'ar' ? z.ar : z.en,
      onClick: () => onZone && onZone(z.key),
      onPointerDown: () => setPressedKey(z.key),
      onPointerUp: () => setPressedKey(null),
      onPointerLeave: () => setPressedKey(k => k === z.key ? null : k),
      style: {
        flex: 1,
        minWidth: 0,
        appearance: 'none',
        border: 'none',
        background: active ? 'var(--primary-700)' : 'transparent',
        color: 'var(--on-primary)',
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 4,
        padding: '6px 4px',
        transition: 'background 100ms ease',
        userSelect: 'none'
      }
    }, /*#__PURE__*/React.createElement(__ds_scope.Icon, {
      name: z.icon,
      size: 20,
      color: "var(--on-primary)"
    }), /*#__PURE__*/React.createElement("span", {
      dir: isRtl ? 'rtl' : 'ltr',
      style: {
        fontFamily: 'var(--font-sans)',
        fontSize: 'var(--text-micro)',
        fontWeight: 'var(--weight-semibold)',
        lineHeight: 1.15,
        textAlign: 'center'
      }
    }, lang === 'ar' ? z.ar : z.en));
  }));
}
Object.assign(__ds_scope, { DangerPanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/DangerPanel.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Button = __ds_scope.Button;

__ds_ns.CfButton = __ds_scope.CfButton;

__ds_ns.LangToggle = __ds_scope.LangToggle;

__ds_ns.OutlinedButton = __ds_scope.OutlinedButton;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.PageCitation = __ds_scope.PageCitation;

__ds_ns.TierBadge = __ds_scope.TierBadge;

__ds_ns.UrgencyBadge = __ds_scope.UrgencyBadge;

__ds_ns.Icon = __ds_scope.Icon;

__ds_ns.LoadingBar = __ds_scope.LoadingBar;

__ds_ns.OverrideToast = __ds_scope.OverrideToast;

__ds_ns.Snackbar = __ds_scope.Snackbar;

__ds_ns.AppBar = __ds_scope.AppBar;

__ds_ns.BottomSheet = __ds_scope.BottomSheet;

__ds_ns.DangerPanel = __ds_scope.DangerPanel;

})();
