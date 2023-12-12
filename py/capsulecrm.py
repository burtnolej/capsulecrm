import requests
import os
import json
import unicodedata
import sys
from veloxutils import now, remove_non_ascii
#from util.misc import now, remove_non_ascii
from time import sleep

def _header(access_token):
    _headers = {
        'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(access_token),
            'Accept': 'application/json'
    }

    return _headers

def _parse_fields(fields):
    o={}
    for _fields in fields:
        o[_fields["definition"]["name"]]= _fields["value"]
    return o

def _geturl(entity_type,action_type="write"):

    _entity_type=""
    _entity_sub_type=""
    
    url='https://api.capsulecrm.com/api/v2'
    #url='https://184.73.209.229/api/v2'
 
    if entity_type in ["organisation","person"]:
        _entity_type='parties'
        _entity_sub_type='party'
        url=url+"/"+_entity_type

        if action_type=="read":
            url=url+"/filters/results"
    elif entity_type in ["note","email"]:
        _entity_type='entries'
        _entity_sub_type="entry"
        url=url+"/"+_entity_type 
    elif entity_type in ["entries"]:
        _entity_type='entries'
        _entity_sub_type="entry"
        url=url+"/"+_entity_type 
    elif entity_type == "opportunity":
        _entity_type='opportunities'
        _entity_sub_type='opportunity'
        url=url+"/"+_entity_type   
        if action_type=="read":
            url=url+"/filters/results"
    elif entity_type == "opportunity_tags":
        _entity_type='tags'
        _entity_sub_type='tag'
        url=url+"/opportunities/"+_entity_type  
    elif entity_type == "kases":
        _entity_type='kases'
        _entity_sub_type='kase'
        url=url+"/"+_entity_type  
    elif entity_type=='tasks':
        _entity_type='tasks'
        _entity_sub_type='task'
        url=url+"/"+_entity_type 
    elif entity_type=='milestones':
        _entity_type='milestones'
        url=url+"/"+_entity_type 
    elif entity_type=='pipelines':
        _entity_type='pipelines'
        url=url+"/"+_entity_type 
    elif entity_type=='lostreasons':
        _entity_type='lostReasons'
        url=url+"/"+entity_type 
    elif entity_type in ['activitytypes']:
        #_entity_type='activityTypes'
        #_entity_sub_type='activityTypes'
        _entity_type=entity_type
        _entity_sub_type=entity_type
        url=url+"/"+entity_type 
    elif entity_type in ['categories']:
        #_entity_type='activityTypes'
        #_entity_sub_type='activityTypes'
        _entity_type=entity_type
        _entity_sub_type="category"
        url=url+"/"+entity_type 
    elif entity_type=='users':
        _entity_type='users'
        _entity_sub_type="user"
        url=url+"/"+entity_type 

    elif entity_type=="opportunities_custom_fields_list":
        _entity_type="definitions"
        _entity_sub_type="definition"
        #list
        url = url + "/opportunities/fields/definitions"
    elif entity_type=="organisation_custom_fields_list":
        _entity_type="definitions"
        _entity_sub_type="definition"
        #list
        url = url + "/parties/fields/definitions"
    elif entity_type=="opportunities_custom_fields_text":
        _entity_type="definitions"
        _entity_sub_type="definition"
        url = url + "/opportunities/fields/definitions"
    elif entity_type=="organisation_custom_fields_text":
        _entity_type="definitions"
        _entity_sub_type="definition"
        #list
        url = url + "/parties/fields/definitions"
    elif entity_type=="person_custom_fields_list":
        _entity_type="definitions"
        _entity_sub_type="definition"
        #list
        url = url + "/parties/fields/definitions"
        
    return url,_entity_type,_entity_sub_type
    
