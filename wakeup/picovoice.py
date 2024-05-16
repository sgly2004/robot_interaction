import pvporcupine
import pyaudio
import struct
import wave
from  common.config import conf
import sys
from common.log import logger

def picovoice(f, player):
    
    # 输入：唤醒后需要被调用的函数
    # 输出：调用这个函数（条件是听到唤醒词）
    logger.info("等待唤醒指令")
    # 使用 pvporcupine 模块创建一个 Porcupine 实例，用于监听声音并检测指定的唤醒词。
    porcupine = pvporcupine.create(
        access_key= conf().get('picovoice_access_key'),
        keyword_paths= [conf().get('picovoice_ppn')]
    )
    
    # 通过 pyaudio 模块创建音频流，用于从声卡读取音频数据。
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)
    while True:
        try:
            # 从音频流中读取指定长度的音频数据.
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            _pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            # 使用 Porcupine 实例处理音频数据，返回检测到的唤醒词的索引。
            keyword_index = porcupine.process(_pcm)
            # 如果检测到了唤醒词，则执行指定的函数 f()。
            if keyword_index >= 0:
                #play_wav('mp3\\wait.wav')
                is_exit = f(player)
                if is_exit is True:
                     sys.exit()
        except KeyboardInterrupt:
                print("\nbye...")
                sys.exit()

def play_wav(filepath):

    # 输入：音频文件路径
    # 输出：播放音频文件

    # 打开wav文件并读取数据                                                                                             │
    with wave.open(filepath, "rb") as audio_file:
        audio_data = audio_file.readframes(-1)
        # 初始化音频流                                                                                                      │
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(audio_file.getsampwidth()),
        channels=audio_file.getnchannels(), 
        rate=audio_file.getframerate(),output=True)
        # 播放音频数据                                                                                                      │
        stream.write(audio_data)
        # 关闭流和PyAudio                                                                                                   │
        stream.stop_stream()
        stream.close()
        p.terminate()