import os, glob
from wakeup import picovoice
from tts import googlesr
from tts import azuretts as azuretts
from chatbot import chatgpt
from playsound import playsound
import speech_recognition as sr
from common import config
from common.log import logger
import pyttsx3
import time
from emojy.emojy_player import EmojiPlayer
import tempfile

######################################## 文本转语音 start ###################################################
engine = pyttsx3.init()  # 实例化 语音 合成 器

def speak(audio):
    engine.say(audio)  # 将需要语音合成的文本传递给引擎
    engine.runAndWait()  # 播放语音
######################################## 文本转语音 end ###################################################

######################################## 语音识别 start ###################################################
# 输入：无（待调用后，开始语音识别）
# 输出：识别得到的文本。

recognizer = sr.Recognizer()  # 实例化语音 识别 器

def takecommand():
    global recognizer
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("请说话...")
        recognizer.pause_threshold = 1  # 静态能量阈值
        recognizer.dynamic_energy_adjustment_damping = 0.15 # 调整阈值的平滑因子
        recognizer.dynamic_energy_ratio = 1.5  # 阈值调整比率
        recognizer.operation_timeout = 5  # 最长等待时间（秒）
        recognizer.energy_threshold = 4000      # 设置音量阈值
        recognizer.dynamic_energy_threshold = True  # 自动调整音量阈值
        # recognizer.default = model
        audio = recognizer.listen(source, phrase_time_limit=5)
        # 将录制的音频保存为临时文件
        with tempfile.NamedTemporaryFile(delete=False) as f:
            audio_file_path = f.name + ".wav"
            f.write(audio.get_wav_data())
    # return audio_file_path 
        try:
            print("Recognizing...")  # 识别中...
            query = recognizer.recognize_sphinx(audio, language='zh-CN')
            print('User: ' + query + '\n')
            return query     
        except Exception as e:
            print("对不起，我没有听清楚，请再说一遍。")
            speak("对不起，我没有听清楚，请再说一遍。")
            query = None
            return query
        except sr.RequestError as error:
            print(f"语音识别请求出错：{error}")
            speak(f"语音识别请求出错：{error}")
            return ""
######################################## 语音识别 end ###################################################

########################################## 主逻辑 start ###########################################
# 当机器人被唤醒后，执行以下逻辑

def run(player):  

    # ################################ 获取用户输入 start #####################################
    logger.info("收到唤醒指令")  # 记录收到唤醒指令的信息
    playsound('mp3\\wait.mp3')  # 播放等待音频

    # 使用 Google 语音识别从麦克风中识别语音
    q = takecommand()

    if len(q) == 0:  # 如果识别到的语音为空
        logger.warn("语言识别失败！")  # 记录语言识别失败的警告
        playsound('mp3\\sorry.wav')  # 播放抱歉音频
        return
    elif q == 'network error':  # 如果出现网络错误
        logger.warn("google连接失败！")  # 记录 Google 连接失败的警告
        playsound('mp3\\neterr.wav')  # 播放网络错误音频
        return
    else:  
        logger.info("你: {}".format(q))  # 记录用户的输入
        last_recv_time = time.time()
    # ################################ 获取用户输入 end #####################################

    # ################################ 获取GPT输出 start #####################################
    text, emojy = chatgpt.chatGpt(q)  # 使用 ChatGPT 进行对话生成
    logger.info("GPT: {}".format(text))  # 记录 ChatGPT 的生成结果

    for file in glob.glob("tmp/*"):  # 清理临时文件
        os.remove(file)
    # ################################ 获取GPT输出 start #####################################
    
    # ################################ 输出语音 start #####################################
    # 使用 TTS 将 ChatGPT 的生成结果转换为语音
    logger.info("GPT语音")
    speak(text)  # 播放 ChatGPT 生成的语音
    # ################################ 输出语音 end #####################################

    # ################################ 输出表情 start #####################################
    player.specific_emoji_name = emojy
    player.play_specific_emoji = True
    # ################################ 输出表情 end #####################################

    # 如果距离上一次收到输入时间太长，认为结束输入
    if time.time() - last_recv_time > 60:
        return True
    else:
        return False
    
########################################## 主逻辑 end ###########################################

def main():
    # 等待唤醒 + 语音转文字 + 调用LLM生成回复 + 拆分出指令、表情、语言 + 执行程序、文字转语音、表情转表情
    config.load_config()
    os.environ["http_proxy"] =  config.conf().get('proxy')
    os.environ["https_proxy"] =  os.environ["http_proxy"]
    player = EmojiPlayer()
    print("程序已启动")
    while True:
        picovoice.picovoice(run, player)
    
if __name__ == "__main__":
    main()