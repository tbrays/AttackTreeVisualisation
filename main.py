"""
main.py

Entry point for the threat modelling application.

This script loads an attack tree from a JSON file and starts a NiceGUI interface,
allowing users to visualise risks, adjust node likelihoods and see live risk summaries.
"""

import json
import copy
from nicegui import ui
from ui_layout import build_ui

def main():
    """
    Launches the threat modelling application.

    Loads an attack tree from a JSON file and starts a NiceGUI interface where users can:
    - Visualise the attack tree using a Plotly sunburst chart.
    - Adjust likelihoods of leaf nodes via sliders.
    - View real time risk summaries.

    Run this file to start the app:
        python main.py
    """
    # Load the attack tree from a JSON file, switch to pre/post trees as needed
    with open('json/attack_tree.json', 'r', encoding='utf-8') as f:
        attack_tree = json.load(f)

    # Preserve the original tree for reset functionality
    original_tree = copy.deepcopy(attack_tree)

    # Build the UI and run the app
    build_ui(attack_tree, original_tree)
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
