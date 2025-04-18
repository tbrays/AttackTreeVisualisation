"""
assessment.py

Generates summary statistics and visual elements for the risk assessment panel.

This module provides a function to update the summary UI based on current threat
likelihoods within an attack tree. It displays key metrics such as:
- Average likelihood across non-root nodes
- The highest-risk node
- Risk breakdown by parent category
- A warning panel for high-risk nodes (likelihood ≥ 75%)

Functions:
- update_assessment(attack_tree, summary): Updates the UI with the latest risk metrics.
"""

from collections import defaultdict
from nicegui import ui

def update_assessment(attack_tree, summary):
    """
    Update the UI assessment panel with risk summaries.

    Displays:
        - Average likelihood across all non-root nodes.
        - The most vulnerable node.
        - Risk breakdown per parent branch.
        - A highlighted list of high-risk nodes (likelihood ≥ 75%).
    """
	
    summary.clear()
    non_root = [n for n in attack_tree if n["parent"] != ""]
    values = [n["likelihood"] for n in attack_tree if "likelihood" in n]

    avg_risk = sum(values) / len(values) if values else 0
    likelihood_nodes = [n for n in non_root if "likelihood" in n]
    highest = max(likelihood_nodes, key=lambda n: n["likelihood"], default=None)
    high_risk_nodes = [n for n in non_root if n.get("likelihood", 0) >= 75]

    with summary:
        with ui.row().classes("w-full justify-between gap-8"):
            with ui.column().classes("flex-1"):
                ui.label("Threat Summary").classes("text-xl font-semibold mb-2")
                ui.label(f"Average Risk Per Node: {avg_risk:.1f}%")
                if highest:
                    ui.label(f"Most Vulnerable Node: {highest['label']} ({highest['likelihood']}%)")

            with ui.column().classes("flex-1"):
                ui.label("Risk Breakdown by Branch").classes("text-xl font-semibold mb-2")
                grouped = defaultdict(list)
                for node in non_root:
                    if "likelihood" in node:
                        grouped[node["parent"]].append(node["likelihood"])
                for parent, risks in grouped.items():
                    avg = sum(risks) / len(risks)
                    ui.label(f"• {parent}: {avg:.1f}%")

        if high_risk_nodes:
            with ui.row().classes(
                "w-full bg-red-100 border border-red-400 rounded-md p-4 mt-4"
            ):
                with ui.column().classes("w-full"):
                    ui.label(
                        "High Risk Nodes (≥ 75%)"
                    ).classes("text-lg font-semibold text-red-700 mb-2")
                    for node in high_risk_nodes:
                        ui.label(
                            f"• {node['label']} — {node['likelihood']}%"
                        ).classes("text-red-800")
											