import pytest

from quiz_enchanter.gui import iterator_to_chain


@pytest.mark.parametrize(
    "iterator, normal_chain, last_connector, expected_result", [
        (["1", "2", "3"], ", ", " and ", "1, 2 and 3"),
        (["1", "2", "3"], ", ", " or ", "1, 2 or 3"),
        (["a", "b", "c"], ", ", " or ", "a, b or c")
    ]
)
def test_iterator_to_chain(iterator, normal_chain, last_connector, expected_result):
    assert iterator_to_chain(iterator, normal_chain, last_connector) == expected_result
