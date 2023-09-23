import sys
import os
from prettytable import PrettyTable
from veloxutils import process_args,recover, removeunicode, get_entity_fields, iter_entity_fields, parse_custom_fields, clean, _get_set, get_query, persist, all_custom_fields, sort_dict_of_lists_by_count
import pprint

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]

entities = recover(entity)
index={}
stats={"success":0,"fail":0,"errors":{}}

class NoKey(Exception):
    pass

def _add_fail(e,section,message=None):
    stats["fail"]=stats["fail"]+1

    if stats["errors"].has_key(section) == False:
        stats["errors"][section]={}

    _section=stats["errors"][section]

    if _section.has_key(e.message) == False:
        _section[e.message] = 1
    else:
        _section[e.message] = _section[e.message] + 1

if entity_key.find("|") != -1:
    _entity_keys = entity_key.split("|")
else:
    _entity_keys = [entity_key]

for _entity in entities:
    if _entity == "timestamp":
        continue

    _record = entities[_entity]
    #{u'definition': {u'id': 680167, u'name': u'Seniority'}, u'tagId': None, u'id': 255443187, u'value': u'UNKNOWN_SENIORITY'}

    section="index_key_exists"
    try:
        entity_key=""
        for _entity_key in _entity_keys:
            if _record.has_key(_entity_key)==True:
                entity_key=_entity_key
            elif _entity_key in all_custom_fields:
                for _field in _record["fields"]:
                    if _field["definition"]["name"]==_entity_key:
                        entity_key=_entity_key
            else:
                pass

        if entity_key=="":
            raise NoKey(entity+" does not have key " + entity_key)

    except Exception, e:
        _add_fail(e,section,_record)
        continue

    section="retreiving_indexes"
    try:
        if _record.has_key(entity_key)==True:
            if _record[entity_key] != None:
                if locals().has_key("subentity_key"):
                    if(isinstance(_record[entity_key], list)) == True:
                        _index = _record[entity_key][0][subentity_key]
                    else:
                        _index = _record[entity_key][subentity_key]
                else:
                    _index = _record[entity_key]
        elif entity_key in all_custom_fields:
            for _field in _record["fields"]:
                if _field["definition"]["name"]==entity_key:
                    _index = _field["value"]
                    continue
        else:
            continue
    except Exception, e:
        _add_fail(e,section,_record)
        continue

    section="writing_results"
    try:
        if isinstance(_index, list) == False:
            _index = [_index]

        for __index in _index:
            if index.has_key(__index) == True:
                index[__index].append(_entity)
            else:
                index[__index]=[_entity]
            stats["success"]=stats["success"]+1
    except Exception, e:
        _add_fail(e,section,_record)


pickle_name = entity+"_"+entity_key.replace(" ","_").lower()+".pickle"
persist(index,pickle_name,True)

#pprint.pprint(index)
print pickle_name
print stats
for _index in index:
    print _index,len(index[_index])
