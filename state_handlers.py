"""
state_handlers.py

Provides functions to manage user interactions and update application state.

This module handles UI-triggered events such as:
- Updating likelihood values from slider input
- Recomputing the attack tree and refreshing the chart
- Resetting all values to their original state

Functions:
- update_value_by_label: Updates a leaf node’s value and refreshes the visual.
- update_chart: Recomputes and redraws the chart and summary.
- reset_all: Restores original likelihood values and slider positions.
"""

from computation import compute_likelihood, is_leaf
from visualisation import generate_figure
from assessment import update_assessment

def update_value_by_label(label, new_value, attack_tree, plot, summary):
    """
    Update likelihood value of a leaf node and refresh UI.

    Args:
        label (str): Node label.
        new_value (float): New likelihood (0–100).
        attack_tree (list[dict]): The tree data.
        plot (ui.plotly): The plotly visual object.
        summary (ui.element): The summary container.
    """
    for node in attack_tree:
        if node["label"] == label:
            node["likelihood"] = new_value
            break
    update_chart(attack_tree, plot, summary)


def update_chart(attack_tree, plot, summary):
    """
    Recompute and update chart and summary panel.

    Args:
        attack_tree (list[dict])
        plot (ui.plotly)
        summary (ui.element)
    """
    compute_likelihood("Root Attack", attack_tree)
    plot.update_figure(generate_figure(attack_tree))
    update_assessment(attack_tree, summary)


def reset_all(attack_tree, original_tree, slider_refs, plot, summary):
    """
    Reset all leaf node values and sliders to original values.

    Args:
        attack_tree (list[dict])
        original_tree (list[dict])
        slider_refs (dict): Map of label → slider.
        plot (ui.plotly)
        summary (ui.element)
    """
    for orig in original_tree:
        for node in attack_tree:
            if node["label"] == orig["label"] and is_leaf(node["label"], attack_tree):
                node["likelihood"] = orig["likelihood"]
                if node["label"] in slider_refs:
                    slider_refs[node["label"]].value = orig["likelihood"]

    compute_likelihood("Root Attack", attack_tree)
    update_chart(attack_tree, plot, summary)
