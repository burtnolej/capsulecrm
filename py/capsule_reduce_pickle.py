import sys
import os
import pprint
from prettytable import PrettyTable
from veloxutils import process_args,recover, removeunicode, get_entity_fields, iter_entity_fields, parse_custom_fields, clean, _get_set, get_query, persist

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

new_size=1000

entities = recover(entity,True,pickledir=dircapsulepickle)
reduced_entities_keys=entities.keys()[:new_size]
reduced_entities={}

for _key in reduced_entities_keys:
    reduced_entities[_key] = entities[_key]

persist(reduced_entities,"reduced_" + entity + ".pickle")

