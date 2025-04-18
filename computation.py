"""
computation.py

Provides core logic for calculating threat likelihoods within an attack tree.

This module supports recursive aggregation of risk values from leaf nodes upward,
based on logical gates defined at each parent node. 

Functions:
- is_leaf(label, attack_tree): Returns True if the node has no children.
- get_children(label, attack_tree): Retrieves immediate child nodes of a given parent.
- compute_likelihood(label, attack_tree): Recursively calculates the likelihood of a node
  based on its children and logic gate (AND/OR).
"""

def is_leaf(label, attack_tree):
    """
    Determine if a node has no children in the attack tree.
  
    Args:
        label (str): The label of the node.
        attack_tree (list[dict]): The tree structure.
  
    Returns:
        bool: True if node has no children, False otherwise.
    """
    return all(n['parent'] != label for n in attack_tree)


def get_children(label, attack_tree):
    """
    Get immediate child nodes of a given parent.
  
    Args:
        label (str): Parent node label.
        attack_tree (list[dict]): The tree structure.
  
    Returns:
        list[dict]: Child node dictionaries.
    """
    return [n for n in attack_tree if n['parent'] == label]


def compute_likelihood(label, attack_tree):
    """
    Compute likelihood of a node recursively using AND/OR logic.
  
    Args:
        label (str): The label of the node.
        attack_tree (list[dict]): The tree structure.
  
    Returns:
        float: Calculated likelihood (0–100).
    """
    node = next((n for n in attack_tree if n['label'] == label), None)
    if node is None:
        return 0

    if is_leaf(label, attack_tree):
        return node.get("likelihood", 0)

    children = get_children(label, attack_tree)
    child_probs = [compute_likelihood(child["label"], attack_tree) / 100 for child in children]

    gate = node.get("gate", "OR").upper()
    if gate == "AND":
        prob = 1
        for p in child_probs:
            prob *= p
    else:  # OR logic
        prob = 1
        for p in child_probs:
            prob *= (1 - p)
        prob = 1 - prob

    node["likelihood"] = round(prob * 100, 1)
    return node["likelihood"]
