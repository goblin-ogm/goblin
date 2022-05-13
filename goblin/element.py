"""Module defining graph elements."""

import logging

import inflection # type: ignore
from gremlin_python.process.traversal import Cardinality # type: ignore
from enum import Enum

from goblin import abc, exception, mapper, properties
from abc import ABCMeta

logger = logging.getLogger(__name__)

class ImmutableMode(Enum):
    OFF = 0
    SIMPLE = 1

class LockingMode(Enum):
    OFF = 0
    OPTIMISTIC_LOCKING = 1

class ElementMeta(ABCMeta):
    """
    Metaclass for graph elements. Responsible for creating the
    :py:class:`Mapping<goblin.mapper.Mapping>` object and replacing user
    defined :py:class:`goblin.properties.Property` with
    :py:class:`goblin.properties.PropertyDescriptor`.
    """

    def __new__(cls, name, bases, namespace, **kwds):
        props = {}
        if name == 'VertexProperty':
            element_type = name.lower()
        elif bases:
            element_type = bases[0].__type__
            if element_type not in ['vertex', 'edge']:
                element_type = bases[0].__name__.lower()
            for base in bases:
                base_props = getattr(base, '__properties__', {})
                props.update(base_props)
        else:
            element_type = name.lower()
        namespace['__type__'] = element_type
        if not namespace.get('__label__', None):
            namespace['__label__'] = inflection.underscore(name)
        new_namespace = {}
        props.pop('id', None)
        for k, v in namespace.items():
            if isinstance(v, abc.BaseProperty):
                if element_type == 'edge' and hasattr(v, 'cardinality'):
                    raise exception.MappingError(
                        'Edge property cannot have set/list cardinality')
                props[k] = v
                if k != 'id':
                    if not v.db_name:
                        v.db_name = v.db_name_factory(k,
                                                      namespace['__label__'])
                v = v.__descriptor__(k, v)
            new_namespace[k] = v
        new_namespace['__mapping__'] = mapper.create_mapping(namespace, props)
        new_namespace['__properties__'] = props
        new_namespace['__immutable__'] = namespace.get('__immutable__', ImmutableMode.OFF)
        new_namespace['__locking__'] = namespace.get('__locking__', LockingMode.OFF)
        result = ABCMeta.__new__(cls, name, bases, new_namespace)
        return result


