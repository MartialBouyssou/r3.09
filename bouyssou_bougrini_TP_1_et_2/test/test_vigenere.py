import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.main_vigenere import generate_vigenere_key, vigenere_cipher, vigenere_decipher


class TestGenerateVigenereKey(unittest.TestCase):

    def test_key_shorter_than_text(self):
        self.assertEqual(generate_vigenere_key("ABC", 10), "ABCABCABCA")

    def test_key_same_length_as_text(self):
        self.assertEqual(generate_vigenere_key("ABC", 3), "ABC")

    def test_key_longer_than_text(self):
        self.assertEqual(generate_vigenere_key("ABCDEFG", 4), "ABCD")

    def test_empty_text(self):
        self.assertEqual(generate_vigenere_key("ABC", 0), "")

    def test_empty_key(self):
        with self.assertRaises(ValueError):
            generate_vigenere_key("", 5)


class TestVigenereCipher(unittest.TestCase):

    def test_basic_encryption(self):
        self.assertEqual(vigenere_cipher("ABC", "ABC"), "bdf")

    def test_encryption_with_space(self):
        self.assertEqual(vigenere_cipher("A A", "ABC"), "bBd")

    def test_key_repetition(self):
        self.assertEqual(vigenere_cipher("ABCABC", "AB"), "bddcce")

    def test_upper_and_lower_case(self):
        self.assertEqual(vigenere_decipher(vigenere_cipher("AbC aBc", "Key"), "Key"), "AbC aBc")

    def test_numbers_and_special_characters(self):
        text = "123 !@#$%^&*()"
        key = "Key"
        self.assertEqual(vigenere_decipher(vigenere_cipher(text, key), key), text)

    def test_key_longer_than_text(self):
        text = "ABC"
        key = "ABCDEFG"
        self.assertEqual(vigenere_decipher(vigenere_cipher(text, key), key), text)

    def test_key_same_length_as_text(self):
        text = "Hello"
        key = "World"
        self.assertEqual(vigenere_decipher(vigenere_cipher(text, key), key), text)

    def test_encrypt_then_decrypt(self):
        texts = [
            "Hello World!",
            "ABC abc",
            "1234 !@#$",
            "Un texte un peu plus long pour tester le fonctionnement.",
        ]
        keys = ["KEY", "ABC", "Secret", "Bonjour"]

        for text, key in zip(texts, keys):
            cipher = vigenere_cipher(text, key)
            decoded = vigenere_decipher(cipher, key)
            self.assertEqual(decoded, text)

    def test_non_printable_text_is_rejected(self):
        with self.assertRaises(ValueError):
            vigenere_cipher("ABC\n", "ABC")

    def test_non_printable_key_is_rejected(self):
        with self.assertRaises(ValueError):
            vigenere_cipher("ABC", "AB\t")

    def test_non_printable_cipher_text_is_rejected(self):
        with self.assertRaises(ValueError):
            vigenere_decipher("ABC\n", "ABC")

    def test_non_printable_decode_key_is_rejected(self):
        with self.assertRaises(ValueError):
            vigenere_decipher("ABC", "AB\t")

    def test_empty_text_is_rejected(self):
        with self.assertRaises(ValueError):
            vigenere_cipher("", "ABC")

    def test_empty_key_is_rejected(self):
        with self.assertRaises(ValueError):
            vigenere_cipher("ABC", "")


if __name__ == "__main__":
    unittest.main()
