# header.py
import streamlit as st
from ui.components.button import button


# ----------------------------
# CREDIT INFO HANDLER
# ----------------------------
def _show_credit_info():
    st.info(
        """
💡 Credit Usage:

• 1 credit = 1 voice generation
• Credits are consumed per generation
• Upgrade your plan for more credits

(Current system: 30 credits total)
"""
    )


# ----------------------------
# HEADER COMPONENT
# ----------------------------
def render_header(credits: int = 30):

    st.markdown('<div class="header">', unsafe_allow_html=True)

    col1, col2 = st.columns([7, 3])

    # ----------------------------
    # LEFT → BRAND
    # ----------------------------
    with col1:
        st.markdown(
            """
            <div class="header-left">
                Mirage
                <div class="header-subtitle">AI Voice Studio</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ----------------------------
    # RIGHT → ACTIONS
    # ----------------------------
    with col2:

        colA, colB = st.columns([3, 1])

        # Credits
        with colA:
            button(
                label=f"{credits} Credits",
                key="credits_btn",
                variant="ghost",
                icon="💳",
                on_click=_show_credit_info
            )

        # Profile
        with colB:
            button(
                label="",
                key="profile_btn",
                variant="ghost",
                icon="👤"
            )

    st.markdown('</div>', unsafe_allow_html=True)