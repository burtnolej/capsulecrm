import sys
import os
from prettytable import PrettyTable
from veloxutils import *
import pprint

_args = process_args(sys.argv,["query_terms"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

#query_terms =[("person","Job Type","TECH"),("person","Seniority","SENIOR")]
#query_terms =[("person","Job Type","TECH"),("person","Seniority","CSUITE"),("person","Sub Department","EQUITIES"),("person","Department","LEADERSHIP")]
#query_terms =[("person","Job Type","TECH|TECH_OTHER"), \
#        ("person","Sub Department","EQUITIES|TRADING|CASH_EQUITIES"), \
#        ("person","Seniority","SENIOR|CSUITE")]
#
#query_terms =[("person","Sub Department","CLEARED_DERIVS"),("person","Seniority","CSUITE|SENIOR|MID_LEVEL")]

def inlocals(key):
    return globals().has_key(key)

def getlocal(key):
    return globals()[key]
        
def setlocal(key,value):
    globals()[key]=value

def _or(value):
    if value.find("|") == -1:
        value = [value]
    else:
        value = value.split("|")
    return value

results=[]
for entity,field,value in query_terms:
    value = _or(value)

    if inlocals(entity) == False:
        index_name = entity+"_"+field.replace(" ","_").lower()
        pickle_name = index_name+".pickle" 
        setlocal(index_name,recover(pickle_name,True))
        if len(getlocal(index_name).keys())==0:
            sys.stderr.write("empty index returned for " + index_name)
            exit()

    _results=[]
    for _value in value:
        if getlocal(index_name).has_key(_value)==True:
            hits=getlocal(index_name)[_value]
            _results = _results + hits
    results.append(_results)


query_results = get_intersect(results)

print str(len(query_results))+" results found"
# specifically for person results for campaignsd
entries = recover("entries")
fh =open(outputfile,"w+")
fh.write("^".join(outputfields))


for _entity in query_results:
     #fh.write("^".join(removeunicode(x) for x in get_multi_field(entries,_entity,["activityType","id","creator","subject","content","party","createdOn"]))+"\n")
     fh.write("^".join(str(removeunicode(x)) for x in get_multi_field(entries,_entity,outputfields))+"\n")
fh.close()
exit()

# specifically for person results for campaignsd
person = recover("person")
fh =open(outputfile,"w+")

fields=["firstName","lastName","jobTitle","Seniority","id","LinkedInURL","emailAddresses","phoneNumbers"]
fh.write("^".join(fields))
for _entity in query_results:
    #print get_core_field(person,_entity,"firstName")
    #print get_field(person,_entity,"firstName")
     fh.write("^".join(removeunicode(x) for x in get_multi_field(person,_entity,fields))+"\n")
fh.close()

