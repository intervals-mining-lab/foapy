import ast
from pathlib import Path

import pytest

PRODUCTION_MODULES = [
    "src/foapy/core/_axis_transform.py",
    "src/foapy/core/_intervals_chain_validation.py",
    "src/foapy/core/_intervals_distribution.py",
    "src/foapy/core/_intervals_tuple.py",
    "src/foapy/partials/_intervals_tuple.py",
]
ITERATION_NODES = (
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
)
DISGUISED_LOOP_CALLS = {"apply_along_axis", "vectorize"}


@pytest.mark.parametrize("relative_path", PRODUCTION_MODULES)
def test_axis_production_modules_use_vectorized_numpy(relative_path):
    source_path = Path(__file__).parents[1] / relative_path
    tree = ast.parse(source_path.read_text(), filename=str(source_path))

    iteration_nodes = [
        node for node in ast.walk(tree) if isinstance(node, ITERATION_NODES)
    ]
    disguised_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in DISGUISED_LOOP_CALLS
    ]

    assert iteration_nodes == []
    assert disguised_calls == []
