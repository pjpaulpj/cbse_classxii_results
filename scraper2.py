import requests 
for init in [
#'46', '47', '48', '49', '56', '57', '58', '59',
'66', '67', '68', '69']:
    for i in xrange(5000, 10000):
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
