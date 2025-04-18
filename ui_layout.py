"""
ui_layout.py

Defines the user interface layout for the threat modelling application using NiceGUI.

This module builds the full UI, including:
- A sidebar with sliders for adjusting likelihoods of leaf nodes.
- A main area displaying an interactive Plotly sunburst chart.
- A summary panel showing calculated risk metrics.
- A reset button to restore original values.

Functions:
- build_ui(attack_tree, original_tree)
"""

from nicegui import ui
from computation import is_leaf, compute_likelihood
from visualisation import generate_figure
from assessment import update_assessment
from state_handlers import update_value_by_label, reset_all

def build_ui(attack_tree, original_tree):
    """
    Construct the main UI layout for the attack tree visualisation.
  
    Builds the following UI structure:
        - Top banner (title and subtitle).
        - Left sidebar (sliders for adjusting leaf node likelihoods).
        - Right content (Plotly sunburst chart and summary panel).
        - Footer (branding information).
  
    Returns:
        None
    """
    slider_refs = {}

    with ui.column().classes("w-full h-screen"):

        with ui.row().classes("w-full bg-blue-700 text-white p-6 shadow-md"):
            with ui.column().classes("w-full"):
                ui.label("Attack Tree Visualisation").classes("text-3xl font-bold tracking-wide")
                ui.label("Interactive Risk Assessment Tool").classes("text-base text-blue-100")

        with ui.row().classes("w-full flex-1 items-stretch no-wrap"):

            with ui.column().classes("w-1/4 p-4 bg-gray-50 overflow-auto border-r border-gray-300"):
                ui.label("Adjust Likelihoods (%)").classes("text-lg font-semibold mb-4")

                for node in attack_tree:
                    root_label = next((n["label"] for n in attack_tree if n["parent"] == ""), None)
                    if node["label"] != root_label and is_leaf(node["label"], attack_tree):
                        with ui.row().classes("items-center w-full mb-3"):
                            ui.label(node["label"]).classes("text-sm whitespace-nowrap mr-2")
                            slider = ui.slider(
                                min=0, max=100, value=node["likelihood"], step=1,
                                on_change=lambda e, label=node["label"]: update_value_by_label(
                                    label, e.value, attack_tree, plot, summary
                                )
                            ).props('label-always instant').classes("w-full")
                            slider_refs[node["label"]] = slider

                ui.button("Reset All", on_click=lambda: reset_all(
                    attack_tree, original_tree, slider_refs, plot, summary
                )).classes("mt-6 bg-blue-600 text-white w-full")

            with ui.column().classes("w-3/4 p-4 h-full overflow-auto"):
								# Global variables required for UI updates from external event handlers
                global plot
                compute_likelihood("Root Attack", attack_tree)
                plot = ui.plotly(generate_figure(attack_tree)).classes("w-full h-[60%]")

                global summary
                summary = ui.row().classes("w-full mt-6 gap-8")
                update_assessment(attack_tree, summary)

        with ui.row().classes("w-full bg-gray-200 text-gray-700 p-3 justify-center border-t"):
            ui.label("Built with NiceGUI + Plotly").classes("text-sm")
