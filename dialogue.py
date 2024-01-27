# import openai
from textapi import *
from openai import OpenAI


class Dialogue:
    intro_text = ""
    messages = []
    model = "gpt-4"
    max_messages = 10

    print_messages = False
    print_system_messages = False

    apis: list[TextApi]

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)
        #openai.api_key = api_key
        self.apis = [BashApi(), SqlApi()]


    def say(self, text, role = "user"):

        if self.print_messages:
            print("user: "+text+"\n")

        if self.print_system_messages:
            print("<generating responce>\n")

        self.messages.append({"role":role, "content": text})
        msgs = [{"role": "system", "content": self.intro_text}] + \
            self.messages[-self.max_messages:]
        
        res = self.client.chat.completions.create(model=self.model, messages=msgs)
        res_text = res.choices[0].message.content 

        self.messages.append({"role":"assistant", "content": res_text})

        if self.print_messages:
            print("assistant: "+res_text+"\n")

        for api in self.apis:
            if api.check_string(res_text):
                res = api.do_it(res_text)
                return self.say(res, role = "system")

        return res_text

    
    