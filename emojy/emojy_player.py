import cv2
import os
import random
import time
import threading

# 注意：为了保证子线程活动，主线程一定不能结束，可以通过while True苟活！！！

class EmojiPlayer:
    def __init__(self):
        self._play_specific_emoji = False  # 是否播放特定表情
        self._specific_emoji_name = None  # 特定表情名称

        # 读取图片并存储为字典
        self.imgs_dict = self.read_img_dict()

        # 创建一个线程来播放表情
        self.thread = threading.Thread(target=self.play_emoji_continuously)
        self.thread.daemon = True  # 设置为守护线程，以便在主线程退出时自动退出
        self.thread.start()

    @property
    def play_specific_emoji(self):
        return self._play_specific_emoji

    @play_specific_emoji.setter
    def play_specific_emoji(self, value):
        self._play_specific_emoji = value
        if value:
            self.do_emoji(self._specific_emoji_name)
        else:
            self.do_emoji("normal")

    @property
    def specific_emoji_name(self):
        return self._specific_emoji_name

    @specific_emoji_name.setter
    def specific_emoji_name(self, value):
        self._specific_emoji_name = value
        if self.play_specific_emoji:
            self.do_emoji(value)

    def read_img_dict(self):
        """
        读取图片文件夹中的图片，并存储为字典
        """
        root_path = ".\\emojy\\image"
        emoji_states = ["blink", "look_left_top", "look_right_top", "excited", "frightened", "disdain", "anger", "sad", "normal"]
        imgs_dict = dict()

        for emoji_state in emoji_states:
            if emoji_state == "blink":
                paths = [os.path.join(root_path, emoji_state, "single_blink"),
                         os.path.join(root_path, emoji_state, "blink_twice")]
            elif emoji_state == "normal":
                paths = [os.path.join(root_path, emoji_state, "normal")]
            else:
                paths = [os.path.join(root_path, emoji_state, emoji_state + "_1"),
                         os.path.join(root_path, emoji_state, emoji_state + "_2"),
                         os.path.join(root_path, emoji_state, emoji_state + "_3")]

            for path in paths:
                key = os.path.basename(path)  # 使用文件夹名字作为key
                imgs_dict[key] = []

                for i in range(1, 200):
                    img_name = os.path.join(path, "%d.jpg" % (i))
                    if not os.path.exists(img_name):
                        continue

                    img = cv2.imread(img_name)
                    imgs_dict[key].append(img)

        return imgs_dict

    def do_emoji(self, emoji_state):
        """
        播放指定表情
        """
        keys = []
        if emoji_state == "blink":
            keys.append(("single_blink"))
            keys.append(("blink_twice"))
            keys = [random.choice(keys)]  # 随机选择一个
        elif emoji_state == "normal":
            keys.append(("normal"))
        else:
            if emoji_state == "look_left_top" or emoji_state == "look_right_top":
                loop_num = 1
            else:
                loop_num = 4

            keys.append((emoji_state + "_1"))

            for l in range(loop_num):
                keys.append((emoji_state + "_2"))

            keys.append((emoji_state + "_3"))

        cnt = 0
        if emoji_state == "excited":
            div = 15
        else:
            div = 3

        for key in keys:  # 遍历所有key
            imgs = self.imgs_dict[key]
            imgs_num = len(imgs)

            for i in range(imgs_num):
                if cnt % div == 0:  # 为加速播放，跳过动画一部分索引的图像
                    img = imgs[i]
                    cv2.imshow("Emoji", img)
                    cv2.waitKey(50)  # 等待50毫秒

                cnt += 1


    def play_emoji_continuously(self):
        """
        播放表情，根据是否播放特定表情来选择播放特定表情或者默认表情
        """
        while True:
            time.sleep(1)  # 等待1秒后继续播放
            if self.play_specific_emoji:  # 如果需要播放特定表情
                self.do_emoji(self.specific_emoji_name)  # 播放特定表情
                self.play_specific_emoji = False
                time.sleep(1)
            else:
                self.do_emoji("normal")  # 播放默认表情
