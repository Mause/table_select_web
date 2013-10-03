# stdlib
import re

# third-party
import tornado.web
from sqlalchemy.orm.collections import InstrumentedList

# application specific
from settings import settings

STRING_DASHERIZE_REGEXP = re.compile(r'[ _]')
STRING_DECAMELIZE_REGEXP = re.compile(r'([a-z])([A-Z])')
STRING_CAMELIZE_REGEXP = re.compile(r'(\-|_|\.|\s)+(.)?')
STRING_UNDERSCORE_REGEXP_1 = re.compile(r'([a-z\d])([A-Z]+)')
STRING_UNDERSCORE_REGEXP_2 = re.compile(r'\-|\s+')


def pluralize(name):
    plurals = settings.get('plurals')

    if plurals and name in plurals:
        return plurals[name]
    else:
        if not name.endswith('s'):
            return name + "s"
        else:
            return name


def singularize(name):
    """
    use the same plurals hash to determine
    special-case singularization
    """

    plurals = settings.get('plurals')
    if plurals:
        for i in plurals.keys():
            if plurals[i] == name:
                return i

    if name.endswith('s'):
        return name[:-1]
    else:
        return name


def camelize(string):
    """
    >>> camelize('words_just_words')
    'wordsJustWords'
    """
    return STRING_CAMELIZE_REGEXP.sub(
        lambda match: match.groups()[1].upper(),
        string
    )


def camelize_dict(dictionary):
    return {camelize(k): v for k, v in dictionary.items()}


def camelize_dicts(dicts):
    return list(map(camelize_dict, dicts))


# these functions assume that there is only one primary key
def get_primary_key_name_from_table(table):
    if hasattr(table, '__table__'):
        table = table.__table__
    assert len(table.primary_key.columns.keys()) < 2, (
        'More than one primary key on table.')
    return table.primary_key.columns.keys()[0]


def get_primary_key_from_record(record):
    key = get_primary_key_name_from_table(record)
    return record.__dict__[key]


def dict_from_query(query):
    def serialize(record, ids_only=False):
        if type(record) in (list, InstrumentedList):
            return [serialize(sub, ids_only=True) for sub in record]

        if ids_only:
            return get_primary_key_from_record(record)
        else:
            out = {}
            for key, value in record.items():
                if type(value) == InstrumentedList:
                    key = singularize(key) + '_ids'
                    value = serialize(value, ids_only=True)
                out[key] = value
            return out

    if type(query) == list:
        return list(map(serialize, query))
    else:
        return serialize(query)


class Application(tornado.web.Application):
    def __init__(self, handlers, *args, **kwargs):
        new_handlers = []

        for handler in handlers:
            if type(handler[1]) == list:
                handler = self.splat(handler[1], handler)
                new_handlers.extend(handler)
            else:
                new_handlers.append(handler)

        return super().__init__(new_handlers, *args, **kwargs)

    def splat(self, handlers, super_handler):
        prefix, _, kwargs = super_handler

        new_handlers = []
        for handler in handlers:
            new_handlers.append(self._splat_single(prefix, kwargs, handler))

        return new_handlers

    def _splat_single(self, prefix, super_kwargs, handler):
        if len(handler) == 3:
            pattern, handler, my_kwargs = handler
        else:
            pattern, handler = handler
            my_kwargs = {}

        kwargs = super_kwargs.copy()
        kwargs.update(my_kwargs)

        pattern = prefix + pattern
        if 'postfix' in kwargs:
            pattern += kwargs['postfix']
            del kwargs['postfix']

        return (pattern, handler, kwargs)


def main():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
