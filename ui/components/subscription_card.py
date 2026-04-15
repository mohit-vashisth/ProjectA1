# subscription_card.py
import streamlit as st
from ui.components.card import card
from typing import Optional
from ui.components.button import primary_button, secondary_button


def subscription_card(
    plan_id: str,
    name: str,
    price: str,
    usage: dict,
    features: Optional[list] = None,
    highlight: bool = False,
    cta_label: str = "Upgrade",
):
    """
    Reusable Subscription Card

    Args:
        plan_id: unique id
        name: plan name
        price: pricing string
        usage: dict (usage stats)
        features: list of features
        highlight: highlight card (pro plan)
        cta_label: button text
    """

    # --------------------------
    # BUILD DESCRIPTION BLOCK
    # --------------------------

    desc_lines = []

    # Price
    desc_lines.append(f"**{price}**")

    # Usage
    for k, v in usage.items():
        desc_lines.append(f"{k}: {v}")

    # Features
    if features:
        desc_lines.append("")
        for f in features:
            desc_lines.append(f"✔ {f}")

    description = "\n".join(desc_lines)

    # --------------------------
    # FOOTER (CTA)
    # --------------------------

    def footer():
        if highlight:
            primary_button(label=cta_label, key=f"{plan_id}_cta")
        else:
            secondary_button(label=cta_label, key=f"{plan_id}_cta")

    # --------------------------
    # BADGE
    # --------------------------

    badge = "Most Popular" if highlight else None

    # --------------------------
    # CARD RENDER
    # --------------------------

    card(
        title=name,
        description=description,
        footer=footer,
        badge=badge
    )