def _compare(access_token,_id,entity_type,new_record):
    skip=True
    old_record = dump(access_token,entity_type,_id,pretty=False)
   
    if old_record.has_key("message"):
	print old_record["message"]
	return skip	
 
    users_nvp = dump_nvp(access_token,"users")
    
    # a hack for person/organization which are actually sub types of party
    if entity_type in ["person","organisation"]:
        entity_type="party"
    
    # api returns tasks as a task
    if entity_type == "tasks":
        entity_type="task"
        
    for key,value in new_record[entity_type].iteritems():
        if key=="fields":
            old_fields= _parse_fields(old_record[entity_type]["fields"])
            new_fields= _parse_fields(new_record[entity_type]["fields"])
            #for key,value in old_fields[entity_type].iteritems():
            #    old_value = old_fields[entity_type][key]
            for key,value in new_fields.iteritems():
                
                new_value = new_fields[key]
                new_value = remove_non_ascii(new_value)
        
                if isinstance(new_value,dict):
                    if new_value.has_key("name"):
                        new_value = new_value["name"]
                if isinstance(value,dict):
                    if value.has_key("name"):
                        value = value["name"]
                    
                if old_fields.has_key(key):
                    old_value = old_fields[key]
                else:
                    old_value = ""
                    
                if new_value.lower() != old_value.lower():
                    skip=False

                    try:
                        old_value=str(old_value).encode('ascii', 'ignore').decode('ascii')
                    except:
                        old_value="cannot decode"
                    try:    
                        value=str(value).encode('ascii', 'ignore').decode('ascii')
                    except:
                        value="cannot decode"
                        
                    print "updating [" + str(_id) + "] : " + key + " **to** " + str(new_value) + " **from** " + str(old_value)
                else:
                    #print "skip     [" + str(_id) + "] : " + key + "[" + str(new_value) + "," + str(old_value) + "]"
                    pass
        else:
            if old_record[entity_type].has_key(key):
                old_value = old_record[entity_type][key]
            else:
                old_value = " field not set"
                
            '''if isinstance(old_value,dict):
                if old_value.has_key("name"):
                    old_value = old_value["name"]
                    
            if isinstance(value,dict):    
                if value.has_key("name"):
                    value = value["name"]'''
                    
            if isinstance(old_value,dict):
                if old_value.has_key("id"):
                    old_value = old_value["id"]
                    
            if isinstance(value,dict):    
                if value.has_key("id"):
                    value = value["id"]
                
            if old_value != value:
                skip=False
                
                try:
                    old_value=str(old_value).encode('ascii', 'ignore').decode('ascii')
                except:
                    old_value="cannot decode"
                try:    
                    value=str(value).encode('ascii', 'ignore').decode('ascii')
                except:
                    value="cannot decode"
                    
                print "updating [" + str(_id) + "] : " + key + " **from** " + str(old_value) + " **to** " + str(value)
            else:   
                #print "skip [" + str(_id) + "] : " + key
                pass
                
    return skip
     
def dump_ids_no_sub_type(access_token,entity_type):

    j = dump(access_token,entity_type,verbose=False,pretty=False)
    ids=[]
    url,_entity_type,_entity_sub_type =_geturl(entity_type) 
    
    for entity in j[_entity_type]:
        ids.append(entity["id"])
        
    return ids

def dump_ids(access_token,entity_type):

    j = dump(access_token,entity_type,verbose=False,pretty=False)
    ids=[]
    url,_entity_type,_entity_sub_type =_geturl(entity_type) 
    
    for entity in j[_entity_type]:
        if entity.has_key("type")==True:
            if entity["type"] != entity_type:
                continue
        ids.append(entity["id"])
        
    return ids

def dump_nvp(access_token,entity_type,lookupkey=None,lookupvalue="id"):

    if entity_type=="milestones":
        j = {}
        i = dump(access_token,"pipelines",party_id="108857",verbose=False,pretty=False)
        l = dump(access_token,"pipelines",party_id="271011",verbose=False,pretty=False)
        k = dump(access_token,"pipelines",party_id="101389",verbose=False,pretty=False)
        j["milestones"] = k["milestones"] + l["milestones"] + i["milestones"]
        #return nvp
    else:
        #https://api.capsulecrm.com/api/v2/pipelines/271011/milestones
        #https://api.capsulecrm.com/api/v2/pipelines/101389/milestones
        j = dump(access_token,entity_type,verbose=False,pretty=False)

    nvp={}
    url,_entity_type,_entity_sub_type =_geturl(entity_type) 
    
    for entity in j[_entity_type]:
        if entity.has_key("type")==True:
            if entity["type"] != entity_type:
                continue
        if lookupkey==None:
            nvp[entity["name"]] = entity["id"]
        elif isinstance(lookupkey,list):
            _a=[]
            for key in lookupkey:
                if entity[key]==None:
                    _a.append("NOTSET")
                else:
                    _a.append(entity[key])
            
            try:
                nvp["$".join(_a)] = entity["id"]
            except:
                print _a
                exit()

        else:
            nvp[entity[lookupkey]] = entity[lookupvalue]
            #nvp[entity[lookupkey]] = entity["id"]
        
    return nvp

def dump_nvp_no_sub_type(access_token,entity_type):

    j = dump(access_token,entity_type,verbose=False,pretty=False)
    nvp={}
    url,_entity_type,_entity_sub_type =_geturl(entity_type) 
    
    for entity in j[_entity_type]:
        if entity_type=="person":
            if entity['type'] == "person":
                nvp[entity["firstName"]+"$"+entity["lastName"]] = entity["id"]
        else:
            nvp[entity["name"]] = entity["id"]
        
        
    return nvp

def _restpostquery(url,access_token,data):
    print "_restpostquery:" + url
    response = requests.post(url, headers=_header(access_token), data=json.dumps(data))
    
    tag = response.json().keys()[0]
    items={tag:response.json()[tag]}
    morepages = response.links.has_key('next')
    
    while morepages==True: 
        url =  response.links['next']['url']
        print "page: _restpostquery:" + url
        response = requests.post(url, headers=_header(access_token), data=json.dumps(data))
        items[tag] = items[tag] + response.json()[tag]
        morepages = response.links.has_key('next')
    
    return items

