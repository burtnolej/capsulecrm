import sys
import os
from prettytable import PrettyTable
from veloxutils import process_args,recover, removeunicode, get_entity_fields, iter_entity_fields, parse_custom_fields, clean, _get_set, get_query

_args = process_args(sys.argv,["entity"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

entities = recover(entity,pickledir=dircapsulepickle)

errors=[]
rowcount=0
_columns=[]
_output=[]
def _print_table(t):
   if outputfile!=None:
       fh =open(outputfile,"w+")
       fh.write(t.get_string())
       fh.close()
   else:
       print t 

def _append(row,value):

    def __append(row,value):
        try:
            value = str(value).replace("\n","")
            _value = removeunicode(str(value))
            row.append(_value)
        except Exception, e:
            row.append("encoding error:"+e.message)

    if isinstance(value,dict)==True:
        if value.has_key("name"):
            __append(_row,value["name"])
        elif value.has_key("amount"):
            __append(_row,value["amount"])
        else:
            __append(_row,value)
    elif isinstance(value,list)==True:
        if len(value)>0:
            if value[0].has_key("number"):
                __append(_row,value[0]["number"])
            elif value[0].has_key("address"):
                __append(_row,value[0]["address"])
            else:
                __append(_row,value)
        else:
            __append(_row,"NOTSET")
    elif isinstance(value,type(None))==True:
        __append(_row,"NOTSET")
    else:
        __append(_row,value)

if outputfields!=None:
    _columns=outputfields
    t=PrettyTable(_columns) 

for _entity in entities:
    if _entity=="timestamp":
        continue

    _row=[]
    _thisentity= entities[_entity]

    if outputfields=="model":
         for _outputfield in iter_entity_fields("address",entity):
              if _thisentity.has_key(_outputfield):
                  _append(_row,_thisentity[_outputfield])
              else:
                  _append(_row,"NOTSET")
         for _outputfield in iter_entity_fields("core",entity):

              if _thisentity.has_key(_outputfield):
                  _append(_row,_thisentity[_outputfield])
              else:
                  _append(_row,"NOTSET")


         for _outputfield in iter_entity_fields("date",entity):
              if _thisentity.has_key(_outputfield):
                  if _thisentity[_outputfield] != None:
                      if isinstance(_thisentity[_outputfield],int) == True:
                          # this is the empty row case when date is equal to -1
                          _append(_row,_thisentity[_outputfield])
                      else:
                          _append(_row,_thisentity[_outputfield][:10])
                  else:
                       _append(_row,"NOTSET")
              else:
                  _append(_row,"NOTSET")
         for _outputfield in iter_entity_fields("custom",entity):
              _pcf = parse_custom_fields(_thisentity)
              if _pcf.has_key(_outputfield):
                  _append(_row,_pcf[_outputfield])
              else:
                  _append(_row,"NOTSET")

         _columns=get_entity_fields(entity)
         t=PrettyTable(_columns) 
    elif outputfields!=None:
         for _outputfield in outputfields:
              try:
                  if entities[_entity].has_key(_outputfield):
                       _append(_row,entities[_entity][_outputfield])
                  else:
                       _append(_row,"NOTSET")
 
              except:
                  errors.append((_outputfield,_entity))
    else:
         if _entity != "timestamp" and isinstance(entities[_entity],dict)==True:
              for _outputfield in entities[_entity].keys():
                  if _outputfield == "fields":
                      for i in range(0,len(entities[_entity][_outputfield])):
                          _append(_row,entities[_entity][_outputfield][i]["value"])
                  elif isinstance(entities[_entity][_outputfield],dict)==True:
                      if entities[_entity][_outputfield].has_key("name"):
                          _append(_row,entities[_entity][_outputfield]["name"])
                      elif entities[_entity][_outputfield].has_key("amount"):
                          _append(_row,entities[_entity][_outputfield]["amount"])
                      else:
                          _append(_row,entities[_entity][_outputfield])
                  elif isinstance(entities[_entity][_outputfield],list)==True:
                      if len(entities[_entity][_outputfield])>0:
                          if entities[_entity][_outputfield][0].has_key("number"):
                              _append(_row,entities[_entity][_outputfield][0]["number"])
                          elif entities[_entity][_outputfield][0].has_key("address"):
                              _append(_row,entities[_entity][_outputfield][0]["address"])
                          else:
                              _append(_row,entities[_entity][_outputfield])
                      else:
                          _append(_row,"NOTSET")

                  elif entities[_entity].has_key(_outputfield):
                      _append(_row,entities[_entity][_outputfield])
                  else:
                      _append(_row,"NOTSET")
         else:
              print "not dict"

    if len(_columns) == len(_row):
        t.add_row(_row)
        _output.append(_row)
    else:
        print "error"

    if rowcount==topn and outputtype=="table":
         sys.stderr.write("topn="+str(topn)+"\n")
         _print_table(t)
         exit()
    rowcount=rowcount+1

if outputtype=="table":
    _print_table(t)
elif outputtype=="list":
    print "writing rows  " + str(len(_output)) + " to " + outputfile
    fh =open(outputfile,"w+")
    fh.write("^".join(_columns)+"\n")
    for _outputrow in _output:
        try:
            fh.write("^".join(_outputrow)+"\n")
        except Exception, e:
            sys.stderr.write(e.message + ":" + e.object + "\n")

    fh.close()

