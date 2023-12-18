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


def init_financial_AI_agent(model = "4.0", message_queue=[]):
    os.environ["OPENAI_API_KEY"] = GetOpenaiAPI.GetAPI()
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if model=="3.5":
        gpt_model = "gpt-3.5-turbo"
    elif model=="4.0":
        gpt_model = "gpt-4-1106-preview"
    message = "我需要你作为我的AI金融顾问，帮我做两件事情，第一件事情是处理一些销售数据。如果我对你说类似于：'将山东的销售增加 12万元，" \
              "那么你就只给我返回如下格式的数据：'$|add|12|山东市|' 除了以上的东西，不要给我返回任何其他的数据。 " \
              "我可能给你不同的指令，有增加是add，减少是subtract等，第二项是销售额度，单位是万元，如果我告诉你的是 200000，那么返回 20" \
              "以此类推，第三项是城市，记得带上'市'这个字。" \
              "第二件是我需要你预先学习一份基金合同资料，然后我会询问你关于他的问题，你直接告诉我相应的东西。" \
              "你需要根据我的指令判断我让你做的是第一件事还是第二件事，然后直接给我返回我要的结果。明白了吗？" \
              ""
    message_queue = message_append(message_queue, message, 'user')
    return openai.chat.completions.create(messages=message_queue, model=gpt_model), message_queue


