import json
import traceback


class JsonField(object):
    pass


class StaticJsonField(JsonField):
    def __init__(self, name, defaultVal=None):
        self.name = name
        self.defaultVal = defaultVal

    def __get__(self, obj: dict, objtype):
        if(self.name not in obj):
            self.__set__(obj, self.defaultVal)
            return self.defaultVal
        return obj[self.name]

    def __set__(self, obj, val):
        obj[self.name] = val
        if(not hasattr(obj, self.name)):
            setattr(obj, self.name, self.__class__(self.name, val))

    def load(self, obj, objtype):
        self.__get__(obj, objtype)


class DynamicJsonField(JsonField):
    def __init__(self, obj, name, defaultVal):
        self.name = name
        self.defaultVal = defaultVal
        self.obj = obj
        if(self.name not in obj):
            self.__set__(obj, self.defaultVal)

    def __get__(self, obj: dict, objtype):
        if(self.name not in obj):
            self.__set__(obj, self.defaultVal)
            return self.defaultVal
        return obj[self.name]

    def __set__(self, obj, val):
        obj[self.name] = val
        if(not hasattr(obj, self.name)):
            setattr(obj, self.name, self.__class__(obj, self.name, val))

    def load(self, obj, objtype):
        self.__get__(obj, objtype)

# def JsonField(name, defaultVal):
#     return property(
#         lambda self: self.__getitem__(name),
#         lambda self, val: self.__setitem__(name, val),
#         lambda self: self.__delitem__(name)
#     )


class JsonObject(dict):
    def __new__(cls, *args, **kwargs):
        instance = super(JsonObject, cls).__new__(cls, *args, **kwargs)
        for key in dir(instance):
            attr = getattr(instance, key)
            if(type(key) == JsonField):
                attr.load(instance, type(instance))
        return instance

    def __getattribute__(self, attr):
        try:
            obj = object.__getattribute__(self, attr)
            if hasattr(obj, '__get__'):
                return obj.__get__(self, type(self))
            return obj
        except AttributeError:
            contain = object.__getattribute__(self, "__contains__")
            if(contain(attr)):
                getItem = object.__getattribute__(self, "__getitem__")
                return getItem(attr)
            else:
                raise AttributeError(
                    "'" + attr+"'" + " Not Found In " + "'" + self.__class__.__name__+"'")
        except e:
            raise e

    def getJson(self):
        return json.dumps(self)

    def setJson(self, val):
        self.update(json.loads(val))

    @classmethod
    def fromJson(_class, val):
        return _class(json.loads(val))
