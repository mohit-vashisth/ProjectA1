# bottom_bar.py
import streamlit as st


def _handle_navigation(route_id: str):
    st.session_state["route"] = route_id


def bottom_nav_button(
    *,
    btn_id: str,
    label: str,
    icon: str = "",
    disabled: bool = False
):
    current_route = st.session_state.get("route")
    is_active = current_route == btn_id

    class_name = "bottom-nav-btn active" if is_active else "bottom-nav-btn"

    st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)

    clicked = st.button(
        f"{icon} {label}",
        key=btn_id,
        disabled=disabled
    )

    if clicked:
        _handle_navigation(btn_id)

    st.markdown("</div>", unsafe_allow_html=True)


def bottom_bar(items: list[dict]):

    st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)

    cols = st.columns(len(items))

    for i, item in enumerate(items):
        with cols[i]:
            bottom_nav_button(
                btn_id=item["id"],
                label=item["label"],
                icon=item.get("icon", ""),
                disabled=item.get("disabled", False)
            )

    st.markdown('</div>', unsafe_allow_html=True)