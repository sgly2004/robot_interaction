# 简介

具有表情和对话功能的机器人交互程序。

# 设计思路

等待唤醒 + 语音转文字 + 调用LLM生成回复 + 拆分出指令、表情、语言 + 执行程序、文字转语音、表情转表情

其中拆分出指令和执行程序已经实现，但并未投入使用。

# 快速开始

## 准备

### 1. OpenAI账号注册

前往 [OpenAI注册页面](https://beta.openai.com/signup) 创建账号，参考这篇 [教程](https://www.pythonthree.com/register-openai-chatgpt/) 可以通过虚拟手机号来接收验证码。创建完账号则前往 [API管理页面](https://beta.openai.com/account/api-keys)创建一个 API Key 并保存。

### 2.Picovoice账号注册

前往[Picovoice注册页面](https://console.picovoice.ai/) 创建账号，生成AccessKey并保存。如果需要训练自己的唤醒词在这个页面[唤醒词训练页面](https://console.picovoice.ai/ppn)，选择“English”，输入唤醒次训练导出。

### 3.运行环境

Python版本在 3.7.1以上。

按requirement.txt安装依赖库。

```
pip install -r requirement.txt
```


## 配置

配置文件的模板在根目录的`config.template.json`中，需复制该模板创建最终生效的 `config.json` 文件：

```bash
  cp config.template.json config.json
```

然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改：

```bash
# config.json文件内容示例
{ 
  "open_ai_key": "YOUR API KEY", # 填入OpenAI创建的 OpenAI API KEY
  "picovoice_access_key": "",  # 填入picovoice创建的AccessKey
  "picovoice_ppn": ".\\model\\",  # 唤醒词模型路径
  "proxy": "http://127.0.0.1:7890", # 代理客户端的ip和端口
}
```

## 运行

```bash
  python main.py
```

# 文件结构

│  config.template.json 配置文件的模板
│  main.py 含有语音转文字和文字转语音模块，并综合调用所有模块实现交互
│
├─chatbot
│  │  chatgpt.py  调用GPT获得回复，并从回复中拆分出“对话”、“指令”和“表情”
│
├─common
│  │  config.py  获取配置文件
│  │  log.py  生成日志
│
├─emojy
│  │  emojy_player.py 获取所有表情图片，并展示表情动画
│  ├─image 表情图片集合
│  │  ├─anger
│  │  │  ├─anger_1
│  │  │  ├─anger_2
│  │  │  └─anger_3
│  │  ├─blink
│  │  │  ├─blink_twice
│  │  │  └─single_blink
│  │  ├─disdain
│  │  │  ├─disdain_1
│  │  │  ├─disdain_2
│  │  │  └─disdain_3
│  │  ├─excited
│  │  │  ├─excited_1
│  │  │  ├─excited_2
│  │  │  └─excited_3
│  │  ├─look_left_top
│  │  │  ├─look_left_top_1
│  │  │  ├─look_left_top_2
│  │  │  └─look_left_top_3
│  │  ├─look_right_top
│  │  │  ├─look_right_top_1
│  │  │  ├─look_right_top_2
│  │  │  └─look_right_top_3
│  │  ├─normal
│  │  │  └─normal
│  │  ├─sad
│  │  │  ├─sad_1
│  │  │  ├─sad_2
│  │  │  └─sad_3
│
├─model 唤醒词集合（命名为“唤醒词_ 语言_ 系统”）
│      Sentry_en_linux_v3_0_0.ppn 
│      sentry_en_windows_v3_0_0.ppn
│
├─mp3 录音集合
│      neterr.mp3
│      sorry.wav
│      wait.mp3
│      wait.wav
│
├─tts 语音转文字、文字转语音（由于需要联网，因此并未使用）
│  │  azuretts.py
│  │  googlesr.py
│  │  SSML.xml
│
└─wakeup
    │  picovoice.py  语音模块唤醒

# 参考资料

https://gitee.com/cv-robot/newbot

https://github.com/PAYDAY3/Butler.git

https://github.com/kuangsqc/voice_robot.git
