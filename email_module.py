import time
import GetOpenaiAPI

import os
import openai
from openai import OpenAI
import imaplib
import email
import smtplib
import ssl
from email.message import EmailMessage
from sound_module import play_sound,voice_gen
import asyncio

Email_Address = '23262010051@m.fudan.edu.cn'
Password = GetOpenaiAPI.Get_Email_API()


def message_append(message_queue, content, role="assistant"):
    if role == "assistant":
        append_mes = {
            "role": "assistant",
            "content": content
        }
    else:
        append_mes = {
            "role": "user",
            "content": content
        }
    message_queue.append(append_mes)
    return message_queue


def send_email(to_whom, content, sender=Email_Address, password=Password):
    with smtplib.SMTP_SSL(host='smtp.exmail.qq.com', port=465) as server:
        server.login(Email_Address, password)
        server.ehlo()
        msg = EmailMessage()
        msg['Subject'] = 'Yao reply'
        msg['From'] = sender
        msg['To'] = to_whom
        msg.set_content(content)
        server.send_message(msg)


def read_unseen_email(Email_Address=Email_Address, Password=Password):
    server = imaplib.IMAP4_SSL(host='imap.exmail.qq.com', port=993)
    server.login(Email_Address, Password)
    server.select("Inbox")
    typ, data = server.search(None, "UNSEEN")  # 这个步骤获得没有阅读过的邮件
    # 标记为已读
    num_store = data[0].split()
    if not num_store:
        return 0
    else:
        server.store(num_store[0], '+FLAGS', '\\Seen')
    # 解码
    decode_num = data[0].decode('utf-8')
    unsee_title = decode_num.split()
    num_unsee = len(unsee_title)
    if(num_unsee==0):
        return 0
    fetch_data_lst = []

    for num in data[0].split():  # data[0].split()选择没有阅读过的邮件的ID,放入num
        typ, fetch_data = server.fetch(num, 'RFC822')
        fetch_data_lst.append(fetch_data)
        msg = email.message_from_bytes(fetch_data_lst[0][0][1])

    msg_list = []
    to_GPT_Message = ''
    for i in range(num_unsee):
        msg = email.message_from_bytes(fetch_data_lst[i][0][1])
        msg_list.append(msg)
        print(msg['from'])

    for msg in msg_list:
        content = 'from: ' + msg['from'] + '. \n' + 'message: '

        for part in msg.walk():
            a = part.get_content_maintype()
            if part.get_content_maintype() == 'text':
                body = part.get_payload(decode=True)
                text = body.decode('utf8')

                content = content + text + '\n'
            else:
                context = content + 'no message' +'\n'
            to_GPT_Message = to_GPT_Message + content
    return to_GPT_Message

# 发件人邮箱账号
def email_assistant():
    # user登录邮箱的用户名，password登录邮箱的密码（授权码，即客户端密码，非网页版登录密码），但用腾讯邮箱的登录密码也能登录成功
    server = imaplib.IMAP4_SSL(host='imap.exmail.qq.com', port=993)
    server.login(Email_Address, Password)
    smtp = smtplib.SMTP_SSL(host='smtp.exmail.qq.com', port=465)
    smtp.login(Email_Address, Password)

    ChatAPI= GetOpenaiAPI.GetAPI()

    gpt_model="gpt-3.5-turbo"
    # client = OpenAI(
    #     # This is the default and can be omitted
    #     api_key=os.environ.get(ChatAPI),
    # )

    message = ("hello, You are going to be my email assistant. I will give my unread email in format of :"
               "'from:  content:' help me generate important information and tell me. After you give me the information about these emails, I will tell you if I want you to help me reply a email, "
               "If I want you to reply the email for me, please format the output like this: '$|target_email_address|content'. I will tell you who you gonna reply and "
               "the content. For example, if pchiang@fudan.edu.cn send me an email and I send you message like 'tell him 'I will be there', or reply to him 'I will be "
               "there, then you give me '$|pichiang@fudan.edu.cn|I will be there'. otherwise, I don't want to reply it, just say 'pass' to me." )
    message_queue = []
    message_queue = message_append(message_queue, message, "user")

    num_detected_objs = 0


    response = openai.chat.completions.create(
        messages=message_queue,
        model=gpt_model,
    )
    message_queue = message_append(message_queue, response.choices[0].message.content)
    now_mes = response.choices[0].message.content
    print(now_mes)
    step = 1
    while step:
        unread_message = read_unseen_email()
        while unread_message == 0:
            time.sleep(2)
            unread_message = read_unseen_email()
            step -= 1
            if step==0:
                asyncio.run(voice_gen(Text="You don't have any new email at this moment", output='E:/pythonProject/insight/insight/response_email.mp3'))
                play_sound(soundfile='E:/pythonProject/insight/insight/response_email.mp3')
                return
        # now_mes = "$|czhu@aum.edu|I will be there"
        message_queue = message_append(message_queue, unread_message, "user")
        response = openai.chat.completions.create(
            messages=message_queue,
            model=gpt_model,
        )
        now_mes = response.choices[0].message.content
        asyncio.run(voice_gen(Text=now_mes,
                              output='E:/pythonProject/insight/insight/response_email.mp3'))
        play_sound(soundfile='E:/pythonProject/insight/insight/response_email.mp3')
        print(now_mes)
        content_mes = input()
        message_queue = message_append(message_queue, content_mes, "user")
        response = openai.chat.completions.create(
            messages=message_queue,
            model=gpt_model,
        )
        now_mes = response.choices[0].message.content

        print(now_mes)
        if (now_mes[0] == '$'):
            list_info = now_mes.split('|')
            print(list_info)
            sending_content = f"Subject: AI assistant reply\n\n{list_info[2]}"
            send_email(list_info[1], list_info[2], Email_Address, Password)
            asyncio.run(voice_gen(Text="I have replied the email for you. You don't have any new email at this moment.",
                                  output='E:/pythonProject/insight/insight/response_email_2.mp3'))
            play_sound(soundfile='E:/pythonProject/insight/insight/response_email_2.mp3')
            break
        else:
            pass