def _restquery(url,access_token):
    print "_restquery:" + url
    response = requests.get(url,headers=_header(access_token))
    
    #print response.json()
    
    tag = response.json().keys()[0]
    items={tag:response.json()[tag]}
    morepages = response.links.has_key('next')
    
    while morepages==True: 
        url =  response.links['next']['url']
        print "page: _restquery:" + url
        response = requests.get(url,headers=_header(access_token))
        items[tag] = items[tag] + response.json()[tag]
        morepages = response.links.has_key('next')
        #print len(items['parties'])
    
    return items

def dump(access_token,entity_type,party_id=None,verbose=False,pretty=True):
    url,_,_ =_geturl(entity_type)
   
    if entity_type=="pipelines":
        url = url +"/"+str(party_id)+"/milestones"+'?embed=fields'
    elif party_id!=None:
        url = url +"/"+str(party_id)+'?embed=fields'
    else:
        url = url +"/"+'?embed=fields'
   
    items = {} 
    try:
       items = _restquery(url,access_token)
    except:
       print "retrying" + url + " sleeeping for 10 secs....."
       sleep(10)
       items = _restquery(url,access_token)
    
    if pretty==True:
        if verbose==True:
            #print json.dumps(response.json(),sort_keys=True, indent=4)
            print json.dumps(items,sort_keys=True, indent=4)
        else:
            #return json.dumps(response.json(),sort_keys=True, indent=4)
            return json.dumps(items,sort_keys=True, indent=4)
    else:
        #return response.json()
        return items
  
def get_parties(access_token,oppid):

    sleep(0.75)

    url="https://api.capsulecrm.com/api/v2/opportunities/"

    _parties=[]
    _ids=[]
    _url = url + str(oppid) + "/parties/" 

    response = requests.get(_url, headers=_header(access_token))
    print "getparties:" + url

    if response.status_code in [201,200,204]:
	_parties = response.json()["parties"]
	for i in range(0,len(_parties)):
            _ids.append(str(_parties[i]["id"]))   	
    else:
    	print "error:" + response.text + _url

    partystr = "$".join(_ids)

    if partystr == "":
        return "NOTSET"

    return "$".join(_ids)


def delete_party(access_token,entity_type,id_list):
    url="https://api.capsulecrm.com/api/v2/opportunities/"

    for _id in id_list:
	oppid=_id[0][1]
	partyid=_id[1][1]

	_url = url + oppid + "/parties/" + partyid

        print "delete_party:" + _url
        response = requests.delete(_url,headers=_header(access_token))

        #response = requests.post(_url, headers=_header(access_token))

        if response.status_code in [201,200,204]:
   	    print "success:" + str(response.status_code) + _url
        else:
    	    print "error:" + response.text + _url



def add_party(access_token,entity_type,id_list):
    url="https://api.capsulecrm.com/api/v2/opportunities/"

    for _id in id_list:
	oppid=_id[0][1]
	partyid=_id[1][1]

	_url = url + oppid + "/parties/" + partyid
        print "add_party:" + _url

        response = requests.post(_url, headers=_header(access_token))

        if response.status_code in [201,200,204]:
   	    print "success:" + str(response.status_code) + _url
        else:
    	    print "error:" + response.text + _url


def delete_list(access_token,entity_type,id_list):
    #j = dump(access_token,entity_type,verbose=False,pretty=False)

    for _id in id_list:
        print _id[0][1]
        delete(access_token,entity_type,_id[0][1])
        
def delete_all(access_token,entity_type):
    j = dump(access_token,entity_type,verbose=False,pretty=False)
    
    url,_entity_type,_entity_sub_type =_geturl(entity_type) 
    
    for entity in j[_entity_type]:
        if entity.has_key("type")==True:
            if entity["type"] != entity_type:
                continue
        delete(access_token,entity_type,entity["id"])

def delete_all_no_subtype(access_token,entity_type):
    j = dump(access_token,entity_type,verbose=False,pretty=False)
    
    url,_entity_type,_entity_sub_type =_geturl(entity_type) 
    
    for entity in j[_entity_type]:
        delete(access_token,entity_type,entity["id"])
        
    
def delete(access_token,entity_type,party_id):
    url,_,_ =_geturl(entity_type)
    url = url +"/"+str(party_id)

    response = requests.delete(url,headers=_header(access_token))

    if response.status_code in [201,200]:
   	status="success"
    else:
    	print response.text

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
 
def importcsv(fn,numlines=-1):
    result=[]

    fh = open(fn, 'r+')
    for line in fh:
        line=line.replace("@@","\n")
        result.append(line.strip())
    fh.close()

    header=result[0].split("^")

    if numlines==-1:
        numlines=len(result)

    output=[]
    for i in range(1,numlines):
	#row=result[i].encode('ascii','ignore')
        #row=row.split("^")
        row=result[i].split("^")
        _output=[]
        for j in range(0,len(row)):
            if header[j]=="description":
                #_output.append((header[j], "\"" + row[j] + "\""))
                _output.append((header[j], row[j] ))
            else:
                _output.append((header[j],row[j]))
        output.append(_output)

    return output

