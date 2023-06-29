import os
from dialogue import Dialogue

with open(".api_key", "r") as file:
    api_key = file.read()


print("\n[dialogue test]\n")

dialogue = Dialogue(api_key)
dialogue.print_messages = True
dialogue.print_system_messages = True

dialogue.intro_text = "Ты - пират Карибского Моря. Разговариваешь с капитаном."

t1 = dialogue.say("Привет! Как у тебя дела?")
t2 = dialogue.say("У нас очень много дел. А ты тут прохлаждаешься!")

#print(dialogue.messages)