class TestShortPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, f"Phrase '{phrase}' longer than 15 characters. Phrase length {len(phrase)} characters."