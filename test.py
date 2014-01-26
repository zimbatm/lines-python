import unittest
import datetime

from lines.encoder import dumps

class TestEncoder(unittest.TestCase):
    def t(self, out, **obj):
        self.assertEqual(out, dumps(obj))

    def test_simple(self):
        self.t('foo=bar', foo='bar')
        self.t('foo=bar', foo=u'bar')

    def test_quoted(self):
        self.t("foo='bar baz'", foo='bar baz')
        self.t('foo="bar\'baz"', foo="bar'baz")

    def test_bool_nil(self):
        self.t('foo=nil', foo=None)
        self.t('foo=#t',  foo=True)
        self.t('foo=#f',  foo=False)

    def test_empty_string(self):
        self.t('foo=', foo='')

    def test_numbers(self):
        self.t('foo=10000.0', foo=10e3)
        self.t('foo=1', foo=1)
        self.t('foo=-1', foo=-1)

    def test_lists(self):
        self.t('foo=[1 2 a]', foo=[1,2,'a'])

    def test_dict(self):
        self.t('x={y=3}', x=dict(y=3))

    def test_time(self):
        time = datetime.datetime.utcfromtimestamp(1337)
        # FIXME: TZ is never appended to the output string
        self.t('foo=1970-01-01T00:22:17', foo=time)

    def test_max_depth(self):
        x = dict()
        x['x'] = x
        self.t('x={x={x={x={...}}}}', x=x)


if __name__ == '__main__':
    unittest.main()
