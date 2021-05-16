import sys
from src.core.random_swap import *
from hypothesis import given
from hypothesis.strategies import text, integers

@given(integers())
def test_decode_inverts_encode(x):
    assert "sean" in "dogs with sean are going to the store"