def read_api(access_token,objid,entity_type,action_type,ofile,col_count=-1,filter=-1):
    if entity_type=="note":
        person_nvp = dump_nvp(access_token,"person",lookupkey=["firstName","lastName"])
   
    def _unpack(op,format):
    
        h=[]
        o=[]
   
	#if op['organisation'] == "Backbase":
	#	pass
 
        _keys = op.keys()
        if entity_type == "person":  #for some reason persons cant rely on fields coming in consistent order
	    _keys.sort()
        
        #_keys = ["firstName","lastName","fields"]
    	dates=["createdAt","updatedAt","lastContactedAt","lastStageChangedAt"]
        
        #for key,value in op.iteritems():
	for key in _keys:
	    value = op[key]
            
            value = remove_non_ascii(value)
            #value = remove_non_ascii(str(value))
           
            if key in ["addresses","websites","pictureURL"]:
                pass
            elif key=="fields":
                for _fields in op["fields"]:
                    h.append(_fields["definition"]["name"])
                    #o.append("$".join([str(_fields["definition"]["id"]),_fields["value"]]))
                    if _fields["value"]==None:
                        o.append("None")
                    else:
                        o.append(_fields["value"])
	    elif key in dates:
                h.append(key)
                if op[key]==None:
                    o.append("2020-01-01")
		else:
               	    o.append(op[key][:10])
	    elif key in ["parties"]:
		_o=[]
                for i in range(0,len(op[key])):
		     _o.append(str(op[key][i]["id"]))
                o.append("$".join(_o))
                h.append(key)
	
            elif key in ["organisation","milestone","lastOpenMilestone","lostReason"]:
                if op[key]==None:
                    o.append("None")
                else:
                    _o=[]
                    if op[key].has_key("type"):
                        _o.append(op[key]["type"])
                    #_o=_o+[str(op[key]["id"]),op[key]["name"]]
                    #_o=_o+[str(op[key]["id"]),op[key]["name"]]
                    #o.append("$".join(_o))
                    o.append(op[key]["name"])
                    
                h.append(key)
            elif key in ["options"]:
                o.append("$".join(value))
                h.append(key)
            elif key == "content":
                h.append(key)
                if _notnull(value) == True:
                    value = value.replace("\n","__")
                    value = value.replace("\r","__")
                    value = value.replace("\t","")
                    value = value.replace("^","")
                    
                    o.append("\""+value+"\"")
                else:
                    o.append("None") 
                    
            elif key in ["attachments"]:
                _o=[]
                for attachment in value:
                    _o.append(attachment["filename"])
                o.append("$".join(_o))
                h.append(key)
            elif key in ["creator"]:
                o.append(value["username"])
                h.append(key)
            elif key in ["activityType","kase","category"]:
                h.append(key)
                if value != None and value != "None" and value != "":
                    o.append(value["name"])
                else:
                    o.append("None")
                    
            elif key in ["opportunity"]:
                if value != None and value != 'None' and  value != '':
                    o.append(value["name"])
                else:
                    o.append("None")
                h.append(key)
            elif key in ["participants"]:
                '''[{u'role': u'FROM', u'id': 263010897, u'name': None, u'address': u'jon.butler@veloxfintech.com'}, {u'role': u'TO', u'id': 263010898, u'name': u"'John Smith'", u'address': u'John.Smith@ihsmarkit.com'}, {u'role': u'CC', u'id': 263010899, u'name': u"'Alison Hood'", u'address': u'alison.hood@veloxfintech.com'}] '''
                emails = ""
                for participant in value:
                    if participant['address'].find("veloxfintech") == -1:
                        emails = emails + participant['address'] + ";"
                o.append(emails)
                h.append(key)
                  
            elif key in ["owner"]:
                try:
                    o.append(op[key]["name"])
                except:
                    o.append("null")
                h.append(key)
            elif key in ["payments"]:
                try:
                    o.append(op[key]["payments"])
                except:
                    o.append("null")
                h.append(key)
            elif key in ["party"]:

                try:
                    if entity_type=="note":
			if op.has_key(key) == True and op[key] != None:
                            fullName = op[key]["firstName"]+"$"+op[key]["lastName"]
                            o.append(str(person_nvp[fullName]))
                        else:
                            o.append("null")

                    elif op["party"]["type"] == "person":
                        if op[key]["firstName"]!=None:
                            firstName = op[key]["firstName"]
                        else:
                            firstName = ""
                            
                        if op[key]["lastName"]!=None:
                            lastName = op[key]["lastName"]
                        else:
                            lastName = ""
                            
                            
                        value = firstName + " " + lastName
                        o.append(value)
	            else:
                        value = op[key]["name"]
                        o.append(value) 
                except:
                    o.append("null")
                h.append(key)

                if entity_type=="opportunity":
                    o.append(get_parties(access_token,op["id"]))
                    h.append("parties")

     
            elif key=="phoneNumbers":
                if op[key]==None:
                    _o.append("None")
                else:
                    _o=[]
                    if isinstance(op[key],list):
                        for item in op[key]:
                            try:
			        _o.append(str(item["number"]))
                            except:
                                _o.append("error")
		    		
                        o.append("$".join(_o))
                    
                h.append(key)
                '''elif key=="tags":
                    if op[key]==None:
                        _o.append("None")
                    else:
                        _o=[]
                        if isinstance(op[key],list):
                            for item in op[key]:
                                print item
                                #_o.append(str(item["number"]))
                            #o.append("$".join(_o))
                        
                    #h.append(key)'''

            elif key in ["about","description","content","detail"]:
                #if value != "check contact created by the drop box":
                #    print 
                if value!=None:
                    _descr = value.replace("\n",";;")
                    _descr = _descr.replace("\r","")
                    _descr = _descr.replace("\t","")
                    _descr = _descr.replace(","," ")
                    o.append(_descr)
                    h.append(key)
                else:
                    o.append("\"\"")
                    h.append(key)
                    
                #o.append("\""+str(op[key])+"\"")
                
            elif key=="value":
                o.append(op[key]["currency"])
                h.append("currency")
                o.append(str(op[key]["amount"]))
                h.append("amount")
            elif key=="emailAddresses":
                if op[key]==None:
                    _o.append("None")
                elif op[key]=="[]":
                    o.append("[]")
                else:
                    _o=[]
                    for item in op[key]:
                        _o.append(str(item["address"]))
                    o.append("$".join(_o))
                h.append(key)
            else:
                o.append(str(value))
                h.append(key)
        return(h,o)
    
    url,_entity_type,_entity_sub_type =_geturl(entity_type,"read") 

    if _entity_type == "definitions":
        entity_type = "list"
    
    #j = _restquery(url,access_token)
    #json.dumps(j,sort_keys=True, indent=4)

    #url = "https://api.capsulecrm.com/api/v2/parties/filters/results"
    url=url+ "?embed=fields&perPage=100"
    if filter=="nofilter":
        data = {"filter": { "conditions": [] } }
        #data = {"filter": { "conditions": [ {"field" : "custom:749060", "operator":"is","value":"Q223 Cosmos"} ] } }
        #data = {"filter": { "conditions": [ {"field" : "custom:749060", "operator":"is","value":"Q223 Cosmos"} , {"field" : "name","operator":"is","value":"CITY_GARIMAGURU"} ] } }
    else:
        data = {"filter": { "conditions": [ { "field": "addedOn", "operator": "is", "value": filter } ] } }
        #data = {"filter": { "conditions": [ { "field": "addedOn", "operator": "is", "value": filter }, {"field" : "custom:{676299}", "operator":"is","value":"Q223 Cosmos"} ] } }

    print url
    if entity=="entry":
	j = _restquery(url,access_token)
    else:
        j = _restpostquery(url,access_token,data)

    #print j
    h=[]
    o=[]
    for op in j[_entity_type]: # _entity_type will be "parties" for organization & person    
        if op.has_key("type"): # only parties and custom fields will have a type
            if op["type"] != entity_type:
            #if op["type"] != _entity_sub_type:
                continue
    
        if objid!=-1:
            if op["id"] == int(objid):
                h,_o = _unpack(op,format)
                o.append(_o)
            else:
                continue
        else:
            h,_o = _unpack(op,format)
            o.append(_o)
    
    fh = open(ofile,'w+')
    fh.write("^".join(h))
    fh.write("\n")
    for _o in o:
        if len(_o) == int(col_count) or col_count == -1:
            ___o=[]

            try:
                fh.write("^".join(_o))
                fh.write("\n")
            except:
                 print _o
  	         print "ERROR:cannot process"
        else:
            print "ERROR:num columns != " + str(len(_o)) + "[" + str(col_count) + "]"
            print _o
    fh.close


    #return responses

