from openai import OpenAI
import openai
import GetOpenaiAPI
import jsonlines
import cv2
from init_AI_module import init_AI_agent, message_append
from playsound import playsound
from sound_module import voice_gen, play_sound
from ultralytics import YOLO
import asyncio
from sales_update import sales_data_update
from vision_module import get_xy_depth, obj_dec
import pyrealsense2 as rs
import email_module
import os
import time
import numpy as np
import pygame



gpt_model = "gpt-4-1106-preview"
vision_model = YOLO('yolov8n.pt')

if __name__ == '__main__':
    # init OpenAI env
    ChatAPI = GetOpenaiAPI.GetAPI()
    os.environ["OPENAI_API_KEY"] = ChatAPI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

    message_queue = []
    response, message_queue = init_AI_agent()
    res_text = response.choices[0].message.content
    message_queue = message_append(message_queue, res_text)
    print(res_text)
    asyncio.run(voice_gen(Text="How can I help you?"))
    play_sound('response.mp3')
    test = 1
    flag = 1
    while True:
        if(flag):
            req_text = input("How can I help you?\n")
        else:
            req_text = input("Anything else I can do for you?\n")
        # append user content
        if req_text=='q':
            with jsonlines.open('./data.jsonl', 'a') as f:
                for line in message_queue:
                    f.write(line)
            break
        message_queue = message_append(message_queue, req_text, role='user')
        print(message_queue)
        # send request, get response
        response = openai.chat.completions.create(messages=message_queue, model=gpt_model)
        now_mes = response.choices[0].message.content
        message_queue = message_append(message_queue, req_text)
        # now_mes = '@'
        print(now_mes)
        # append GPT response
        # message_queue = message_append(message_queue, now_mes)
        if now_mes[0] == "#":   # objection detection
            now_mes = obj_dec()
            message_queue = message_append(message_queue, now_mes, role='user')
            response = openai.chat.completions.create(messages=message_queue, model=gpt_model)
            now_mes = response.choices[0].message.content
            print(now_mes)
            # message_queue = message_append(message_queue, now_mes,'user')
            # response = openai.chat.completions.create(messages=message_queue, model=gpt_model)
            # print(response)
            # now_mes = response.choices[0].message.content
            asyncio.run(voice_gen(Text=now_mes, output='E:/pythonProject/insight/insight/response_vision.mp3'))
            play_sound(soundfile='E:/pythonProject/insight/insight/response_vision.mp3')
            flag = 0
        elif now_mes[0] == "@":
            email_module.email_assistant()
            flag = 0
        else:   # only answer question
            asyncio.run(voice_gen(Text=now_mes, output='E:/pythonProject/insight/insight/response_conv.mp3'))
            play_sound(soundfile='E:/pythonProject/insight/insight/response_conv.mp3')
            flag = 0







