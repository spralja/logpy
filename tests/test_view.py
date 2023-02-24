import unittest



class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        from os import system

        from logpy.view.config import Config

        system('mkdir tests/temp')
        self.config = Config('tests/temp/.logpy.yaml')

    def tearDown(self):
        from os import system

        system('rm -r tests/temp')

    def test_constructor_no_file(self):
        from pathlib import Path

        self.assertTrue(Path('tests/temp/.logpy.yaml').exists())

    def test_get_no_values(self):
        value = self.config.get('somtn')
        expected = None

        self.assertEqual(value, expected)

    def test_get_value(self):
        from os import system

        system('echo "something: someone" > tests/temp/.logpy.yaml')

        value = self.config.get('something')
        excepted = 'someone'

        self.assertEqual(value, excepted)

    def test_set_value_old_none(self):
        old_value = self.config.set('something', 'someone')
        new_value = self.config.get('something')

        expected_old = None
        expected_new = 'someone'

        self.assertEqual(old_value, expected_old)
        self.assertEqual(new_value, expected_new)

    def test_set_value_old_exists(self):
        from os import system

        system('echo "something: someone2" > tests/temp/.logpy.yaml')

        old_value = self.config.set('something', 'someone')
        new_value = self.config.get('something')

        expected_old = 'someone2'
        expected_new = 'someone'

        self.assertEqual(old_value, expected_old)
        self.assertEqual(new_value, expected_new)