def _notnull(value):
    if value!="null" and value!="None" and value != "" and value!=None:
        return True
    return False
        
def write_api(access_token,entities,write_type,entity_type,dryrun=False):
   
    ignore_fields = ["","None","createdAt","updatedAt","lastContactedAt",
                     "id","lastStageChangedAt",
                     "owner","party","lastOpenMilestone"]
    
    #custom_fields=[]
    custom_fields=["Org Group","State","Product","Primary Rev Model",
                   "Summary Status","Secondary Rev Model",
                   "Client Type","Client Size","Client Description","Last Summary Status","Summary Status Date","Source","Source Date"]
    
    url,_entity_type,sub_entity_type =_geturl(entity_type)
    
    if entity_type == "opportunity":
        #organisation_nvp = dump_nvp(access_token,"organisation")
        #milestones_nvp = dump_nvp(access_token,"milestones")
        #lostreasons_nvp = dump_nvp(access_token,"lostreasons")
        #users_nvp = dump_nvp(access_token,"users")
        #tags_nvp = dump_nvp(access_token,"opportunity_tags")
        #customfieldslist_nvp = dump_nvp_no_sub_type(access_token,"opportunities_custom_fields_list")
        #custom_fields = customfieldslist_nvp.keys()
        if write_type in ["update","delete"]:
            opportunity_nvp = dump_nvp(access_token,"opportunity",lookupkey="id",lookupvalue="name")
            opportunity_byname_nvp = dump_nvp(access_token,"opportunity")
        
    elif entity_type == "organisation":
        #organisation_nvp = dump_nvp(access_token,"organisation")
        #users_nvp = dump_nvp_no_sub_type(access_token,"users")
        #customfieldslist_nvp = dump_nvp_no_sub_type(access_token,"organisation_custom_fields_list")
        #custom_fields = customfieldslist_nvp.keys()
        pass
    elif entity_type == "person":
        #person_nvp = dump_nvp(access_token,"person",lookupkey=["firstName","lastName"])
        #users_nvp = dump_nvp_no_sub_type(access_token,"users")
        #organisation_nvp = dump_nvp(access_token,"organisation")
        customfieldslist_nvp = dump_nvp_no_sub_type(access_token,"person_custom_fields_list")
        custom_fields = customfieldslist_nvp.keys()
    elif entity_type == "note":
        users_nvp = dump_nvp(access_token,"users",lookupkey="username")
        organisation_nvp = dump_nvp(access_token,"organisation")
        opportunity_nvp = dump_nvp(access_token,"opportunity")
    elif entity_type == "tasks":
        organisation_nvp = dump_nvp(access_token,"organisation")
        milestones_nvp = dump_nvp(access_token,"milestones")
        lostreasons_nvp = dump_nvp(access_token,"lostreasons")
        users_nvp = dump_nvp(access_token,"users")
        tasks_nvp = dump_nvp(access_token,"tasks", lookupkey="description")
        tags_nvp = dump_nvp(access_token,"opportunity_tags")
        customfieldslist_nvp = dump_nvp_no_sub_type(access_token,"opportunities_custom_fields_list")
        opportunity_nvp = dump_nvp(access_token,"opportunity")
        kases_nvp = dump_nvp(access_token,"kases")
        categories_nvp = dump_nvp(access_token,"categories")
    elif entity_type == "kases":
        users_nvp = dump_nvp(access_token,"users")
        organisation_nvp = dump_nvp(access_token,"organisation")
        opportunity_nvp = dump_nvp(access_token,"opportunity")
        
    orig_write_type = write_type
    
    responses={"success":[],"failure":[],"skip":[]}
    for entity in entities:
        
        write_type = orig_write_type # in case we switch to add 
        
        _id=""
        #_id=""
        _data={}
        fields=[]
        for key,value in entity:
            
            key = remove_non_ascii(key)
            
            value = remove_non_ascii(value)
            
            
            if key=="id":
                if write_type=="update":
                    _id=value
                else:
                    #_data[key]=value
                    pass
            elif key=="name" and write_type in ["update","delete"]:
                
                if entity_type == "organisation":
                    if organisation_nvp.has_key(value) == False:
                        print "NEED TO ADD: [" + value + "] organisation not found"
                        _data["type"]=entity_type
                        write_type="add"
                        _data["name"]=value
                        #_id=-1
                    else:
                        _id=organisation_nvp[value]
                elif entity_type == "opportunity":
                    if _id != "": #treat name like any other field, id is the key
                        _data[key]=value
                    elif opportunity_byname_nvp.has_key(value) == False:
                        print "NEED TO ADD: [" + value + "] Opportunity not found"
                        _data["type"]=entity_type
                        _data["name"]=value
                        write_type="add"
                        #_id=-1
                    else:
                        _id=opportunity_byname_nvp[value]
                elif entity_type == "person":
                    if opportunity_nvp.has_key(value) == False:
                        print "NEED TO ADD: [" + value + "] Person not found"
                        _data["type"]=entity_type
                        _data["name"]=value
                        write_type="add"
                        #_id=-1
                    else:
                        _id=person_nvp[value]
            elif key=="description" and write_type=="update":
                
                if entity_type == "tasks":
                    if tasks_nvp.has_key(value) == False:
                        print "NEED TO ADD: [" + value + "] task not found"
                        _data["type"]=entity_type
                        write_type="add"
                        _data["name"]=value
                        #_id=-1
                    else:
                        _id=tasks_nvp[value]

         
            elif key=="fullName":
                if write_type=="update" or write_type=="delete":
                    if person_nvp.has_key(value) == False:
                        print "ADDING: [" + value + "] Person not found"
                        _data["type"]=entity_type
                        #_data["name"]=value
                        write_type="add"
                    else:
                        _id=person_nvp[value]
            elif key=="tags":
                _data["tags"] =[]
                for _tag in value.split(","):
                    if tags_nvp.has_key(_tag) == False:
                        data={"tag":{"name":_tag,"dataTag" : False}}
                        _url = url+"/tags"
                        requests.put(_url, headers=_header(access_token), data=json.dumps(data))
                    _data["tags"].append({"name":_tag,"dataTag" : False})
                        
            elif key=="client": # column name of organisation when updating opportunities
                if value!="None" and value!="":
                    if organisation_nvp.has_key(value) == True:
                        _data["party"] = {"id":organisation_nvp[value]}
                        
            elif key=="organisation":
                _data[key] = {"id":int(value)}
                #if value!="None" and value!="":
                #    if organisation_nvp.has_key(value) == True:
                #        _data[key] = {"id":organisation_nvp[value]}
                #    else:
                #        print "ADDING: [" + value + "] organisation not found"
                #        _data["type"]=entity_type
                #        write_type="add"
                #        #print "ERROR: [" + value + "] Cannot update as organisation not found"
                
                #if write_type=="update":
                #    if organisation_nvp.has_key(value) == True:
                #        #_id=organisation_nvp[value]     
		#
               	#    else:
                #        print "ERROR: [" + value + "] Cannot update as organisation not found"
            elif key in ["lostReason"]:
                if value!="null" and value!="None" and value != "Not Lost":
                    _data[key]={"id":lostreasons_nvp[value],"name":value}


                        
            elif key in ["probability"]:
                _data[key] = int(value)
            elif key in ["options"]:
                _data[key] = value.split("$")
            elif key in ["activityType"]:
                _data[key] = int(value)
            elif key in ["value"]:
                (amount,currency) = value.split("$")
                if amount!="None":
                    _data["value"] = {"amount":int(amount), "currency":currency}
            elif key == "icon":
                isSystem,displayName,order,iconName,id = value.split("$")
                _data["value"]= {'isSystem': isSystem, 'displayName': displayName, 
                        'order': order, 'iconName': iconName, 'id': id}
                
            elif key == "party":
                if _notnull(value) == True:
                    _data[key]={"id":int(value)}
                    #_data[key]={"id":organisation_nvp[value]}
            elif key == "opportunity":
                if _notnull(value) == True:
                    _data[key]={"id":opportunity_nvp[value]}
            elif key in ["milestone","lastOpenMilestone"]:
                if value!="null" and value!="None":
                    _data[key]={"id":milestones_nvp[value],"name":value}
            elif key in ["category"]:
                if _notnull(value) == True:
                    _data[key]={"id":categories_nvp[value],"name":value}
            elif key in ["kase"]:
                if _notnull(value) == True:
                    _data[key]={"id":kases_nvp[value],"name":value}
                        
                        
            elif key in ["addresses"]:
                a=[]
                for address in value.split("$"):
                    a.append({"street":address})
                _data["addresses"]=a
            elif key in ["emailAddresses"]:
                a=[]
                if value!="":
                    for address in value.split("$"):
                        a.append({"address":address})
                    _data["emailAddresses"]=a
                
            elif key in ["phoneNumbers"]:
                a=[]
                for phone in value.split("$"):
                    if phone != '':
                        a.append({"number":phone})
                
                if a!=[]:
                    _data["phoneNumbers"]=a
                                    
            elif key in ["owner"]:
                if value!="null":
                    _data[key]={"id":users_nvp[value]}
            elif key in ["creator"]:
                _data[key]={"id":users_nvp[value]}
            elif key in custom_fields:
                if value=="None":
                    fields.append({"definition": {"id":customfieldslist_nvp[key],"name":key},
                                   "value":"None"})
                elif value!="null":
                    fields.append({"definition": {"id":customfieldslist_nvp[key],"name":key},
                                   "value":value})
                pass
            elif key == "duration":
                if value == "None":
                    _data[key] = int(0)
		else:
                    _data[key] = int(value)
            elif key == "dataTag":
                if value == "False":
                    _data[key] = False
                elif value == "True":
                    _data[key] = True
            else:
                if value!="" and value !="None" and key not in ignore_fields:
                    _data[key]=value
        
        if fields!=[]:
            _data["fields"]=fields
        #data={"party":_data}
        data={sub_entity_type:_data}
        
        
        if write_type=="update":
            #sleep(0.25) 
		 
            if _id!=-1: # temp thing to stop failing on intra update adds
                #if entity_type=="person":
                #    _url = url+"/"+str(_id)
                #else:
                _url = url+"/"+str(_id)+'?embed=fields'
                #pass
               
                #print "_update compare:" + _url
                
                try:
                    response = requests.put(_url, headers=_header(access_token), data=json.dumps(data))
                except:
                    print "failed put waiting for 60 secs to try again"
                    sleep(60)
                    response = requests.put(_url, headers=_header(access_token), data=json.dumps(data))
        
                if response.status_code in [201,200,204]:
                     #print str(response.status_code) + ":" + _url
                     sys.stderr.write(".")
                else:
                     print "error:" + str(response.status_code) + " " + response.text + ":" + _url

                #if _compare(access_token,_id,entity_type,data) == False and dryrun==False:  
                #    print "_update compare:" + _url
                #    response = requests.put(_url, headers=_header(access_token), data=json.dumps(data))
                   
                #    status="failure"
                #    if response.status_code in [201,200]:
                #        status="success"
                #    else:
                #        print response.json()['errors']
                #    responses[status].append((response.json(),response,url,data))
                #else:
                #    responses['skip'].append((666))
                continue
            else:
                continue
                
        elif write_type=="add":
            sleep(0.5) 
            _url = url+'?embed=fields,tags'
            #+'?embed=fields'
        elif write_type=="delete":
            sleep(1) 
            _url = url+"/"+str(_id)
            response = requests.delete(_url, headers=_header(access_token))
            status="failure"
            if response.status_code in [201,200,204]:
                status="success"
            else:
                print _data
                print response.json()
            responses[status].append((response,_url))
            continue
        else:
            _url = url+'?embed=fields'
            
        if  dryrun==False:
            print "_update compare:" + _url
            response = requests.post(_url, headers=_header(access_token), data=json.dumps(data))
            status="failure"
            if response.status_code in [201,200]:
		print ".",
                status="success"
                print status,write_type,_data
            else:
                print
                print _data
                print response.json()
            responses[status].append((response.json(),response,url,data))
        else:
            responses['skip'].append((666))
            

        
    return responses

