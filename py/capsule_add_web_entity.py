import datetime
import sys
import requests
import json
import time
import pprint
import unicodedata

from veloxutils import _put_data,_header,process_args, persist, get_remaining_rate, _get_data_simple

_args = process_args(sys.argv)
#_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

t1 = datetime.datetime.now()

access_code="4rY0P12jmfi0iq41S0mtuDUi4yKEfnLefH260Ufkgnb8fE33xfdt/fb2dsqGeev7"
response = _get_data_simple("https://api.capsulecrm.com/api/v2/parties/fields/definitions",access_code)

response = httpfunc(url,headers=_header(access_token),data=json.dumps(data))
print response.json()['definitions']

#access_code="kBtqQU5lrQ5tVfn3Ngz04BhcSyWWGJ2Nycz+ODFdXOdPTur9FVmhw3wN3bs6TOhC"

data = {"party":{"Contact Owner":"Jon",\
        "firstName":"foo", \
        "jobTitle":"foobar", \
        "lastName":"barfoo", \
        "type":"person",\
        "organisation":188497262}}

entity="parties"
sub_entity="person"

print _put_data("https://api.capsulecrm.com/api/v2/"+entity, \
                access_code, \
                "party", \
                data)
