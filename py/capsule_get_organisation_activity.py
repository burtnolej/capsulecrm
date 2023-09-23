from veloxutils import *
import pprint

def  generate_org_activity(all_results,ifile="../org_updates.csv"):
    entries_parties = recover("entries_parties",True)
    person_organisation = recover("person_organisation",True)
    opportunities_party = recover("opportunities_party",True)

    entries = recover("entries")
    person = recover("person")
    opportunities = recover("opportunities")
    organisation = recover("organisation")

    with open(ifile,"r+") as f:
        lines = f.readlines()
        for _line in lines[1:]:
            _line = _line.strip("\r\n")
            (old_name,new_name,old_id,new_id) = _line.split("^")
       
            try:
                results={}
                _results= has_a(person_organisation,int(old_id))
                if len(_results)>0:
                    results["person"]= _results

                _results = has_a(opportunities_party,int(old_id))
                if len(_results)>0:
                    results["opportunities"]= _results

                _results = has_a(entries_parties,int(old_id))
                if len(_results)>0:
                    results["entries"]=_results

            except Exception, e:
                print e, old_id

            if len(results.keys())>0:
                results["new_id"]=new_id
                results["old_name"]=old_name
                results["new_name"]=new_name
                all_results[old_id] = results
    return all_results

def process_org_activity(all_results):
    for _entities in ["person","opportunities","entries"]:
        filepath = os.path.join(os.environ["DIRCAPSULE"],"real_update/prod_data_"+_entities+"_update_"+now(dayonly=True)+".csv")
        with open(filepath,"w") as f:
            f.write("id^"+organisation_update_fields[_entities]+"\n")
            for _entity_id,_results in all_results.iteritems():
                if _entity_id != "timestamp":
                    if _results.has_key(_entities) == True:
                        for _entity in _results[_entities]:
                            f.write("^".join([str(_entity),str(_results["new_id"])])+"\n") 

    filepath = os.path.join(os.environ["DIRCAPSULE"],"real_update/prod_data_organisation_delete_"+now(dayonly=True)+".csv")
    with open(filepath,"w") as f:
        f.write("id^name\n")
        for _entity_id,_results in all_results.iteritems():
            if _entity_id != "timestamp":
                f.write(str(_entity_id)+"^"+_results["old_name"]+"\n")



_args = process_args(sys.argv,_must_be_set=["mode"])
for _arg in _args:
    locals()[_arg] = _args[_arg]

if mode=="persist":
    all_results={}
    generate_org_activity(all_results,input_file)
    persist(all_results,"tmp_org_activity.pickle")
    pprint.pprint(all_results)
elif mode=="recover":
    all_results = recover("tmp_org_activity")
    print all_results
    process_org_activity(all_results)
else:
    pass
