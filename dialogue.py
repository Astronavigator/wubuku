import openai

class Dialogue:
    intro_text = ""
    messages = []
    model = "gpt-3.5-turbo"
    max_messages = 10

    print_messages = False
    print_system_messages = False

    def __init__(self, api_key):
        openai.api_key = api_key


    def say(self, text, role = "user"):

        if self.print_messages:
            print("user: "+text+"\n")

        if self.print_system_messages:
            print("<generating responce>\n")

        self.messages.append({"role":role, "content": text})
        msgs = [{"role": "system", "content": self.intro_text}] + \
            self.messages[-self.max_messages:]
        
        res =  openai.ChatCompletion.create(model=self.model, messages=msgs)
        res_text = res.choices[0].message.content 

        self.messages.append({"role":"assistant", "content": res_text})

        if self.print_messages:
            print("assistant: "+res_text+"\n")

        return res_text

    
    