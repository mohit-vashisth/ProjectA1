import streamlit as st

def inject_css(theme: str = "dark"):
    """
    Injects CSS with light/dark theme variables.
    theme: 'dark' or 'light'
    """
    # Define colour tokens for both themes
    dark_tokens = """
        --bg-primary: #0B1120;
        --bg-secondary: #1E293B;
        --bg-tertiary: #334155;
        --bg-hover: #475569;
        --text-primary: #F8FAFC;
        --text-secondary: #E2E8F0;
        --text-muted: #94A3B8;
        --border-default: #3B82F6;
        --border-light: rgba(255, 255, 255, 0.08);
        --brand-primary: #3B82F6;
        --brand-primary-hover: #2563EB;
        --brand-primary-light: #60A5FA;
        --success: #10B981;
        --error: #EF4444;
        --warning: #F59E0B;
        --info: #64748B;
    """
    light_tokens = """
        --bg-primary: #F8FAFC;
        --bg-secondary: #FFFFFF;
        --bg-tertiary: #F1F5F9;
        --bg-hover: #E2E8F0;
        --text-primary: #0F172A;
        --text-secondary: #334155;
        --text-muted: #64748B;
        --border-default: #3B82F6;
        --border-light: rgba(0, 0, 0, 0.06);
        --brand-primary: #3B82F6;
        --brand-primary-hover: #2563EB;
        --brand-primary-light: #93C5FD;
        --success: #059669;
        --error: #DC2626;
        --warning: #D97706;
        --info: #475569;
    """

    tokens = dark_tokens if theme == "dark" else light_tokens

    st.markdown(f"""
    <style>
    :root {{
        /* ========== BASE TOKENS ========== */
        --white: #FFFFFF;
        --black: #000000;

        /* ========== THEME TOKENS ========== */
        {tokens}

        /* ========== TYPOGRAPHY ========== */
        --font-family: "Inter", system-ui, -apple-system, sans-serif;
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

        /* ========== SPACING ========== */
        --space-1: 4px;
        --space-2: 8px;
        --space-3: 12px;
        --space-4: 16px;
        --space-5: 24px;
        --space-6: 32px;
        --space-7: 48px;

        /* ========== RADIUS ========== */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;

        /* ========== SHADOW ========== */
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
        --shadow-md: 0 8px 20px rgba(0,0,0,0.1);
        --shadow-lg: 0 12px 30px rgba(0,0,0,0.15);

        /* ========== ANIMATION ========== */
        --anim-fast: 150ms;
        --anim-normal: 250ms;
        --ease-standard: cubic-bezier(0.16, 1, 0.3, 1);

        /* ========== LAYOUT ========== */
        --container-width: 1200px;
        --header-height: 64px;
        --bottom-bar-height: 70px;
    }}

    /* ========== GLOBAL BASE ========== */
    html, body {{
        margin: 0;
        padding: 0;
        font-family: var(--font-family);
        background: var(--bg-primary);
        color: var(--text-primary);
    }}
    .stApp {{
        background: var(--bg-primary);
    }}
    div[data-testid="stAppViewContainer"] {{
        background: var(--bg-primary);
    }}

    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {{
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-light);
    }}
    section[data-testid="stSidebar"] * {{
        color: var(--text-primary) !important;
    }}

    /* ========== TYPOGRAPHY ========== */
    h1 {{ font-size: var(--text-2xl); font-weight: var(--font-bold); letter-spacing: -0.02em; }}
    h2 {{ font-size: var(--text-xl); font-weight: var(--font-semibold); letter-spacing: -0.01em; }}
    h3 {{ font-size: var(--text-lg); font-weight: var(--font-semibold); }}
    h4 {{ font-size: var(--text-md); font-weight: var(--font-medium); }}
    p {{
        font-size: var(--text-md);
        line-height: var(--leading-normal);
        color: var(--text-secondary);
    }}

    /* ========== BUTTONS ========== */
    .stButton > button {{
        border-radius: var(--radius-md) !important;
        padding: 10px 20px !important;
        font-weight: var(--font-medium) !important;
        border: none !important;
        cursor: pointer !important;
        transition: all var(--anim-normal) var(--ease-standard) !important;
        background: var(--brand-primary) !important;
        color: white !important;
        box-shadow: var(--shadow-sm) !important;
    }}
    .stButton > button:hover {{
        background: var(--brand-primary-hover) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
    }}
    .stButton > button:active {{
        transform: scale(0.98) !important;
    }}
    .stButton > button:disabled {{
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }}

    /* ========== INPUTS ========== */
    input, textarea, .stTextInput > div > div > input {{
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        padding: 10px 14px !important;
    }}
    input:focus, textarea:focus {{
        border-color: var(--brand-primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }}

    /* ========== CARDS ========== */
    .custom-card {{
        background: var(--bg-secondary);
        padding: var(--space-5);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
        transition: all var(--anim-normal) var(--ease-standard);
    }}
    .custom-card:hover {{
        background: var(--bg-hover);
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
    }}
    .card-title {{
        font-size: var(--text-lg);
        font-weight: var(--font-semibold);
        margin-bottom: var(--space-2);
    }}
    .card-badge {{
        display: inline-block;
        font-size: var(--text-xs);
        padding: 4px 10px;
        border-radius: 20px;
        background: var(--bg-tertiary);
        color: var(--text-secondary);
        font-weight: var(--font-medium);
    }}

    /* ========== STATS GRID ========== */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: var(--space-4);
        margin: var(--space-5) 0;
    }}
    .stat-card {{
        background: var(--bg-secondary);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        display: flex;
        align-items: center;
        gap: var(--space-4);
        border: 1px solid var(--border-light);
        transition: all var(--anim-normal);
    }}
    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }}
    .stat-icon {{
        width: 48px;
        height: 48px;
        border-radius: var(--radius-md);
        background: var(--brand-primary-light);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
    }}
    .stat-value {{
        font-size: 28px;
        font-weight: var(--font-bold);
        line-height: 1.2;
        color: var(--text-primary);
    }}
    .stat-label {{
        font-size: var(--text-sm);
        color: var(--text-muted);
    }}

    /* ========== QUICK ACTIONS ========== */
    .quick-actions {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-5);
        margin-bottom: var(--space-6);
    }}
    .action-card {{
        background: var(--bg-secondary);
        border-radius: var(--radius-lg);
        padding: var(--space-5);
        border: 1px solid var(--border-light);
        text-align: center;
        transition: all var(--anim-normal);
        cursor: pointer;
    }}
    .action-card:hover {{
        background: var(--bg-hover);
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
        border-color: var(--brand-primary);
    }}
    .action-icon {{
        font-size: 36px;
        margin-bottom: var(--space-3);
    }}
    .action-card h4 {{
        margin: 0 0 var(--space-2) 0;
        font-size: var(--text-md);
    }}
    .action-card p {{
        margin: 0;
        font-size: var(--text-sm);
        color: var(--text-muted);
    }}

    /* ========== FILE GRID ========== */
    .files-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: var(--space-4);
        margin-bottom: var(--space-6);
    }}
    .file-card {{
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
        padding: var(--space-4);
        display: flex;
        align-items: center;
        gap: var(--space-3);
        border: 1px solid var(--border-light);
        transition: background var(--anim-fast);
    }}
    .file-card:hover {{
        background: var(--bg-tertiary);
    }}
    .file-icon {{
        font-size: 24px;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--bg-tertiary);
        border-radius: var(--radius-sm);
    }}
    .file-name {{
        font-weight: var(--font-medium);
        margin-bottom: 2px;
    }}
    .file-meta {{
        font-size: var(--text-xs);
        color: var(--text-muted);
    }}

    /* ========== SECTION HEADER ========== */
    .section-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: var(--space-6) 0 var(--space-4) 0;
    }}
    .section-header h3 {{
        margin: 0;
    }}
    .view-all {{
        color: var(--brand-primary);
        text-decoration: none;
        font-size: var(--text-sm);
        font-weight: var(--font-medium);
    }}

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-thumb {{
        background: var(--bg-tertiary);
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--brand-primary);
    }}

    /* ========== BLOCK CONTAINER ========== */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: var(--container-width) !important;
        margin: 0 auto !important;
    }}

    /* ========== MISC ========== */
    hr {{
        border-color: var(--border-light);
    }}
    </style>
    """, unsafe_allow_html=True)