from config_loader.loader import ConfigLoader
from config_loader.config import ConfigBaseDict
from config_loader.config import ConfigBase


class DummyFoo(ConfigBase):
    def __init__(self, *args, **kwargs):
        self._type = str
        super(DummyFoo, self).__init__(*args, **kwargs)


class DummyConfig(ConfigBaseDict):
    def __init__(self, *args, **kwargs):
        self._dict_fields = {
            'foo': {
                'class': DummyFoo,
            }
        }
        super(DummyConfig, self).__init__(*args, **kwargs)


class DummyConfigRequired(ConfigBaseDict):
    def __init__(self, *args, **kwargs):
        self._dict_fields = {
            'foo': {
                'class': DummyFoo,
                'required': True,
            }
        }
        super(DummyConfigRequired, self).__init__(*args, **kwargs)


class DummyConfigDefault(ConfigBaseDict):
    def __init__(self, *args, **kwargs):
        self._dict_fields = {
            'foo': {
                'class': DummyFoo,
                'default': 'test',
            }
        }
        super(DummyConfigDefault, self).__init__(*args, **kwargs)


def test_normal():
    value = {}
    config = DummyConfig(value=value)
    assert config.is_valid()
    assert 'foo' not in config._children
    assert not hasattr(config, 'foo')

    value = {'foo': 'bar'}
    config = DummyConfig(value=value)
    assert config.is_valid()
    assert 'foo' in config._children
    assert hasattr(config, 'foo')


def test_required():
    value = {}
    config = DummyConfigRequired(value=value)
    assert not config.is_valid()
    assert config._errors[0].title == 'Required field is missing'

    value = {'foo': 'bar'}
    config = DummyConfigRequired(value=value)
    assert config.is_valid()


def test_default():
    value = {}
    config = DummyConfigDefault(value=value)
    assert config.is_valid()
    assert config.foo._value == 'test'

    value = {'foo': 'bar'}
    config = DummyConfigDefault(value=value)
    assert config.is_valid()
    assert config.foo._value == 'bar'