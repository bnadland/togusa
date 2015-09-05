#!./env/bin/python

import json
import unittest

import togusa

ENGLISH_TEXT="""The Aneristic Principle is that of apparent order; the Eristic Principle is
that of apparent disorder. Both order and disorder are man made concepts and
are artificial divisions of pure chaos, which is a level deeper than is the
level of distinction making.
"""

GERMAN_TEXT="""
Bescheidne Wahrheit sprech ich dir. Wenn sich der Mensch, die kleine Narrenwelt, Gewöhnlich für ein Ganzes hält.
"""

class TogusaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = togusa.app.test_client()

    def get_json(self, response):
        return json.loads(response.data.decode('UTF-8'))

    def get_language(self, text):
        rv = self.app.post('/api/language',
            data=json.dumps({'text': text}),
            content_type='application/json',
            follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        json_data = json.loads(rv.data.decode('UTF-8'))
        self.assertEqual(json_data['text'], text)
        self.assertIsNotNone(json_data['probabilities'])

        return json_data['lang']

    def get_keywords(self, text):
        rv = self.app.post('/api/keywords',
            data=json.dumps({'text': text}),
            content_type='application/json',
            follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        json_data = json.loads(rv.data.decode('UTF-8'))
        self.assertEqual(json_data['text'], text)
        self.assertIsNotNone(json_data['lang'])

        return json_data['keywords']

    def test_helpscreen(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn('Togusa Textanalysis Api', rv.data.decode('UTF-8'))

    def test_language_english(self):
        lang = self.get_language(ENGLISH_TEXT)
        self.assertEqual(lang, 'en')

    def test_language_german(self):
        lang = self.get_language(GERMAN_TEXT)
        self.assertEqual(lang, 'de')

    def test_keywords_english(self):
        keywords = self.get_language(ENGLISH_TEXT)
        self.assertIsNotNone(keywords)

    def test_keywords_german(self):
        keywords = self.get_language(GERMAN_TEXT)
        self.assertIsNotNone(keywords)
        
if __name__ == '__main__':
    unittest.main()
