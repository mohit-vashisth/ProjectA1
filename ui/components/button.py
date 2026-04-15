# button.py
import streamlit as st
from typing import Optional


def button(
    *,
    label: str,
    key: str,
    variant: str = "primary",
    icon: str = "",
    on_click=None,
    route: Optional[str] = None,
    disabled: bool = False,
):
    """
    Universal Button Component

    Supports:
    - Action button (on_click)
    - Internal navigation (route)
    """

    # -----------------------
    # VALIDATION
    # -----------------------
    if sum([bool(on_click), bool(route)]) > 1:
        raise ValueError("Only one of on_click or route should be provided")

    class_name = f"btn-{variant}"

    st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)

    clicked = st.button(
        f"{icon} {label}",
        key=key,
        disabled=disabled,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        if on_click:
            on_click()
        elif route:
            st.session_state.route = route