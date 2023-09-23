import pickle
import os
import sys
from veloxutils import removeunicode,get_now, _get_data_header, process_args

access_code="4rY0P12jmfi0iq41S0mtuDUi4yKEfnLefH260Ufkgnb8fE33xfdt/fb2dsqGeev7"

_args = process_args(sys.argv)
for _arg in _args:
    locals()[_arg] = _args[_arg]


def get_remaining_rate():

    print _get_data_header("https://api.capsulecrm.com/api/v2/site",access_code,"X-RateLimit-Remaining")


def get_new_file(_category,_datestr,file_count,f=None):
    if f!=None:
        f.close()

    fname='prod_data_person_update_'+_category.replace(" ","_")+'_'+_datestr+'_'+str(file_count)+'.csv'
    ffullname=os.path.join(bumblebee_dir,fname)

    print "opening new file " + ffullname
    return open(ffullname,'w+') 

all_categories=["job type","sub department","seniority","department"]
#all_person_pickles=["person_1"]
all_person_pickles=["person_1","person_2","person_3","person_4"]

with open(os.path.join(os.environ["DIRCAPSULEPICKLE"],'summary.pickle'), 'rb') as f:
    summary = pickle.load(f)

with open(os.path.join(os.environ["DIRCAPSULEPICKLE"],'results.pickle'), 'rb') as f:
    results = pickle.load(f)


output ={}
datestr = get_now("%Y%m%d")

bumblebee_dir="."
os.getenv('DIRBCAPSULEUPLOAD')
#bumblebee_dir=os.getenv('DIRBCAPSULEUPLOAD')

max_rows = 3800
file_count=0

categories=all_categories
try:
    if locals()['category']!="all":
        categories = [locals()['category'].lower()]
except:
    pass

for person_pickle in all_person_pickles:
    same_count=0
    diff_count=0
    pickle_fname=person_pickle + '.pickle'
    with open(os.path.join(os.environ["DIRCAPSULEPICKLE"],pickle_fname), 'rb') as f:
        person_1 = pickle.load(f)

    for _person in person_1.keys():
        if results.has_key(str(_person))==True:
            for _field in person_1[_person]['fields']:
                _category = _field['definition']['name']

                if _category.lower() in categories:
                    _old_value = _field['value']
                    _new_value = results[str(_person)]['results'][_category]
                    _jobtitle =  results[str(_person)]['jobtitle']
                    if _old_value.upper() == _new_value.upper() or  _old_value[:6].upper() == _new_value[:6].upper():
                        same_count=same_count+1
                    else:

                        if output.has_key(_category) == False:
                            output[_category]=[]
                        output[_category].append([str(_person),_new_value])
                        diff_count=diff_count+1
        else:
            print "missing" + str(_person)
    print pickle_fname,categories
    print "same : " + str(same_count)
    print "diff : " + str(diff_count)

    if locals()["generate_files"]==True:
        for _category in output.keys():
            row_count=0
            f=None
            for _update in output[_category]:
                if row_count > max_rows or row_count == 0:
                    f = get_new_file(_category,datestr,file_count,f)
                    file_count=file_count+1
                    f.write("id^"+_category+"\n")
                    row_count=0

                f.write("^".join(_update)+"\n")
                row_count=row_count+1

