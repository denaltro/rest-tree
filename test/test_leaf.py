import tree
import unittest

from tree.model import Leaf


class LeafTest(unittest.TestCase):
    def test_init_model(self):
        model = Leaf('1', 'name_test')
        assert model.id is '1'
        assert model.name is 'name_test'

    def test_parent_level_one(self):
        model = Leaf('1.2', 'name')
        assert model.parent_id is '1'

    def test_parent_level_two(self):
        model = Leaf('1.2.3', 'model name')
        assert model.parent_id == '1.2'

    def test_text_field(self):
        model = Leaf('1.2', 'fulltextsearch')
        assert model.text == '1.2 fulltextsearch'

    def test_model_type(self):
        with self.assertRaises(ValueError):
            Leaf(1.2, 111)

    def test_none_args(self):
        with self.assertRaises(ValueError):
            Leaf(None, None)


if __name__ == '__main__':
    unittest.main()