def run(action,ofile,entity,entity_type,env='prod',action_type='csv',filter='nofilter'):

    latest=now(format="%H%M%S_%Y%m%d")

    if entity in ["opportunity","milestones","opportunities_custom_fields","entries"]:
        entity_type=entity # opportunity has no subtype
    elif entity=="opportunity_tags":
        entity_type=entity

    if env=="dev":
        access_token = "kBtqQU5lrQ5tVfn3Ngz04BhcSyWWGJ2Nycz+ODFdXOdPTur9FVmhw3wN3bs6TOhC"
    elif env=="prod":
        access_token = "4rY0P12jmfi0iq41S0mtuFqygXwoirn6Q2gA8+nvjBgTUlRzNqrOla27EeJcYkAs"
    else:
        print "ERROR: env="+env

    func = "read_api"
    args=[access_token]
    kwargs={}
    numrows=-1

    if action in ["add","update"]:
        func = "write_api"
        _args=[ofile]
        if numrows!=-1: _args.append(int(numrows))
        rows=importcsv(*_args)
        args = args + [rows,action,entity_type]
    elif action in ["dump"]:
        func="dump"
        args = args + [entity_type,objid]
        kwargs = {"verbose":True}
    elif action in ["delete"]:
        func="delete"
        args = args + [entity_type,objid]
    elif action in ["delete_all"]:
        func="delete_all"
        args = args + [entity_type]
    elif action in ["delete_party"]:
        _args=[ofile]
        func="delete_party"
        rows=importcsv(*_args)
        args = args + [entity_type,rows]
    elif action in ["add_party"]:
        _args=[ofile]
        func="add_party"
        rows=importcsv(*_args)
        args = args + [entity_type,rows]
    elif action in ["delete_list"]:
        _args=[ofile]
        func="delete_list"
        rows=importcsv(*_args)
        args = args + [entity_type,rows]
    else:
        args = args + [objid,entity_type,action_type,ofile,col_count,filter]

    responses = globals()[func](*args,**kwargs)


