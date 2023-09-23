import sys
import operator
from veloxutils import process_args,recover,sort_dict_by_value,get_field_uniq_value_counts
from prettytable import PrettyTable

_args = process_args(sys.argv,_must_be_set="entity")
for _arg in _args:
    locals()[_arg] = _args[_arg]


entities=[entity]
print "recovering " + entity
locals()[entity+"_obj"]=recover(entity)

fields=["createdAt","updatedAt"]

def _init_rows(listsize):
    return([[] for i in range(0,listsize)])

def _get_sorted_dict_table_rows(object,field,rows,tablerow,topn):
    uniq_created=get_field_uniq_value_counts(object,field,10)
    sorted_dict=sort_dict_by_value(uniq_created,topn)
    for r in sort_dict_by_value(uniq_created,topn):
        rows[tablerow].append((r,uniq_created[r]))
        tablerow=tablerow+1
    return rows

topn=10
rows = []

t = PrettyTable(["name","dbnumrows","timestamp"])
try:
    t.add_row([entity,len(locals()[entity+"_obj"].keys()),\
        locals()[entity+"_obj"]["timestamp"]])
except Exception as error:
    print _entity+":an error has occurred:"+ type(error).__name__ + "-"+str(error)
    
print(t)


for _field in fields:
    rows = _init_rows(topn)
    rows = _get_sorted_dict_table_rows(locals()[entity+"_obj"],_field,rows,0,topn)

    t = PrettyTable(entities)
 
    for i in range(0,len(rows)):
        if len(rows[i]) > 0:
            t.add_row(rows[i])

    print _field,"topn="+str(topn) 
    print(t)



