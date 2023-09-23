import re
import os
import sqlite3

class TextApi:

    def __init__(self):
        pass

    def check_string(self, text):
        res = self.re.search(text)
        return res 

    def do_it(self, text):
        pass


class BashApi(TextApi):

    def __init__(self):
        self.re = re.compile("<BASH\>(.*?)\<\/BASH\>", re.DOTALL)
    
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


class SqlApi(TextApi):
    def __init__(self, file_name="sql.db"):
        self.con = sqlite3.connect(file_name)
        self.cur = self.con.cursor()

        self.re = re.compile(r"<SQLITE\>(.*?)\<\/SQLITE\>", re.DOTALL)

    def do_it(self, text):
        commands = self.re.findall(text)
        if commands:
            res = "<SQL_RESULT>"
            for cmd in commands:
                sql_text_res = ""
                try:
                    cur_res = self.cur.execute(cmd)
                    sql_text_res = str(cur_res.fetchall())
                    self.con.commit()
                except Exception as e:
                    sql_text_res = str(e)
                
                res = res + f"<item><sql>{cmd}</sql><result>{sql_text_res}</result></item>"

            res = res + "</SQL_RESULT>"
            return res



"""
class C:
    apis: list[TextApi]

c = C()
c.apis = [SqlApi(),]

s = "<SQLITE>SELECT name FROM sqlite_master WHERE type='table'\n</SQLITE>"

for api in c.apis:
    if api.check_string(s):
        res = api.do_it(s)
        print(res)


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