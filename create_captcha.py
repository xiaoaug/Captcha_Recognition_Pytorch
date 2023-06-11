from captcha.image import ImageCaptcha  # pip install captcha
from PIL import Image
import random
import os
from tqdm import tqdm

import setting  # 相关设置项

# 生成图片的数量
"""
温馨提示：如果是在自己电脑上生成图片，建议数字设置小一些，服务器就无所谓了。
生成 60,000 张图片需要八分钟。80,000 张图片占存储空间约 900M。
"""
TRAIN_COUNT = 80000  # 训练集图片数量
TEST_COUNT = 3000    # 测试集图片数量
PREDICT_COUNT = 10   # 预测集图片数量
ALL_COUNT = [TRAIN_COUNT, TEST_COUNT, PREDICT_COUNT]


def create_random_char() -> str:
    """
    随机生成一组验证码数组
    :return: 生成的验证码数组
    """
    captcha_text = []
    for _ in range(setting.CAPTCHA_NUM_LEN):
        i = random.choice(setting.ALL_CHAR)  # 随机选择一个字符或数字
        captcha_text.append(i)
    return ''.join(captcha_text)


def create_captcha() -> None:
    """
    生成验证码图片
    :return: None
    """
    # 生成图片的路径
    train_path = setting.TRAIN_DATASETS_PATH
    test_path = setting.TEST_DATASETS_PATH
    pre_path = setting.PREDICT_DATASETS_PATH
    all_path = [train_path, test_path, pre_path]

    # 如果没有文件夹，则生成文件夹
    for path in all_path:
        if not os.path.exists(path=path):
            os.makedirs(path)

    for count, path in zip(ALL_COUNT, all_path):
        for i in tqdm(range(count)):
            captcha = ImageCaptcha(width=setting.IMAGE_WIDTH, height=setting.IMAGE_HEIGHT)  # 验证码图像生成函数
            captcha_char = create_random_char()
            captcha_image = Image.open(captcha.generate(captcha_char))
            filename = f'{i}.{captcha_char}.png'
            captcha_image.save(os.path.join(path, filename))


if __name__ == '__main__':
    create_captcha()
