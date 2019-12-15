from jsontools import JsonObject, StaticJsonField, DynamicJsonField


class Test_JsonObject(JsonObject):
    name = StaticJsonField("name", "kamran")
    birthDay = StaticJsonField("birthDay", 1993)


print("\ncreate instance with default value    +++++++++++++++++++++++++++")
instance = Test_JsonObject()
print(instance.getJson())
print(instance.name)

print("\nadd json attribute's like variable's    +++++++++++++++++++++++++++")
instance.nation = DynamicJsonField(instance, "nation", "iraninan")
print(instance.getJson())

print("\nchange default value by a json    +++++++++++++++++++++++++++")
instance.setJson('{"name":"unknown", "nation":"iraninan"}')
print(instance.getJson())
print(instance.nation)

print("\nload json to a new instance    +++++++++++++++++++++++++++")
instance = Test_JsonObject.fromJson('{"name":"unknown", "nation":"iraninan"}')
print(instance.getJson())
print(instance.nation)

print("\ncreate instance by a dict    +++++++++++++++++++++++++++")
instance = Test_JsonObject({"name": "unknown", "nation": "iraninan"})
print(instance.getJson())
print(instance.nation)
