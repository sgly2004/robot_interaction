import openai
from  common.config import conf

#gpt-3.5-turbo 模型
def gptTur(text): 
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "你叫Sentry，负责回复输入。请返回 你想回复的语句 和 你当前的表情，二者中间用“|||||”隔开，你的表情只能是（blink, look_left_top, look_right_top, excited, frightened, disdain, anger, sad, normal）其中之一，回复请尽量简短"},
            {"role": "user", "content": text}
        ]
    )

    resText = response.choices[0].message.content
    # 使用 "|||||" 作为分隔符将话语和表情分开
    parts = resText.split("|||||")
    return parts[0], parts[1]  # 返回话语和表情

def chatGpt(input_text):
    openai.api_key = conf().get('open_ai_key')
    if len(input_text) == 0:
        return
    input_text = input_text.replace('\n', ' ').replace('\r', '').strip()
    text, emojy = gptTur(input_text)
    return text, emojy

