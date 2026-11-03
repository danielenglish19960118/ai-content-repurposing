"""
Unit Tests for InsightEngine Enterprise Core Module
"""
import unittest
from src.schemas import TEMPLATES, SUPPORTED_LANGUAGES, DEFAULT_MODEL

class TestEngine(unittest.TestCase):
    def test_templates_exist(self):
        self.assertIn("Standard Executive Briefing", TEMPLATES)
        self.assertIn("Technical & Infrastructure Review", TEMPLATES)
        self.assertIn("Product & Marketing Strategy", TEMPLATES)

    def test_supported_languages(self):
        self.assertIn("English", SUPPORTED_LANGUAGES)
        self.assertIn("Traditional Chinese (繁體中文)", SUPPORTED_LANGUAGES)

    def test_default_model(self):
        self.assertEqual(DEFAULT_MODEL, "gemini-3.6-flash")

if __name__ == "__main__":
    unittest.main()
