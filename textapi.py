import re
import os

class TextApi:

    def __init__(self):
        pass

    def check_string(self, text):
        pass

    def do_it(self, text):
        pass


class BashApi:

    def __init__(self):
        self.re = re.compile("<BASH\>(.*?)\<\/BASH\>")

    def check_string(self, text):
        res = self.re.search(text)
        return res 
    
    def do_it(self, text):
        commands = self.re.findall(text)

        res = "<BASH_RESULTS>\n";
        if commands:
            for cmd in commands:
                res = res + "<item><cmd>"+cmd+"</cmd><result>\n"
                print("executing :"+cmd)
                stream = os.popen(cmd)
                output = stream.read()

                res = res +  output;
        
                res = res + "</result></item>\n\n"

        res = res + "</BASH_RESULTS>"
        return res


"""
api = BashApi()

str = "<BASH>date</BASH> <BASH>ls</BASH>"

res = api.check_string(str)
if res:
    text=api.do_it(str)

    print(text)




s = "BASH this is my text"

r = re.compile("<BASH\>(.*?)\<\/BASH\>")
res = r.findall("<BASH>abc qwer</BASH> ffff <BASH>qqq</BASH>")
if res:
    for i in res:
        print(i)
"""