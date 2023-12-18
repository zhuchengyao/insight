import edge_tts
import asyncio

async def voice_gen(Text = '你好',
                      voice = 'zh-CN-XiaoxiaoNeural',
                      output = '/Users/zhuchengyao/PycharmProjects/SalesTrainer/response.mp3',
                      rate = '+4%',
                      volume = '+0%'):

    tts=edge_tts.Communicate(text=Text, voice=voice, rate=rate, volume=volume)
    await tts.save(output)