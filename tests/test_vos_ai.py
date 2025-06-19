import unittest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import vos_ai

class TestOpenApplication(unittest.TestCase):
    def test_known_command(self):
        with mock.patch('vos_ai.os.system') as mock_system:
            result = vos_ai.open_application('open chrome')
            self.assertTrue(result)
            mock_system.assert_called_once()

    def test_search_google(self):
        with mock.patch('vos_ai.webbrowser.open') as mock_open:
            result = vos_ai.open_application('search google for unit testing')
            self.assertTrue(result)
            mock_open.assert_called_once()

    def test_unknown_command(self):
        with mock.patch('vos_ai.os.system') as mock_system:
            result = vos_ai.open_application('do something unknown')
            self.assertFalse(result)
            mock_system.assert_not_called()

if __name__ == '__main__':
    unittest.main()
