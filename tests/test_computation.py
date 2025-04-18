import pytest
import copy
from computation import is_leaf, get_children, compute_likelihood

# Sample attack trees
basic_tree = [
		{"label": "Root", "parent": "", "gate": "OR"},
		{"label": "A", "parent": "Root", "likelihood": 60},
		{"label": "B", "parent": "Root", "likelihood": 40}
]

and_tree = [
		{"label": "Root", "parent": "", "gate": "AND"},
		{"label": "A", "parent": "Root", "likelihood": 50},
		{"label": "B", "parent": "Root", "likelihood": 80}
]

nested_tree = [
		{"label": "Root", "parent": "", "gate": "OR"},
		{"label": "Mid", "parent": "Root", "gate": "AND"},
		{"label": "Leaf1", "parent": "Mid", "likelihood": 70},
		{"label": "Leaf2", "parent": "Mid", "likelihood": 60}
]

# Tests
def test_is_leaf_true():
		tree = copy.deepcopy(basic_tree)
		assert is_leaf("A", tree) is True

def test_is_leaf_false():
		tree = copy.deepcopy(basic_tree)
		assert is_leaf("Root", tree) is False

def test_get_children():
		tree = copy.deepcopy(basic_tree)
		children = get_children("Root", tree)
		assert len(children) == 2
		assert {child["label"] for child in children} == {"A", "B"}

def test_compute_likelihood_or_gate():
    tree = copy.deepcopy(basic_tree)
    result = compute_likelihood("Root", tree)
    expected = 76.0
    assert result == pytest.approx(expected)

def test_compute_likelihood_and_gate():
		tree = copy.deepcopy(and_tree)
		result = compute_likelihood("Root", tree)
		expected = 0.5 * 0.8  # = 0.4 → 40.0%
		assert result == pytest.approx(40.0)

def test_compute_likelihood_nested():
		tree = copy.deepcopy(nested_tree)
		result = compute_likelihood("Root", tree)
		mid = 0.7 * 0.6  # AND gate = 0.42
		expected = mid  # OR with one child = 42.0%
		assert result == pytest.approx(42.0)

def test_compute_likelihood_leaf_only():
		tree = [{"label": "Single", "parent": "", "likelihood": 75}]
		result = compute_likelihood("Single", tree)
		assert result == 75

def test_compute_likelihood_missing_node():
		tree = copy.deepcopy(basic_tree)
		result = compute_likelihood("NonExistent", tree)
		assert result == 0