class Element(metaclass=ElementMeta):
    """Base class for classes that implement the Element property interface"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if not (hasattr(self, key) and isinstance(
                    getattr(self, key), properties.PropertyDescriptor)):
                raise AssertionError(
                    "No such property: {} for element {}".format(
                        key, self.__class__.__name__))
            setattr(self, key, value)

    id = properties.IdProperty(properties.Generic)
    dirty = properties.Property(properties.String)


class VertexPropertyDescriptor:
    """
    Descriptor that validates user property input and gets/sets properties
    as instance attributes.
    """

    def __init__(self, name, vertex_property):
        self._prop_name = name
        self._name = '_' + name
        self._vertex_property = vertex_property.__class__
        self._data_type = vertex_property.data_type
        self._default = vertex_property.default
        self._cardinality = vertex_property._cardinality

    def __get__(self, obj, objtype):
        if obj is None:
            return getattr(objtype.__mapping__, self._prop_name)
        default = self._default
        if default is not None:

            default = self._data_type.validate_vertex_prop(
                default, self._cardinality, self._vertex_property,
                self._data_type)
        return getattr(obj, self._name, default)

    def __set__(self, obj, val):
        if val is not None:
            val = self._data_type.validate_vertex_prop(
                val, self._cardinality, self._vertex_property, self._data_type)
        setattr(obj, self._name, val)


class VertexProperty(Element, abc.BaseProperty):
    """Base class for user defined vertex properties."""

    __descriptor__ = VertexPropertyDescriptor

    def __init__(self,
                 data_type,
                 *,
                 default=None,
                 db_name=None,
                 card=None,
                 db_name_factory=None):
        if not db_name_factory:
            def db_name_factory(x, y):
                pass
        if isinstance(data_type, type):
            data_type = data_type()
        self._db_name_factory = db_name_factory
        self._data_type = data_type
        self._default = default
        self._db_name = db_name
        self._val = None
        if card is None:
            card = Cardinality.single
        self._cardinality = card

    def to_dict(self):
        result = {
            '__label__': self.__label__,
            '__type__': self.__type__,
            '__value__': self._val
        }
        for key, value in self.__properties__.items():
            prop = getattr(self, key, None)
            result[key] = prop
        return result

    def from_dict(self, d):
        d.pop('__label__')
        d.pop('__type__')
        d.pop('__value__')
        for key, value in d.items():
            setattr(self, key, value)

    @property
    def default(self):
        return self._default

    @property
    def data_type(self):
        return self._data_type

    @property
    def db_name_factory(self):
        return self._db_name_factory

    def getvalue(self):
        return self._val

    def setvalue(self, val):
        self._val = val

    value = property(getvalue, setvalue)

    def getdb_name(self):
        return self._db_name

    def setgetdb_name(self, val):
        self._db_name = val

    db_name = property(getdb_name, setgetdb_name)

    @property
    def cardinality(self):
        return self._cardinality

    def __repr__(self):
        return '<{}(type={}, value={})'.format(self.__class__.__name__,
                                               self._data_type, self.value)


class Vertex(Element):
    """Base class for user defined Vertex classes"""

    def to_dict(self):
        result = {'__label__': self.__label__, '__type__': self.__type__}
        for key, value in self.__properties__.items():
            vert_prop = getattr(self, key, None)
            if isinstance(vert_prop, (list, set)):
                vert_prop = [vp.to_dict() for vp in vert_prop]
            elif isinstance(vert_prop, VertexProperty):
                vert_prop = vert_prop.to_dict()
            result[key] = vert_prop
        return result

    @classmethod
    def from_dict(cls, d):
        elem = cls()
        d.pop('__label__')
        d.pop('__type__')
        for key, value in d.items():
            if isinstance(value, list):
                first_prop = value[0]
                setattr(elem, key, first_prop['__value__'])
                if isinstance(getattr(elem, key), list):
                    getattr(elem, key)[0].from_dict(first_prop)
                    for prop in value[1:]:
                        getattr(elem, key).append(prop['__value__'])
                        getattr(elem, key)[-1].from_dict(prop)

                elif isinstance(getattr(elem, key), set):
                    getattr(elem,
                            key)(first_prop['__value__']).from_dict(first_prop)
                    for prop in value[1:]:
                        val = prop['__value__']
                        getattr(elem, key).add(val)
                        getattr(elem, key)(val).from_dict(prop)
                else:
                    raise Exception("not a list or set property")
            elif isinstance(value, dict):
                setattr(elem, key, value['__value__'])
                getattr(elem, key).from_dict(value)
            else:
                setattr(elem, key, value)
        return elem


class GenericVertex(Vertex):
    """
    Class used to build vertices when user defined vertex class is not
    available. Generally not instantiated by end user.
    """
    pass


class Edge(Element):
    """
    Base class for user defined Edge classes.

    :param Vertex source: Source (outV) vertex
    :param Vertex target: Target (inV) vertex
    """

    def __init__(self, source=None, target=None):
        self.source = source
        self.target = target

    def to_dict(self, source=None, target=None):
        if not source:
            source = self.source.to_dict()
        if not target:
            target = self.target.to_dict()
        result = {
            '__label__': self.__label__,
            '__type__': self.__type__,
            'source': source,
            'target': target
        }
        for key, value in self.__properties__.items():
            prop = getattr(self, key, None)
            result[key] = prop
        return result

    @classmethod
    def from_dict(cls, d):
        elem = cls()
        d.pop('__label__')
        d.pop('__type__')
        for key, value in d.items():
            setattr(elem, key, value)
        return elem

    def getsource(self):
        return self._source

    def setsource(self, vertex):
        assert isinstance(vertex, Vertex) or vertex is None
        self._source = vertex

    def delsource(self):
        del self._source

    source = property(getsource, setsource, delsource)

    def gettarget(self):
        return self._target

    def settarget(self, vertex):
        assert isinstance(vertex, Vertex) or vertex is None
        self._target = vertex

    def deltarget(self):
        del self._target

    target = property(gettarget, settarget, deltarget)


class GenericEdge(Edge):
    """
    Class used to build edges when user defined edges class is not available.
    Generally not instantiated by end user.
    """
    pass
