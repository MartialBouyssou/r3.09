import pathlib
import sys
import unittest


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.main_vigenere import generate_vigenere_key, vigenere_cipher


class TestGenerateVigenereKey(unittest.TestCase):

    def test_key_shorter_than_text(self):
        self.assertEqual(
            generate_vigenere_key("ABC", 10),
            "ABCABCABCA"
        )

    def test_key_same_length_as_text(self):
        self.assertEqual(
            generate_vigenere_key("ABC", 3),
            "ABC"
        )

    def test_key_longer_than_text(self):
        self.assertEqual(
            generate_vigenere_key("ABCDEFG", 4),
            "ABCD"
        )

    def test_empty_text(self):
        self.assertEqual(
            generate_vigenere_key("ABC", 0),
            ""
        )


class TestVigenereCipher(unittest.TestCase):

    def test_basic_encryption(self):
        self.assertEqual(
            vigenere_cipher("ABC", "ABC"),
            '"$&'
        )

    def test_encryption_with_space(self):
        self.assertEqual(
            vigenere_cipher("A A", "ABC"),
            '"b$'
        )

    def test_key_repetition(self):
        self.assertEqual(
            vigenere_cipher("ABCABC", "AB"),
            '"$$##%'
        )


if __name__ == "__main__":
    unittest.main()