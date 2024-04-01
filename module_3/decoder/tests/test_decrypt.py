import unittest

from module_3.decoder.decrypt import decrypt


class TestDecrypt(unittest.TestCase):

    def test_decrypt_can_pass_base_checks(self):
        base_checks = (
            ('абра-кадабра.', 'абра-кадабра'),
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
            ('абрау...-кадабра', 'абра-кадабра'),
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1..2.3', '23'),
            ('.', ''),
            ('1.......................', '')
        )

        for check in base_checks:
            with self.subTest(data=check):
                encrypted_data = check[0]
                response = check[1]
                self.assertEqual(decrypt(encrypted_data), response)
