import pytest
from difflib import Differ

from main import main


def test_main_function():
    # Run the main function
    main()

    # Read the expected and actual HTML outputs
    with open('./tests/index.html', 'r') as expected_file, open('./build/index.html', 'r') as actual_file:
        expected_html = expected_file.read().splitlines()
        actual_html = actual_file.read().splitlines()

    # Compare the actual and expected HTML outputs using difflib
    differ = Differ()
    diff = list(differ.compare(expected_html, actual_html))

    # Check if there are any differences
    assert all(line.startswith('  ') for line in diff), "HTML files do not match"


# Run the test
if __name__ == "__main__":
    pytest.main()
