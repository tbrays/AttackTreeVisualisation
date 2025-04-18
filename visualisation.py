"""
visualisation.py

Generates visual representations of the attack tree using Plotly.

This module provides functionality to create an interactive sunburst chart
based on the hierarchical structure and likelihood values of the threat model.

Functions:
- generate_figure(attack_tree): Returns a Plotly sunburst chart visualising
  node relationships and likelihood values from the attack tree.
"""

import plotly.graph_objs as go

def generate_figure(attack_tree):
    """
    Generate Plotly sunburst chart of attack tree.

    Args:
        attack_tree (list[dict]): The current attack tree data.

    Returns:
        plotly.graph_objs.Figure: Sunburst chart object.
    """
    labels = [n["label"] for n in attack_tree]
    parents = [n["parent"] for n in attack_tree]
    values = [n["likelihood"] for n in attack_tree if "likelihood" in n]


    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues='remainder',
        hoverinfo='label+value+percent parent',
        maxdepth=-1
    ))

    fig.update_layout(margin={"t": 10, "l": 10, "r": 10, "b": 10})
    return fig
