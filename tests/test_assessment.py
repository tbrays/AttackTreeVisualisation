import pytest
from collections import defaultdict

# Sample tree for testing
sample_tree = [
		{"label": "Root", "parent": "", "gate": "OR"},
		{"label": "BranchA", "parent": "Root", "gate": "OR"},
		{"label": "Leaf1", "parent": "BranchA", "likelihood": 60},
		{"label": "Leaf2", "parent": "BranchA", "likelihood": 80},
		{"label": "BranchB", "parent": "Root", "gate": "OR"},
		{"label": "Leaf3", "parent": "BranchB", "likelihood": 90},
]

# Helper function to replicate summary logic from assessment.py
def extract_summary(tree):
		non_root = [n for n in tree if n["parent"] != ""]
		values = [n["likelihood"] for n in tree if "likelihood" in n]
		avg_risk = sum(values) / len(values) if values else 0

		likelihood_nodes = [n for n in non_root if "likelihood" in n]
		highest = max(likelihood_nodes, key=lambda n: n["likelihood"], default=None)

		grouped = defaultdict(list)
		for node in non_root:
				if "likelihood" in node:
						grouped[node["parent"]].append(node["likelihood"])
		branch_risks = {
				parent: sum(risks) / len(risks) for parent, risks in grouped.items()
		}

		high_risk_nodes = [n for n in non_root if n.get("likelihood", 0) >= 75]

		return {
				"average": avg_risk,
				"highest": highest,
				"branch_risks": branch_risks,
				"high_risk_nodes": high_risk_nodes
		}

# Tests
def test_average_risk():
		result = extract_summary(sample_tree)
		assert result["average"] == pytest.approx((60 + 80 + 90) / 3)

def test_highest_risk_node():
		result = extract_summary(sample_tree)
		assert result["highest"]["label"] == "Leaf3"
		assert result["highest"]["likelihood"] == 90

def test_branch_risks():
		result = extract_summary(sample_tree)
		assert result["branch_risks"]["BranchA"] == pytest.approx(70.0)
		assert result["branch_risks"]["BranchB"] == pytest.approx(90.0)

def test_high_risk_nodes():
		result = extract_summary(sample_tree)
		high_risks = {n["label"] for n in result["high_risk_nodes"]}
		assert high_risks == {"Leaf2", "Leaf3"}
