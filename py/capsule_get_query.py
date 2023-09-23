import sys
import os
import pprint
from prettytable import PrettyTable
from veloxutils import process_args,recover, get_query 

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

db = recover(entity)

query_results = get_query(db,query)

