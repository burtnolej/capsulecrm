import fnmatch

field_types=["core","custom","date","address"]
entity_types=["person","organisation","opportunities","entries"]

person_filter = {"filter": { "conditions": [ {"field":"type", "operator":"is", "value":"person"} ] } }
organisation_filter = {"filter": { "conditions": [ {"field":"type", "operator":"is", "value":"organisation"} ] } }

# person
person_core_fields=["Contact Owner","firstName","id","jobTitle","lastName","organisation","owner","phoneNumbers","team","title"]
person_custom_fields=["Job Type","Department","Sub Department","Seniority","LinkedInURL","Notes"]
person_date_fields=["lastContactedAt","createdOn","updatedOn"]
person_address_fields=["emailAddresses"]
person_dict_fields=[]


# organisation
organisation_core_fields=["name","phoneNumbers","team","owner","id"]
organisation_custom_fields=["Company Type","Company Size","Head Region","Notes"]
organisation_date_fields=["createdOn","updatedOn"]
organisation_dict_fields=[]
organisation_address_fields=["emailAddresses"]
organisation_update_fields ={"person":"organisation","opportunities":"party","entries":"party"}

# opportunities
opportunities_core_fields=["name","description","value","owner","durationBasis","milestone","duration","party","lostReason","id"]
opportunities_custom_fields=["Product","Rev Model","Lead Source","Campaign"]
opportunities_date_fields=["expectedCloseOn","lastContactedAt","lastStageChangedAt","closedOn","createdOn","updatedOn"] 
opportunities_address_fields=[]
opportunities_dict_fields=["milestone"]

#entries
entries_core_fields=["id","content","subject","creator","activityType"]
entries_custom_fields=[]
entries_address_fields=[]
entries_date_fields=["entryAt","createdAt","updatedOn"]
entries_dict_fields=["creator","activityType","party"]

_list_name = "all_address_fields"
locals()[_list_name] =[]
for _entity_type in entity_types:
    locals()[_list_name] = locals()[_list_name] + locals()[_entity_type+"_address_fields"]

for _field_type in field_types + ["dict"]:
    _list_name = "all_"+_field_type+"_fields"
    locals()[_list_name] =[]
    for _entity_type in entity_types:
        locals()[_list_name] = locals()[_list_name] + locals()[_entity_type+"_"+_field_type+"_fields"]

def matchkey(index,pattern):
    return  fnmatch.filter(index.keys(), pattern)

def has_a(index,parent_id):
    if index.has_key(parent_id)==True:
        if len(index[parent_id]) > 0:
            return index[parent_id]
    return []

def get_multi_field(entities,entity_id,entity_fields):
    result=[]
    for _entity_field in entity_fields:
        result.append(get_field(entities,entity_id,_entity_field))
    return result

def get_field(entities,entity_id,entity_field):

    if globals().has_key("get_"+entity_field+"_field"):
        return globals()["get_"+entity_field+"_field"](entities,entity_id,entity_field)

    for field_type in field_types:
        if entity_field in globals()["all_"+field_type+"_fields"]:
            _field_value = globals()["get_"+field_type+"_field"](entities,entity_id,entity_field)
            if _field_value == None:
                _field_value=""
            return _field_value
    return -1


def get_id_field(entities,entity_id,entity_field):
    return str(entities[entity_id][entity_field])

def get_content_field(entities,entity_id,entity_field):
    _content =  entities[entity_id][entity_field]
    if _content != None:
        return _content.replace("\n","$$")
    else:
        return "None"

def get_phoneNumbers_field(entities,entity_id,entity_field):
    _result=""
    for _number in entities[entity_id][entity_field]:
        if _result == "":
            _result = _number["number"]
        else:
            _result = _result + " " + _number["number"]

    return _result

def get_address_field(entities,entity_id,entity_field):
    #if entity_field in globals()["all_address_fields"]:
        _result=""
        for _address in entities[entity_id][entity_field]:
            if _result == "":
                _result = _address["address"]
            else:
                _result = _result + " " + _address["address"]

        return _result

def get_core_field(entities,entity_id,entity_field):

    for field_type in field_types:
        if entity_field in globals()["all_dict_fields"]:
            if entities[entity_id][entity_field] != None and entities[entity_id][entity_field].has_key("name"):
                return entities[entity_id][entity_field]["name"]
            else:
                return "no name field"
    try:
        return entities[entity_id][entity_field]
    except:
        return "field not exist"

def get_date_field(entities,entity_id,entity_field):
    return entities[entity_id][entity_field][:10]

def get_custom_field(entities,entity_id,entity_field):
    fields=entities[entity_id]["fields"]
    for _field in fields:
        if _field["definition"]["name"].replace(" ","_").lower() == entity_field.replace(" ","_").lower():
            return _field["value"]
    return -1

def parse_custom_fields(entity):
    _pcf = {}
    for i in range(0,len(entity["fields"])):

        _field = entity["fields"][i]["definition"]["name"]
        _value = entity["fields"][i]["value"]
        _pcf[_field]=_value

    return _pcf

def iter_entity_fields(field_type,entity):
    return(iter(globals()[entity+"_"+field_type+"_fields"]))

def get_entity_fields(entity):
    return(globals()[entity+"_core_fields"]+globals()[entity+"_date_fields"]+globals()[entity+"_custom_fields"])
