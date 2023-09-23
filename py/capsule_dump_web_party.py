import datetime
import sys
import requests
import json
import time
import pprint
import unicodedata

from veloxutils import _get_data,_header,process_args, persist

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

t1 = datetime.datetime.now()

access_code="4rY0P12jmfi0iq41S0mtuDUi4yKEfnLefH260Ufkgnb8fE33xfdt/fb2dsqGeev7"

entities = _get_data("https://api.capsulecrm.com/api/v2/parties", \
                    access_code, \
                    entity, \
                    data_filter, \
                    start_page, \
                    int(multipage))

entities_results={}


for _entity in entities:
    if _entity.has_key("type") == True:
        if _entity["type"] == sub_entity:
            entities_results[_entity["id"] = _entity

t2 = datetime.datetime.now()
delta = t2-t1
sys.stderr.write("rows exported: " + str(len(entities)) +" runtime: "+str(delta.total_seconds())+" secs\n")

persist(entities_results,persistfile)
