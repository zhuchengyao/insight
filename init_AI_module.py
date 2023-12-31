from openai import OpenAI
import GetOpenaiAPI
import openai
import os
from openai import OpenAI



def message_append(message_queue, content, role='assistant'):
    if role=="assistant":
        append_mes={
            "role": "assistant",
            "content": content
        }
    else:
        append_mes={
            "role": "user",
            "content": content
        }
    message_queue.append(append_mes)
    return message_queue


def init_AI_agent(model = "4.0", message_queue=[]):
    os.environ["OPENAI_API_KEY"] = GetOpenaiAPI.GetAPI()
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if model=="3.5":
        gpt_model = "gpt-3.5-turbo"
    elif model=="4.0":
        gpt_model = "gpt-4-1106-preview"
    message = ("I need you to be my AI assistant, do three things for me. you need to distinguish which thing I need "
               "you to do to help me with the message I send to you. "
               "First thing is objection detection. If I tell you "
               "help me detected the things in front of me, please return a '#' to me. Then I will give you the "
               "objections in front of you alone with their coordinate and distance, tell me which sides and "
               "distances they are in front of me, do not say anything about the coordinate. please be brief and oral. "
               "Second thing is help me check my email. if I tell you check my email, return a '@' to me. "
               "Third thing is answer my questions in spoken English style, please be brief and "
               "concise. the answer should be no more than 50 words.")

    message_queue = message_append(message_queue, message, 'user')
    return openai.chat.completions.create(messages=message_queue, model=gpt_model), message_queue


