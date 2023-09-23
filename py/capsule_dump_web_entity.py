import datetime
import sys
import requests
import json
import time
import pprint
import unicodedata

from veloxutils import _get_data,_header,process_args, persist, get_remaining_rate

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

t1 = datetime.datetime.now()

access_code="4rY0P12jmfi0iq41S0mtuDUi4yKEfnLefH260Ufkgnb8fE33xfdt/fb2dsqGeev7"

#access_code="kBtqQU5lrQ5tVfn3Ngz04BhcSyWWGJ2Nycz+ODFdXOdPTur9FVmhw3wN3bs6TOhC"


while get_remaining_rate(access_code) < 10:
    sys.stderr.write("sleeping .. no capacity\n")
    sleep(60)

sys.stderr.write("capacity on capsule api : " + str(get_remaining_rate(access_code)))

entities = _get_data("https://api.capsulecrm.com/api/v2/"+entity, \
                    access_code, \
                    entity, \
                    data_filter, \
                    start_page, \
                    int(multipage))

entities_results={}

for _entity in entities:
    entities_results[_entity["id"]] = _entity
    print _entity


t2 = datetime.datetime.now()
delta = t2-t1
sys.stderr.write(entity+" rows exported: " + str(len(entities)) +" runtime: "+str(delta.total_seconds())+" secs\n")

persist(entities_results,persistfile,index=False,pickledir=dircapsulepickle)
