import datetime
import sys
import requests
import json
import time

from veloxutils import _get_data, _header

access_code="4rY0P12jmfi0iq41S0mtuDUi4yKEfnLefH260Ufkgnb8fE33xfdt/fb2dsqGeev7"
opps = _get_data("https://api.capsulecrm.com/api/v2/opportunities",access_code,"opportunities","nofilter")

for _opp in opps:
	oppid=str(_opp['id'])
	opp=[oppid]
	opp.append(_opp['name'])
	opp.append(_opp['milestone']['name'])
	opp.append(_opp['createdAt'])

	url = "https://api.capsulecrm.com/api/v2/opportunities/"+oppid+"/parties"
	parties = _get_data("https://api.capsulecrm.com/api/v2/opportunities/"+str(oppid)+"/parties",access_code,"parties","nofilter")

	emails=[]
	for _party in parties:
		if _party.has_key('emailAddresses'): 
			try:
				emails.append(_party['emailAddresses'][0]['address'])
			except:
				emails.append(_party['firstName'] + " " +_party['lastName'])
				#emails.append("error")

	print ",".join(opp) + "," + ",".join(emails)
	time.sleep(1)

exit()

