import sys
from veloxutils import process_args,recover

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]

opps = recover(dbopportunities)

for _opp in opps:
    print _opp,opps[_opp]