if __name__ == "__main__":


    '''
    python ./capsulecrm.py entity=party ]
                            entity_type=organisation 
                            action=update 
                            ofile=/tmp/capsuledumpparty2.csv 
                            env=dev 
                            
    python ./capsulecrm.py entity=party 
                           entity_type=organisation 
                           action=read
                           
    python ./capsulecrm.py entity=party 
                           entity_type=milestones 
                           action=read
                            
    python ./capsulecrm.py entity=opportunity action=read env=prod
                           
    python ./capsulecrm.py entity=opportunity 
                           action=read 
                           env=prod 
                           objid=8244650

    python ./capsulecrm.py entity=opportunity 
                           action=dump 
                           env=prod 
                           objid=8244650
                           
    python ./capsulecrm.py entity=party
                           entity_type=organisation 
                           action=add 
                           ofile=/tmp/party_read_dev.csv 
                           env=dev
python ./capsulecrm.py entity=opportunity objid=8318119 action=dump env=prod

python ./capsulecrm.py entity=party entity_type=opportunities_custom_fields_list env=prod action=read
python ./capsulecrm.py entity=party entity_type=opportunities_custom_fields_text env=prod action=read

python ./capsulecrm.py entity=party entity_type=organisation action=delete objid=188680763 env=dev

python ./capsulecrm.py entity=party entity_type=organisation action=delete_all env=dev
python ./capsulecrm.py entity=party entity_type=users env=prod action=read
python ./capsulecrm.py entity=entry entity_type=note env=prod action=read
python ./capsulecrm.py entity=entry entity_type=email env=prod action=read
 
    '''    
    

    for cfg in sys.argv[1:]:
        (k,v) = cfg.split("=")
        if v in ["True","true"]: v =True
        if v in ["False","false"]: v =False

        locals()[k] = v


    run(action,ofile,entity,entity_type,env)

