import sys
import os
from prettytable import PrettyTable
from veloxutils import *
import pprint

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]
    
person = recover("person")
organisation = recover("organisation")

entries = recover("entries_parties",True)
opportunities = recover("opportunities_party",True)   

person_join={}

for _person in person:
    _person_join = {}
    if _person != "timestamp":
        _person_fields={}
        _organisation_fields={}
        if person[_person]["organisation"] != None:
            _organisation_id = person[_person]["organisation"]["id"]
            if opportunities.has_key(_organisation_id) == True:
                _organisation_opportunities = opportunities[_organisation_id]
            else:
                _organisation_opportunities=[]
                
            if entries.has_key(_person) == True:
                _entries_person = entries[_person]
            else:
                _entries_person=[]
                
            _organisation_fields = get_multi_field_raw(organisation,_organisation_id,get_entity_fields_raw("organisation"),True) 
            _organisation_fields.pop("emailAddresses")
            _organisation_fields["orgUpdatedAt"] = _organisation_fields.pop("updatedAt")
            _organisation_fields["orgCreatedAt"] = _organisation_fields.pop("createdAt")
            _organisation_fields["orgId"] = _organisation_fields.pop("id")
        else:
            _organisation_id=-1
            _organisation_opportunities=[]
            _entries_person=[]
            _organisation_fields = dict(organisation_empty_dict)
        
        _person_fields = get_multi_field_raw(person,_person,get_entity_fields_raw("person"),True)
        
        # pull out the 'fields' otherwise they get overwritten     
        _person_custom_fields=_person_fields.pop("fields")
        
        if _organisation_fields.has_key("fields") == False:
            pass
        else:
            _organisation_custom_fields=_organisation_fields.pop("fields")
            
        _person_custom_fields=_person_custom_fields+_organisation_custom_fields
        
        _person_join.update(_person_fields)
        _person_join.update(_organisation_fields)
        _person_join["fields"]=_person_custom_fields # add back the 'fields'
        
        _person_join["Opportunity Count"] = len(_organisation_opportunities)
        _person_join["Entries Count"] = len(_entries_person)
        
        if len(_person_join["emailAddresses"])>0:
            _person_join["Email Flag"] = 1
        else:
            _person_join["Email Flag"] = 0

        person_join[_person]=_person_join

persist(person_join,persistfile,index=False,pickledir=dircapsulepickle)
