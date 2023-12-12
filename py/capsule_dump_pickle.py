import sys
import os
import pprint
from prettytable import PrettyTable
from veloxutils import process_args,recover, removeunicode, get_entity_fields, iter_entity_fields, parse_custom_fields, clean, _get_set, get_query

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

entities = recover(entity,True,pickledir=dircapsulepickle)

pprint.pprint(entities[int(myid)])


