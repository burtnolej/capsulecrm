import sys
import datetime
import ast

all_categories=["Job Type","Sub Department","Seniority","Department"]

for cfg in sys.argv[1:]:
	(k,v) = cfg.split("=")
	if v in ["True","true"]: v =True
	if v in ["False","false"]: v =False
	locals()[k] = v

def _get_set(summary,term):
	category=term[0]
	value=term[1]
	return set(summary[category][value])

def _get_client_meta(client_name,clients):
#ClientSource=INITIAL;LinkedInFirm=INITIAL;

    client_type = "UNKNOWN"
    full_client_name = "UNKNOWN"

    if clients.has_key(client_name)==True:
            client_type = clients[client_name]["Company Type"]
            if clients[client_name].has_key("Notes") == True:
                    try:
                        full_client_name = clients[client_name]["Notes"].split(";")[0].split("=")[1]
                    except:
                        pass

    return(client_type,full_client_name)

def _get_person_meta(results,_id):
	result=[results[_id]["firstname"],
       		results[_id]["lastname"], \
       		results[_id]["email"], \
       		_id, \
       		results[_id]["phone"], \
                results[_id]["organization"],
                results[_id]["jobtitle"]]

	for _category in all_categories:
		result.append(results[_id]["results"][_category])

	return result

def print_summary_query(summary,all_terms,outputtype,results,clients):

    superset=set()
    for terms in all_terms:
        term =ast.literal_eval(terms)
    
    set1=_get_set(summary,term[0])

    if len(all_terms)==1:
        superset=set1
    else:
        nextset=[]
        for _term in term[1:]:
            nextset=_get_set(summary,_term)
            nextset=list(set1.intersection(nextset))
        superset=superset.union(nextset)

    if outputtype=="count":
        print len(superset)
    elif outputtype=="list":
        fh = open(queryoutputfile,"w")

        for _id in superset:
            (client_type,_) = _get_client_meta(results[_id]["organization"],clients)
            _output = _get_person_meta(results,_id)
            _output.append(client_type)
            fh.write("^".join(_output)+"\n")
        fh.close()


def print_summary(summary):

	for category in summary.keys():
		for value in summary[category].keys():
			print category,value,len(summary[category][value])

def print_results(persons,clients):
	fh = open(outputfile,"w")
	_header=["id","jobtitle","SENIORITY","DEPTTYPE","SUBDEPTTYPE","JOBTYPE"]
	fh.write(",".join(_header)+"\n")
	for id in persons.keys():
 		(client_type,full_client_name) = _get_client_meta(results[id]["organization"],clients)
                _output = _get_person_meta(persons,id)
                _output.append(client_type)
                _output.append(full_client_name)
                fh.write("^".join(_output)+"\n")
	fh.close

def print_stats(persons):
	from collections import Counter
	stats = {"SENIORITY":[],"DEPTTYPE":[],"SUBDEPTTYPE":[],"JOBTYPE":[]}
	jobtitles=[]
	ids=[]
	for id in persons.keys():
		person = persons[id]
		results = person["results"]
		for category in ["SENIORITY","DEPTTYPE","SUBDEPTTYPE","JOBTYPE"]:
			stats[category].append(results[category])
		jobtitles.append(person["jobtitle"])
		ids.append(id)


	for category in ["SENIORITY","DEPTTYPE","SUBDEPTTYPE","JOBTYPE"]:
		print Counter(stats[category])

	for _category in stats.keys():
		jobtitles_unk=[]
		ids_unk=[]
		for i in range(0,len(stats[_category])):
			if stats[_category][i] == "UNKNOWN_"+_category:
				jobtitles_unk.append(jobtitles[i])
				ids_unk.append(ids[i])

		x = Counter(jobtitles_unk)
		itemcount=0
		for i in range(0,100):
			_output=[]
			_output.append(_category)
			_output.append("")
			_output.append("")
			_output.append(x.most_common()[i][0])
			_output.append(str(x.most_common()[i][1]))
			print "^".join(_output)
			itemcount=itemcount+x.most_common()[i][1]
		print itemcount


	
def get_rulesets(rulesfile):
	rulesets={}
	fh = open(rulesfile,"r+")
	for line in fh:
		line=line.replace("\"","")
		line=line.replace("\r","")
		line=line.replace("\n","")
		_line =line.split("^")

		if rulesets.has_key(_line[0])==True:
 			rulesets[_line[0]].append(_line)
		else:	
			rulesets[_line[0]] = [line.split("^")]
	fh.close()
	return rulesets

#name^phoneNumbers^team^owner^emailAddresses^id^createdAt^updatedAt^Company Type^Company Size^Head Region

def get_clients(clientsfile):
	clients={}
	fh = open(clientsfile,"r+")
	linecount=0
	for line in fh:
		if linecount!=0:
			_client = line.split("^")
  			client = {"id":_client[5]}
  			client["Company Type"] = _client[8]
  			client["Company Size"] = _client[9]
  			client["Company Region"] = _client[10]
  			client["Notes"] = _client[11]
  			_name = _client[0]

			clients[_name] = client
		else:
			linecount=linecount+1
	fh.close()
	return clients

#emailAddresses^Contact Owner^firstName^id^jobTitle^lastName^organisation^owner^phoneNumbers^team^title^lastContactedAt^createdAt^updatedAt^Job Type^Department^Sub Department^Seniority^LinkedInURL^Notes

