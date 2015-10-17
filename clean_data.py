import pandas as pd
import numpy as np
from pattern import web
from os import listdir

print 'reading files'
all_files = sorted(listdir('results_raw_2015'))

def parse_results(fname):
    with open('results_raw_2015/%s'%fname, 'r') as f:
        dom = web.Element(f.read())
    fields = dom('td')
    stud_det = {'roll_num': web.plaintext(fields[8].content),
                'name': web.plaintext(fields[10].content),
                'mother_name': web.plaintext(fields[12].content),
                'father_name': web.plaintext(fields[14].content)}
    for i in range(21,len(fields)-7,6):
        if web.plaintext(fields[i].content) == 'Additional Subject':
            i += 1
        stud_det.update({web.plaintext(fields[i+1].content) + '_theory': web.plaintext(fields[i+2].content),
                            web.plaintext(fields[i+1].content) + '_practical': web.plaintext(fields[i+3].content),
                            web.plaintext(fields[i+1].content) + '_total': web.plaintext(fields[i+4].content),
                            web.plaintext(fields[i+1].content) + '_grade': web.plaintext(fields[i+5].content)})
    stud_det['fin_result'] = web.plaintext(fields[-5].content)[8:]
    return stud_det

print 'processing files'
df = pd.DataFrame([parse_results(fname) for fname in all_files])

print 'finished processing'
subs = list(df.columns)[:-5]
subs = [subs[i] for i in xrange(len(subs)) if i%4 != 0]

df = df[['roll_num', 'name', 'father_name', 'mother_name'] + subs + ['fin_result']]
def f(i):
    if pd.isnull(i):
        return np.nan
    try:
        return int(i)
    except:
        if 'AB' in i:
            return np.nan
        elif i == 'A':
            return np.nan
        elif ' ' in i:
            return int(i.split()[0])
        elif i == '---':
            return np.nan
        elif i == '':
            return np.nan
        else:
            print i
            return i

for sub in subs:
    df[sub] = df[sub].apply(f)

subs_total = subs[2::3]
df['avg_score'] = df[subs_total].mean(axis=1)

def get_top_5(i):
    return i.sort(ascending=False, inplace=False)[:5].mean()

df['top_5_avg'] = df[subs_total].apply(get_top_5, axis=1)

def get_last_name(i):
    if ' ' in i:
        return i.split()[-1]
    return 'None'

def get_first_name(i):
    if ' ' in i:
        return i.split()[0]
    return i

df['last_name'] = df['name'].apply(get_last_name)
df['first_name'] = df['name'].apply(get_first_name)
df['len_last'] = df.last_name.str.len()
df['len_first'] = df.first_name.str.len()

df['roll_num'] = df['roll_num'].astype(int)
df['area_code'] = df['roll_num']/100000
df['area_code'] = df['area_code'].astype(int)

def get_region(code):
    if code in [16,17]: return 'Ajmer'
    elif code in [26,27]: return 'Panchkula'
    elif code in [36]: return 'Guwahati'
    elif code in [46,48]: return 'Chennai/Trivandrum'
    elif code in [56,58,59]: return 'Dehradun/Allahabad'
    elif code in [66]: return 'Calcutta/Cuttack'
    elif code in [76]: return 'Patna'
    elif code in [91,92,96,97]: return 'Delhi'

df['region'] = df['area_code'].apply(get_region)
df.to_csv('results_2015.csv', index=False)
