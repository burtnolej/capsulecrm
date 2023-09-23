import sys
from veloxutils import process_args,recover, removeunicode

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]

persons_by_partyid = recover(dbpersons_by_partyid)
persons = recover(dbpersons)

if thisid!=None:
    if persons.has_key(thisid) == True:
        print "this id=" + thisid + " numentries:"+str(len(persons[thisid]))

elif inputfile!=None:
    fh_out = open(outputfile,'w+')
    fh = open(inputfile,'r+')
    for _line in fh:
	(_id,_name) = _line.replace("\r","").replace("\n","").split("^")
	if persons_by_partyid.has_key(int(_id)) == True:
            for _person in persons_by_partyid[int(_id)]:
                _output=[_name,str(_person),str(_id), \
                    removeunicode(persons[_person]["firstName"]), \
                    removeunicode(persons[_person]["lastName"]), \
                    removeunicode(persons[_person]["Notes"]),]
                print _output
                fh_out.write("^".join(_output)+"\n")
    fh_out.close()
    fh.close()