def get_persons(personsfile):
	persons=[]
	fh = open(personsfile,"r+")
	linecount=0
	for line in fh:
		if linecount!=0:
			_person = line.split("^")
  			person = {"firstname":_person[2]}
  			person["lastname"] = _person[5]
  			person["jobtitle"] = _person[4]
  			person["organization"] = _person[6]
  			person["id"] = _person[3]
  			person["email"] = _person[0]
  			person["phone"] = _person[8]

			persons.append(person)
		else:
			linecount=linecount+1
	fh.close()
	return persons

def _not(value,nottest):
	if nottest==True and value == 1:
		return 0
	elif nottest==True and value == 0:
		return 1
	else:
		return value

def _testmatch(jobtitle,constraint,_match,testdepth,nottest=False):
	if jobtitle.find(constraint)==-1:
		_match=_match*_not(0,nottest)
        else:
        	_match=_match*_not(1,nottest)
        if DEBUG!=False:
        	print " "*testdepth,
                print "not_test_type="+str(nottest) + " jobtitle=" + jobtitle + " constraint=" + constraint + " matchstr=" + str(_match)
	return _match

def _update_summary(summary,value,_id):
	if summary[category].has_key(value) == True:
		_tmp = summary[category][value]
		_tmp.append(_id)
		summary[category][value] = _tmp
	else:
		summary[category][value] = [_id]
	return summary

def _update_results(person_results,ruleset,jobtitle,rule,category,value):
	if DEBUG!=False:
        	print ruleset + ":" + jobtitle + " MATCH [" + ",".join(rule)+"]"
        person_results[category]=value
	return person_results

t1 = datetime.datetime.now()
numtests=0


if locals().has_key("debug"):
	DEBUG=locals()["debug"]
else:
	DEBUG=False

if locals().has_key("outputfile"):
	outputfile=locals()["outputfile"]
else:
	outputfile="output.txt"

if locals().has_key("queryoutputfile"):
	queryoutputfile=locals()["queryoutputfile"]
else:
	queryoutputfile="queryoutput.txt"

if locals().has_key("mode"):
	mode=locals()["mode"]
else:
	mode="normal"

query=[]
for i in range(0,4):
	qname="query"+str(i)
	if locals().has_key(qname):
		query.append(locals()[qname])

if locals().has_key("outputtype"):
	outputtype=locals()["outputtype"]
else:
	outputtype="count"

if locals().has_key("echo"):
	echo=locals()["echo"]
else:
	echo=False

if locals().has_key("printstats"):
        printstats=locals()["printstats"]
else:
        printstats=False

persons = get_persons(locals()["personsfile"])
clients = get_clients(locals()["clientsfile"])
rulesets =get_rulesets(locals()["rulesfile"])
count =0
if mode!="recover":

    results={}
    summary={"Job Type":{},"Sub Department":{},"Seniority":{},"Department":{}}
    for _person in persons:
        _jobtitle= _person["jobtitle"]
        _id=_person["id"]

        if _id=="":
            id=time.time() * 1000
	
        person_results={}
        for _ruleset in rulesets.keys():
            for _rule in rulesets[_ruleset]:
                constraints = _rule[3].split("$$")
                category=_rule[0]
       	       	value=_rule[1]
                match=1

                for i in range(0,len(constraints)):
                    _constraint = constraints[i]
                    if _constraint.find("!")==-1:
                        match = _testmatch(_jobtitle,_constraint,match,i)
                    else:
                        _constraint=_constraint.replace("!","")
                        match = _testmatch(_jobtitle,_constraint,match,i,nottest=True)

                numtests=numtests+1
                if match==1:
                    #_update_results(person_results,_ruleset,_jobtitle,_rule,category,"UNKNOWN_"+category)
                    if DEBUG!=False:
                        print _ruleset + ":" + _jobtitle + " MATCH [" + ",".join(_rule)+"]"
                    person_results[category]=value
                    _update_summary(summary,value,_id)
                    break
				
            if match==0:
                #_update_results(person_results,_ruleset,_jobtitle,_rule,category,"UNKNOWN_"+category)
                if DEBUG!=False:
                    print _ruleset + ":" + _jobtitle + " NOMATCH [" + ",".join(_rule)+"]"
                #person_results[category]="UNKNOWN_"+category
                person_results[category]="UNKNOWN"
                _update_summary(summary,value,_id)
            else:
                pass
			
        count = count +1
        results[_id]={"results": person_results, 
            "organization":_person["organization"], 
            "jobtitle" : _jobtitle, 
            "email" : _person["email"], 
            "phone" : _person["phone"], 
            "firstname":_person["firstname"], 
            "lastname":_person["lastname"]}
else:
	import pickle

	with open('summary.pickle', 'rb') as f:
    		summary = pickle.load(f)	
	with open('results.pickle', 'rb') as f:
    		results = pickle.load(f)	

sys.stderr.write(str(count))
print_results(results,clients)
t2 = datetime.datetime.now()
delta = t2-t1
sys.stderr.write("number of tests performed: " + str(numtests) + " in " +str(delta) + "secs\n")

if printstats==True:
	print_stats(results)

if query!=[]:
	print_summary_query(summary,query,outputtype,results,clients)

if mode=="persist":
	import pickle
	with open('summary.pickle', 'wb') as f:
    		pickle.dump(summary, f, pickle.HIGHEST_PROTOCOL)
	with open('results.pickle', 'wb') as f:
    		pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

if echo ==True:
	with open(queryoutputfile,"r+") as f:
		for _line in f:
			for _field in _line.split(","):
				print _field.ljust(26),
