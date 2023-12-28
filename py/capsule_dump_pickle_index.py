import sys
import os
import pprint
from prettytable import PrettyTable
from veloxutils import process_args,recover, removeunicode, get_entity_fields, iter_entity_fields, parse_custom_fields, clean, _get_set, get_query

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

if reduced==True:
    entities = recover("reduced_" + entity,True,pickledir=dircapsulepickleindex)
else:
    entities = recover(entity,True,pickledir=dircapsulepickleindex)


pprint.pprint(len(entities.keys()))

for _key in entities.keys():
    print _key,len(entities[_key])


pprint.pprint(entities[entities.keys()[0]])

#pprint.pprint(entities[int(myid)])


