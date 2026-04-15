# utils.py
import streamlit as st


def inject_css():
    st.markdown("""
    <style>

    /* =========================================================
       ROOT DESIGN SYSTEM (TOKENS)
    ========================================================= */
    :root {

      /* ================= COLORS ================= */

      --white: #ffffff;
      --black: #000000;

      --bg-primary: #0f172a;
      --bg-secondary: #1e293b;
      --bg-tertiary: #334155;
      --bg-hover: #334155;

      --text-primary: #f1f5f9;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --text-inverse: #0f172a;

      --brand-primary: #6366f1;
      --brand-primary-hover: #4f46e5;
      --brand-primary-light: #818cf8;

      --success: #22c55e;
      --error: #ef4444;
      --warning: #f59e0b;
      --info: #64748b;

      --border-default: #475569;
      --border-light: rgba(255, 255, 255, 0.08);

      /* ================= TYPOGRAPHY ================= */

      --font-family: "Inter", "Geist", system-ui, sans-serif;

      --text-xs: 12px;
      --text-sm: 14px;
      --text-md: 16px;
      --text-lg: 20px;
      --text-xl: 24px;
      --text-2xl: 32px;

      --font-normal: 400;
      --font-medium: 500;
      --font-semibold: 600;
      --font-bold: 700;

      --leading-normal: 1.5;
      --leading-tight: 1.2;

      /* ================= SPACING ================= */

      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-5: 24px;
      --space-6: 32px;
      --space-7: 48px;

      /* ================= RADIUS ================= */

      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;

      /* ================= SHADOW ================= */

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
      --shadow-md: 0 4px 10px rgba(0, 0, 0, 0.12);

      /* ================= ANIMATION ================= */

      --anim-fast: 150ms;
      --anim-normal: 250ms;
      --ease-standard: cubic-bezier(0.16, 1, 0.3, 1);

      /* ================= LAYOUT ================= */

      --container-width: 1200px;
      --header-height: 64px;
      --bottom-bar-height: 70px;
    }


    /* =========================================================
       GLOBAL BASE
    ========================================================= */

    html, body {
        margin: 0;
        padding: 0;
        font-family: var(--font-family);
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    .stApp {
        background: var(--bg-primary);
    }

    div[data-testid="stAppViewContainer"] {
        background: var(--bg-primary);
    }


    /* =========================================================
       SIDEBAR
    ========================================================= */

    div[data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-default);
    }


    /* =========================================================
       TYPOGRAPHY
    ========================================================= */

    h1 { font-size: var(--text-2xl); font-weight: var(--font-bold); }
    h2 { font-size: var(--text-xl); font-weight: var(--font-semibold); }
    h3 { font-size: var(--text-lg); font-weight: var(--font-semibold); }
    h4 { font-size: var(--text-md); font-weight: var(--font-medium); }

    p {
        font-size: var(--text-md);
        line-height: var(--leading-normal);
        color: var(--text-secondary);
    }


    /* =========================================================
       HEADER SYSTEM
    ========================================================= */

    .header {
        position: sticky;
        top: 0;
        z-index: 1000;

        height: var(--header-height);

        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 0 var(--space-4);

        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);

        border-bottom: 1px solid var(--border-default);
    }

    .header-left {
        font-size: var(--text-lg);
        font-weight: var(--font-semibold);
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }

    .header-chip {
        padding: 4px 10px;
        border-radius: var(--radius-md);
        background: var(--bg-tertiary);
        font-size: var(--text-xs);
        color: var(--text-secondary);
    }

    /* HEADER SUBTITLE */

    .header-subtitle {
        font-size: var(--text-xs);
        color: var(--text-muted);
        margin-top: 2px;
    }


    /* =========================================================
       BUTTON SYSTEM
    ========================================================= */

    .stButton > button {
        border-radius: var(--radius-md);
        padding: 10px 16px;
        font-weight: var(--font-medium);
        border: none;
        cursor: pointer;
        transition: all var(--anim-normal) var(--ease-standard);
        background: var(--brand-primary);
        color: var(--white);
    }

    .stButton > button:hover {
        background: var(--brand-primary-hover);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    .stButton > button:active {
        transform: scale(0.98);
    }

    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    /* VARIANTS */

    .btn-primary button {
        background: var(--brand-primary);
        color: var(--white);
    }

    .btn-secondary button {
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }

    .btn-ghost button {
        background: transparent;
        color: var(--text-secondary);
    }


    /* =========================================================
       INPUT SYSTEM
    ========================================================= */

    input, textarea {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-default) !important;
        border-radius: var(--radius-sm) !important;
        padding: var(--space-2) !important;
    }

    input:focus, textarea:focus {
        border-color: var(--brand-primary) !important;
    }


    /* =========================================================
       CARD SYSTEM
    ========================================================= */

    .custom-card {
        background: var(--bg-secondary);
        padding: var(--space-4);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
        transition: all var(--anim-normal) var(--ease-standard);
    }

    .custom-card:hover {
        background: var(--bg-hover);
        transform: translateY(-2px);
    }

    .card-title {
        font-size: var(--text-lg);
        font-weight: var(--font-semibold);
        margin-bottom: var(--space-1);
    }

    .card-subtitle {
        font-size: var(--text-sm);
        color: var(--text-muted);
        margin-bottom: var(--space-2);
    }

    .card-desc {
        font-size: var(--text-md);
        color: var(--text-secondary);
    }

    .card-badge {
        font-size: var(--text-xs);
        padding: 2px 8px;
        border-radius: var(--radius-sm);
        background: var(--bg-tertiary);
        float: right;
    }


    /* =========================================================
       BOTTOM BAR
    ========================================================= */

    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: var(--bottom-bar-height);
        background: var(--bg-secondary);
        border-top: 1px solid var(--border-default);
        display: flex;
        align-items: center;
        justify-content: space-around;
        padding: 0 var(--space-4);
        z-index: 999;
    }

    .bottom-nav-btn button {
        width: 100%;
        height: 48px;
        border-radius: var(--radius-md);
        background: transparent;
        color: var(--text-secondary);
    }

    .bottom-nav-btn.active button {
        background: var(--brand-primary);
        color: var(--white);
    }


    /* =========================================================
       SCROLLBAR
    ========================================================= */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--bg-tertiary);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--brand-primary);
    }

    /* =========================================================
    PRICING SECTION
    ========================================================= */

    .pricing-container {
        margin-top: var(--space-6);
    }

    .pricing-grid {
        display: flex;
        gap: var(--space-4);
        justify-content: space-between;
    }

    .pricing-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: var(--space-5);
        flex: 1;
        transition: all var(--anim-normal) var(--ease-standard);
        position: relative;
    }

    .pricing-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
    }

    .pricing-card.highlight {
        border: 2px solid var(--brand-primary);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.35);
    }

    .pricing-badge {
        position: absolute;
        top: -10px;
        right: 16px;
        background: var(--brand-primary);
        color: var(--white);
        font-size: var(--text-xs);
        padding: 4px 10px;
        border-radius: var(--radius-sm);
    }

    .pricing-title {
        font-size: var(--text-lg);
        font-weight: var(--font-semibold);
    }

    .pricing-price {
        font-size: var(--text-2xl);
        font-weight: var(--font-bold);
        margin: var(--space-2) 0;
    }

    .pricing-credits {
        font-size: var(--text-sm);
        color: var(--text-muted);
        margin-bottom: var(--space-3);
    }

    .pricing-features {
        margin-top: var(--space-3);
        margin-bottom: var(--space-4);
    }

    .pricing-feature {
        font-size: var(--text-sm);
        color: var(--text-secondary);
        margin-bottom: 6px;
    }

    .pricing-cta {
        margin-top: auto;
    }

    </style>
    """, unsafe_allow_html=True)