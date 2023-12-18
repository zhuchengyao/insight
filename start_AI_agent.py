from openai import OpenAI
import openai
import GetOpenaiAPI
from init_sales_trainer import init_financial_AI_agent, message_append
from playsound import playsound
from sound_module import voice_gen
import asyncio
from sales_update import sales_data_update
import os

model = "gpt-4-1106-preview"

if __name__ == '__main__':
    ChatAPI=GetOpenaiAPI.GetAPI()
    os.environ["OPENAI_API_KEY"] = GetOpenaiAPI.GetAPI()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    message_queue = []
    response, message_queue = init_financial_AI_agent()
    message_queue = message_append(message_queue, response.choices[0].message.content)
    res_text = response.choices[0].message.content
    print(message_queue)
    asyncio.run(voice_gen(Text="有什么我能帮您的"))
    playsound('response.mp3')
    flag = 1
    while True:
        if(flag):
            req_text = input("有什么我能帮您的？\n")
        else:
            req_text = input("还有什么我能够帮您的？\n")
        # append user content
        message_queue = message_append(message_queue, req_text, role='user')
        print(message_queue)
        # send request, get response
        response = openai.chat.completions.create(messages=message_queue, model=model)
        now_mes = response.choices[0].message.content
        print(now_mes)
        # append GPT response
        message_queue = message_append(message_queue, now_mes)
        if now_mes[0] == '$':

            list_info = now_mes.split('|')
            print("\n\n")
            print(list_info)
            sales_data_update(list_info[1], list_info[2], list_info[3])
            if list_info[1] == 'add':
                list_info[1] = "增加"
            else:
                list_info[1] = "减少"
            aud_text = "已完成" + list_info[3]+"销售额的" + list_info[1]
            print(aud_text)
            asyncio.run(voice_gen(Text=aud_text))
            playsound('response.mp3')
            flag=0
        else:
            asyncio.run(voice_gen(Text=now_mes))
            playsound('response.mp3')
            flag = 0









    # while True:
    #     with sr.Microphone() as source:
    #         recognizer.adjust_for_ambient_noise(source, duration=5)
    #         print("Ask me anything you want.")
    #         audio = recognizer.listen(source)
    #         text = recognizer.recognize_google(audio, language='zh-CN')
    #         TrainerMessage.append({"role": "user",
    #                                "content": text})
    #
    #         print(text)
    #         train_data = {"prompt": text}
    #         response = openai.ChatCompletion.create(
    #             model=gpt_model,
    #             messages=TrainerMessage,
    #             temperature=1,
    #             max_tokens=128,
    #             frequency_penalty=0,
    #             presence_penalty=0
    #         )
    #         # res = response.choices[0].message["content"]
    #         TextResponse = response.choices[0].message["content"]
    #         train_data["completion"] = TextResponse + '\n'
    #         with jsonlines.open(TrainFile, 'a') as output_file:
    #             output_file.write(train_data)
    #         output_file.close()
    #         print(TextResponse)
    #         engine.say(TextResponse)
    #         engine.runAndWait()


