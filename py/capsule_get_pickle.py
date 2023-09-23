import sys
import os
import pprint
from prettytable import PrettyTable
from veloxutils import process_args,recover

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

entities = recover(entity)


pprint.pprint(entities)
