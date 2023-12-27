import sys
import os
from prettytable import PrettyTable
from veloxutils import *
import pprint

_args = process_args(sys.argv,["query_terms"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

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

query_results=[]
for query in query_terms:
    results=[]
    for entity,field,value in query:
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


    query_results = query_results + list(get_intersect(results))

print str(len(query_results))+" results found"

# specifically for person results for campaignsd
person = recover("person")
fh =open(outputfile,"w+")

fields=["firstName","lastName","jobTitle","Seniority","Job Type","Department","Sub Department","id","LinkedInURL","emailAddresses","phoneNumbers"]
fh.write("^".join(fields)+"\n")
for _entity in query_results:
    try:
        fh.write("^".join(removeunicode(str(x)) for x in get_multi_field(person,_entity,fields))+"\n")
    except:
        sys.stderr.write("could not remove unicode for " + str(_entity)+ "\n")
fh.close()

