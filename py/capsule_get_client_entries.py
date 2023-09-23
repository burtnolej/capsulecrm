import sys
from veloxutils import process_args,recover

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]

entries = recover(dbentries_by_partyid)

if thisid!=None:
    if entries.has_key(thisid) == True:
        print "this id=" + thisid + " numentries:"+str(len(entries[thisid]))

elif inputfile!=None:
    fh_out = open(outputfile,'w+')
    fh = open(inputfile,'r+')
    for _line in fh:
	(_id,_name) = _line.replace("\r","").replace("\n","").split("^")
	if entries.has_key(_id) == True:
            for _entry in entries[_id]:
                _output=[_name,str(_entry["id"]),str(_id)]
                print _output
                fh_out.write("^".join(_output)+"\n")
    fh_out.close()
    fh.close()
