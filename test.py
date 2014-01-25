import unittest

from lines.encoder import dumps

class TestEncoder(unittest.TestCase):
    def t(self, out, **obj):
        self.assertEqual(out, dumps(obj))

    def test_simple(self):
        self.t('foo=bar', foo='bar')

    def test_bool(self):
        # NOOOOOOOOOO!, the order or kwargs is not kept
        self.t('foo=#t bar=#f baz=nil', foo=True, bar=False, baz=None)

    def test_empty_string(self):
        self.t('foo=', foo='')

    def test_numbers(self):
        self.t('foo=10000.0', foo=10e3)
        self.t('foo=1', foo=1)
        self.t('foo=-1', foo=-1)

    def test_lists(self):
        self.t('foo=[1 2 a]', foo=[1,2,'a'])

    def test_max_depth(self):
        x = dict()
        x['x'] = x
        self.t('x={x={x={x={...}}}}', x=x)


if __name__ == '__main__':
    unittest.main()
