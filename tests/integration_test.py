import os
import json
import unittest

from unittest.mock import patch, MagicMock
from difflib import Differ

from main import generate_html


class TestMain(unittest.TestCase):
    """Test case for the main function."""

    def setUp(self):
        """Load expected and actual HTML outputs."""
        with open('./tests/expected.html', 'r') as expected_file:
            self.expected_html = expected_file.read().splitlines()

        # Load sample data from JSON file
        with open('./tests/sample_data.json', 'r') as json_file:
            self.sample_data = json.load(json_file)

        self.user_list = ["yankeexe", "Swechhya", "mesaugat"]
        data_count = 5
        start_date = os.environ.get("START_DATE", "2023-10-01T00:00:00")
        self.variables = {
            "timedelta": start_date,
            "dataCount": data_count,
        }

    @patch('leaderboard.fetch_data.execute_query')
    def test_main_function(self, mock_execute_query):
        """Test the main function to ensure HTML output matches expected output."""
        
        # Create a list of mock HTTP response objects for each sample data entry
        mock_responses = [MagicMock(json=entry.copy) for entry in self.sample_data]

        # Set the side effect of the mock to return each response sequentially
        mock_execute_query.side_effect = mock_responses

        # Run the generate_html_function
        html_string = generate_html(self.user_list, self.variables)  # This will use the mocked execute_query
        with open("tests/actual.html", "w") as f:
            f.write(html_string)

        with open('./tests/actual.html', 'r') as actual_file:
            self.actual_html = actual_file.read().splitlines()

        # Compare the actual and expected HTML outputs using difflib
        differ = Differ()
        diff = list(differ.compare(self.expected_html, self.actual_html))

        # Check if there are any differences
        self.assertTrue(all(line.startswith('  ') for line in diff), "HTML files do not match")


if __name__ == '__main__':
    unittest.main()
