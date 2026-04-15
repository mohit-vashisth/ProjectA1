# input.py
import streamlit as st
from typing import List, Any, Optional


# ----------------------------
# TEXT INPUT
# ----------------------------
def text_input(
    label: str,
    key: str,
    placeholder: str = "",
    value: str = "",
    disabled: bool = False,
    help: Optional[str] = None,
) -> str:

    return st.text_input(
        label=label,
        key=key,
        value=value,
        placeholder=placeholder,
        disabled=disabled,
        help=help,
    )


# ----------------------------
# TEXTAREA INPUT
# ----------------------------
def textarea_input(
    label: str,
    key: str,
    placeholder: str = "",
    value: str = "",
    height: int = 120,
    disabled: bool = False,
) -> str:

    return st.text_area(
        label=label,
        key=key,
        value=value,
        placeholder=placeholder,
        height=height,
        disabled=disabled,
    )


# ----------------------------
# SELECT INPUT
# ----------------------------
def select_input(
    label: str,
    options: List[Any],
    key: str,
    index: int = 0,
    disabled: bool = False,
    help: Optional[str] = None,
):

    return st.selectbox(
        label=label,
        options=options,
        index=index,
        key=key,
        disabled=disabled,
        help=help,
    )


# ----------------------------
# MULTI SELECT
# ----------------------------
def multiselect_input(
    label: str,
    options: List[Any],
    key: str,
    default: Optional[List[Any]] = None,
):

    return st.multiselect(
        label=label,
        options=options,
        default=default,
        key=key,
    )


# ----------------------------
# SLIDER INPUT
# ----------------------------
def slider_input(
    label: str,
    min_value: float,
    max_value: float,
    key: str,
    value: float,
    step: float = 0.1,
):

    return st.slider(
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step,
        key=key,
    )


# ----------------------------
# TOGGLE INPUT
# ----------------------------
def toggle_input(
    label: str,
    key: str,
    value: bool = False,
):

    return st.toggle(
        label=label,
        value=value,
        key=key,
    )


# ----------------------------
# FILE UPLOADER
# ----------------------------
def file_uploader_input(
    label: str,
    key: str,
    type: Optional[List[str]] = None,
    accept_multiple: bool = False,
):

    return st.file_uploader(
        label=label,
        type=type,
        accept_multiple_files=accept_multiple,
        key=key,
    )