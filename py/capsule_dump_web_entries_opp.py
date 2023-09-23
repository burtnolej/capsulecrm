import datetime
import sys
import requests
import json
import time
import pprint
import unicodedata

from veloxutils import persist, _get_data, _header, entry_date_fields, process_args, party_fields,opp_date_fields, removeunicode

t1 = datetime.datetime.now()
access_code="4rY0P12jmfi0iq41S0mtuDUi4yKEfnLefH260Ufkgnb8fE33xfdt/fb2dsqGeev7"

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

entries = _get_data("https://api.capsulecrm.com/api/v2/entries", \
                    access_code, \
                    entity, \
                    data_filter, \
                    start_page, \
                    int(multipage))

opportunities = _get_data("https://api.capsulecrm.com/api/v2/opportunities", \
                    access_code, \
                    "opportunities", \
                    data_filter, \
                    start_page, \
                    int(multipage))

_opportunities={"OPID":{},"CLIENTID":{}}
_opsid = _opportunities["OPID"]
_opsclient = _opportunities["CLIENTID"]

for _opp in opportunities:
    _id=_opp["id"]
    _party= _opp["party"]

    _opsid[_id]=_opp

    if _opsclient.has_key(_party["id"])==True:
        _opsclient[_party["id"]].append(_opp)
    else:
        _opsclient[_party["id"]] = [_opp]

if len(entries)==0:
    exit()


fh = open(outputfile,'w+')
#fh.write("^".join(cols+custom_fields)+"\n")

entries_by_partyid={}
_entries={}

for _entry in entries:
    _type = _entry["type"]
    _output = [_type]
    _partytype=""
    _party=""

    if _entry["id"]==387264302:
        pass

    if _type=="note":
        if _entry.has_key("party"):
	    if _entry["party"]!=None:
                _partytype=_entry["party"]["type"]
                _party=_entry["party"] 
        _subject=""
    elif _type=="email":
        if _entry.has_key("parties"):
	    if _entry["parties"]!=None:
                if len(_entry["parties"])>0:
                    _partytype=_entry["parties"][0]["type"]
                    _party=_entry["parties"][0] 
        _subject=_entry["subject"]
    elif _type=="task":
        if _entry.has_key("party"):
	    if _entry["party"]!=None:
                _partytype=_entry["party"]["type"]
                _party=_entry["party"] 
        _subject=""

    _opportunityid=""
    _opportunity_name=""
    if _entry.has_key("opportunity"):
        if _entry["opportunity"]!=None:
            #try:
            _opportunityid=_entry["opportunity"]["id"]
            _opportunity_name=_entry["opportunity"]["name"]
            #except:
            #pass

    _output.append(str(_opportunityid))
    _output.append(str(_opportunity_name))
    _output.append(_entry["creator"]["username"])
    _output.append(str(_entry["id"]))
    _output.append(_type)
    _output.append(_subject)
    _output.append(removeunicode(_subject))
    
    _content=""
    if _entry.has_key("content"):
        if _entry["content"]!=None:
            _content=_entry["content"].replace("\r","")
    _output.append(removeunicode("$$".join(_content.split("\n"))))

    if _party=="":
        if _opportunityid!="":
            if _opsid.has_key(_opportunityid):
                if _opsid[_opportunityid].has_key("party")==True:
                    _output.append(str(_opsid[_opportunityid]["party"]["id"]))
                    _party_id=str(_opsid[_opportunityid]["party"]["id"])
                    for _partyfield in party_fields:
                        if _opsid[_opportunityid]["party"].has_key(_partyfield):
                            _output.append(str(_opsid[_opportunityid]["party"][_partyfield]))
                        else:
                            _output.append("")
                else:
                    _party_id=None
                    _output = _output+[None,"","","",""]
            else:
                _output = _output+["","","","",""]
        else:
            _output = _output+["","","","",""]
    else:
        _party_id=str(_party["id"])
        _output.append(str(_party["id"]))

        for _partyfield in party_fields:
            _value=""
            if _party.has_key(_partyfield):
                if _party[_partyfield] != None:
	    	    _value = removeunicode(_party[_partyfield])
            _output.append(_value)

    for _date in entry_date_fields:
        _output.append(_entry[_date][:10])

    _entries[_entry["id"]]=_entry

    try: 
        fh.write("^".join(removeunicode(_s) for _s in _output)+"\n")
        if _party_id!="None":
            if entries_by_partyid.has_key(_party_id)!=True:
	        entries_by_partyid[_party_id]=[_entry]
            else:
	        entries_by_partyid[_party_id].append(_entry)

    except Exception as error:
        print "an error has occurred:"+ type(error).__name__ + "-"+str(error)
        print _output
        exit()
fh.close()


t2 = datetime.datetime.now()
delta = t2-t1
sys.stderr.write("rows exported: " + str(len(entries)) +" runtime: "+str(delta.total_seconds())+" secs\n")

if mode=="persist":
    persist(entries_by_partyid,"entries_by_partyid.pickle")
    persist(_entries,"entries.pickle")
    persist(_opsclient,"opportunities_by_partyid.pickle")
    persist(_opsid,"opportunities.pickle")
