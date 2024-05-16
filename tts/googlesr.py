import speech_recognition as sr

def recognize_from_microphone():
    """
    使用麦克风识别语音输入

    Returns:
        str: 识别到的文本，如果识别失败或未识别到文本，则返回空字符串
    """
    # 创建Recognizer对象
    r = sr.Recognizer()

    # 打开麦克风并开始录音
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        # 将录音转化为文字
        text = r.recognize_google(audio, language='zh-CN', show_all=True)

        # 如果识别结果为最终结果，则返回该结果
        if text['final'] == True:
            return text['alternative'][0]['transcript']
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Error: {e}")
        return "network error"

def s2text(filepath):
    """
    将语音文件转换为文字

    Args:
        filepath (str): 待识别的语音文件路径

    Returns:
        str: 识别到的文本
    """
    r = sr.Recognizer()

    # 打开语音文件
    test = sr.AudioFile(filepath)

    with test as source:
        audio = r.record(source)

    # 使用 Google 语音识别将语音转换为文字
    return r.recognize_google(audio, language='zh-CN', show_all=True)
