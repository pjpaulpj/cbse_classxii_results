import requests
for init in ['76', '77', '78', '79', '91', '92', '93', '94', '95', '96', '97', '98']:
    for i in xrange(5000,10000):
        roll_num = int(init)*100000 + i
        r = requests.post("http://cbseresults.nic.in/class12/cbse122015_all.asp", 
                          data={"regno": roll_num},
                          headers= {'Origin': 'http://cbseresults.nic.in',
                                    'Referer': 'http://cbseresults.nic.in/class12/cbse122015_all.htm'})
        is_invalid = "Result Not Found" in r.text
        if is_invalid and i > 0:
            print roll_num
            break
        else:
            if not is_invalid:
                with open('results_raw_2015/'+str(roll_num)+'.html', "w") as f:
                    f.write(r.text.encode('utf-8'))
    print init
