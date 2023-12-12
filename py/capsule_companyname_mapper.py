import sys
from veloxutils import _get_data,_header,process_args, persist, get_remaining_rate

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]

raw_ample_headers="email^first_name^last_name^title^linkedin^company_name^company_domain^company_email_domain^company_linkedin^country^state^city^location^industry^company_size^email_status^recent_position_change^tenure_at_company^tenure_at_position"

def get_ample_export(amplefile):
    _ample_headers = raw_ample_headers.split("^")
    ampleexport={}
    fh = open(amplefile,"r+")
    for line in fh:
        _ample = {}
        _ample_row=line.split("^")
        for i in range(0,len(_ample_headers)):
            _ample[_ample_headers[i]]=_ample_row[i].lower()

        ampleexport[_ample["linkedin"]] = _ample
    fh.close()
    return ampleexport

def get_num_words(sentence,num_words):
    if num_words==0:
        return sentence
    _sentence=sentence.split(" ")
    return " ".join(_sentence[:num_words])

def get_company_mapping(mappingfile,num_words=0):
    mapping={}
    fh = open(mappingfile,"r+")
    linecount=0
    for line in fh:
        _mapping = line.split("^")
        mapping[get_num_words(_mapping[0].lower(),num_words)]=_mapping[1].strip().lower()
    fh.close()
    return mapping

def match_companyname(mapping,companyname,num_words=0):
    _match=get_num_words(companyname,num_words)
    if mapping.has_key(_match)==True:
        _matchedto=mapping[_match]
        return True,_matchedto
    return False,""

def _store(d,_company_name,_liurl,_matchtype):
    _value = _liurl + "_" + _matchtype
    if d.has_key(_company_name)==False:
        d[_company_name] = [_value]
    else:
        d[_company_name].append(_value)

def _storeexportdict(d,_matchflag,_company_name,_record):
    if _matchflag==True:
        key="^".join([_record["first_name"],_record["last_name"],_company_name])
        d["matched"][key]=_record
    else:
        key="^".join([_record["first_name"],_record["last_name"],_record["company_name"]])
        d["unmatched"][key]=_record

ampleexport = get_ample_export("/home/burtnolej/sambashare/veloxmon/capsulecrm/csv/ample_export.csv")

stats = {"index":{},"runs":{"0":0,"1":0,"2":0,"3":0}}

matchtype=[0,3,2,1]
exportdict={"matched":{},"unmatched":{}}

unmatched={}
matched={}
for i in range(0,len(matchtype)):
    _matchtype=str(matchtype[i])
    mapping = get_company_mapping("/home/burtnolej/sambashare/veloxmon/capsulecrm/csv/company_name_mapper.csv",int(_matchtype))

    testcount=0
    matchcount=0
    for _amplekey in ampleexport.keys():
        _company_name=ampleexport[_amplekey]["company_name"]
        _liurl=_amplekey
        if stats["index"].has_key(_liurl) == False:
            stats["index"][_liurl]={"matched":False}
        elif stats["index"][_liurl]["matched"]==True:
            continue

        _matchresult,_matchedto = match_companyname(mapping,_company_name,int(_matchtype))
        if _matchresult == True:
            stats["index"][_liurl][_matchtype]=True
            stats["index"][_liurl]["matched"]=True
            if unmatched.has_key(_company_name)==True:
                unmatched.pop(_company_name)

            _store(matched,_matchedto,_liurl,_matchtype)
            _storeexportdict(exportdict,_matchresult,_matchedto,ampleexport[_amplekey])
            matchcount=matchcount+1
        else:
            stats["index"][_liurl][_matchtype]=False
            _store(unmatched,_company_name,_liurl,_matchtype)
            _storeexportdict(exportdict,_matchresult,_company_name,ampleexport[_amplekey])

        testcount=testcount+1
    stats["runs"][_matchtype] = (testcount,matchcount)

fh =open(outputfile,"w+")
fh.write("^".join(["^".join([str((key,value)) for key,value in stats["runs"].iteritems()]),str(len(unmatched.keys())),str(len(matched.keys()))])+"\n")

for _key in matched.keys():
    fh.write("^".join([_key]+[str((ampleexport[_match[:-2]]["company_name"],int(_match[-1:]))) for _match in matched[_key]])+"\n")

for _key in unmatched.keys():
    fh.write("^".join([_key] + [_liurl for _liurl in unmatched[_key]])+"\n")
fh.close()

persist(exportdict,persistfile,index=False,pickledir=dircapsulepickle)
