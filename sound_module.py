import edge_tts
import asyncio
import pygame
from playsound import playsound


async def voice_gen(Text = 'hello',
                      voice = 'en-US-JennyNeural',
                      output = 'E:/pythonProject/insight/insight/response.mp3',
                      rate = '+4%',
                      volume = '+0%'):

    tts=edge_tts.Communicate(text=Text, voice=voice, rate=rate, volume=volume)
    await tts.save(output)

def non():
    pass

def play_sound(soundfile="E:/pythonProject/insight/insight/response.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

# if __name__=="__main__":
#     asyncio.run(voice_gen(Text="hello world. this is Yao."))
#     playsound('response.mp3')