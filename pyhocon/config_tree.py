from pyparsing import TokenConverter, ParseResults
from pyhocon.exceptions import ConfigException


class ConfigTreeParser(TokenConverter):

    def __init__(self, expr=None):
        super(ConfigTreeParser, self).__init__(expr)
        self.saveAsList = True

    def postParse(self, instring, loc, token_list):
        config_tree = ConfigTree()
        for token in token_list:
            # key, value
            if len(token) == 2:
                key, value = token
                conv_value = list(value) if isinstance(value, ParseResults) else value
                config_tree.put(key, conv_value)

        return config_tree


class ConfigTree(object):
    KEY_SEP = '.'

    def __init__(self):
        self._dictionary = {}

    def _put(self, key_path, value):
        key_elt = key_path[0]
        if len(key_path) == 1:
            self._dictionary[key_elt] = value
        else:
            next_config_tree = self._dictionary.get(key_elt)
            if not isinstance(next_config_tree, ConfigTree):
                # create a new dictionary or overwrite a previous value
                next_config_tree = ConfigTree()
                self._dictionary[key_elt] = next_config_tree
            next_config_tree._put(key_path[1:], value)

    def _get(self, key_path):
        key_elt = key_path[0]
        elt = self._dictionary.get(key_elt)

        if len(key_path) == 1:
            return elt

        if isinstance(elt, ConfigTree):
            try:
                return elt._get(key_path[1:])
            except ConfigException as e:
                raise ConfigException(e.message, key_path=[key_elt] + e._key_path)
        else:
            # TODO: show prefix path
            raise ConfigException("Cannot access field {key}".format(key=key_elt), key_path=[key_elt])

    def put(self, key, value):
        self._put(key.split(ConfigTree.KEY_SEP), value)

    def get(self, key):
        try:
            return self._get(key.split(ConfigTree.KEY_SEP))
        except ConfigException as e:
            raise ConfigException('{message}. Path = {path}'.format(message=e.message, path=ConfigTree.KEY_SEP.join(e._key_path)), e._key_path)

    def get_string(self, key):
        return str(self.get(key))

    def get_int(self, key):
        return int(self.get(key))

    def get_float(self, key):
        return float(self.get(key))

    def get_bool(self, key):
        return bool(self.get(key))

    def get_list(self, key):
        value = self.get(key)
        if isinstance(value, list):
            return value
        else:
            raise ConfigException("{key} has type '{type}' rather than 'list'".format(key=key, type=type(value).__name__))

    def __getitem__(self, item):
        return self.get(item)

    def __contains__(self, item):
        return item in self._dictionary

    def __str__(self):
        return str(self._dictionary)

    def __repr__(self):
        return repr(self._dictionary)