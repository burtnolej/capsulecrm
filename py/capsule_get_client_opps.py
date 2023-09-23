import sys
from veloxutils import process_args,recover

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]

_opps = recover(dbopps_by_partyid)

if thisid!=None:
    if _opps.has_key(thisid) == True:
        print "this id=" + thisid + " numopps:"+str(len(_opps[thisid]))
elif inputfile!=None:
    fh = open(inputfile,'r+')
    fh_out = open(outputfile,'w+')
    for _line in fh:
        (_id,_name) = _line.replace("\r","").replace("\n","").split("^")
        if _opps.has_key(int(_id)) == True:
            for _opp in _opps[int(_id)]:
                 _output=[_name,str(_opp["id"]),str(_id),_opp["name"]]
                 print _output
                 fh_out.write("^".join(_output)+"\n")
 
    fh.close()
    fh_out.close()
