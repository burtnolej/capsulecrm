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

for key in response.json()['definitions']:
    print key['name']+"^"+str(key['id'])

response = _get_data_simple("https://api.capsulecrm.com/api/v2/opportunities/fields/definitions",access_code)

for key in response.json()['definitions']:
    _id = str(key['id'])
    _key =  key['name']

    print "^".join([_key,_id])

response = _get_data_simple("https://api.capsulecrm.com/api/v2/pipelines/101389/milestones",access_code)

for key in response.json()['milestones']:
    _id = str(key['id'])
    _key =  key['name']

    print "^".join([_key,_id])


response = _get_data_simple("https://api.capsulecrm.com/api/v2/users",access_code)

for key in response.json()['users']:
    _id = str(key['id'])
    _key =  key['name']

    try:
        print _key,_id
        print "^".join([_key,_id])
    except:
        pass
