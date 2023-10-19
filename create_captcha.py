from captcha.image import ImageCaptcha  # pip install captcha
import string
from PIL import Image
import random
import os
from tqdm import tqdm

# setting
ALL_CHAR = string.digits + string.ascii_lowercase  # 获取所有小写字母和数字
ALL_CHAR_LEN = len(ALL_CHAR)  # 36
CAPTCHA_NUM_LEN = 4  # 每张验证码图片所包含的字符数量
IMAGE_HEIGHT = 100  # 图像高度
IMAGE_WIDTH = 180  # 图像宽度
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)  # 图像尺寸大小
TRAIN_DATASETS_PATH = os.path.join(os.getcwd(), "datasets/train_set")  # 用来训练的图片路径
TEST_DATASETS_PATH = os.path.join(os.getcwd(), "datasets/test_set")  # 用来测试的图片路径
PREDICT_DATASETS_PATH = os.path.join(os.getcwd(), "datasets/pred_set")  # 用来预测的图片路径

""" 生成图片的数量
温馨提示：如果是在自己电脑上生成图片，建议数字设置小一些，服务器就无所谓了。
生成 60,000 张图片需要八分钟。80,000 张图片占存储空间约 900M。
"""
TRAIN_COUNT = 80000  # 训练集图片数量
TEST_COUNT = 3000  # 测试集图片数量
PREDICT_COUNT = 10  # 预测集图片数量
ALL_COUNT = [TRAIN_COUNT, TEST_COUNT, PREDICT_COUNT]


def create_random_char() -> str:
    """
    随机生成一组验证码数组
    :return: 生成的验证码数组
    """
    captcha_text = []
    for _ in range(CAPTCHA_NUM_LEN):
        i = random.choice(ALL_CHAR)  # 随机选择一个字符或数字
        captcha_text.append(i)
    return "".join(captcha_text)


def create_captcha() -> None:
    """
    生成验证码图片
    :return: None
    """
    # 生成图片的路径
    train_path = TRAIN_DATASETS_PATH
    test_path = TEST_DATASETS_PATH
    pre_path = PREDICT_DATASETS_PATH
    all_path = [train_path, test_path, pre_path]

    # 如果没有文件夹，则生成文件夹
    for path in all_path:
        if not os.path.exists(path=path):
            os.makedirs(path)

    for count, path in zip(ALL_COUNT, all_path):
        for i in tqdm(range(count)):
            captcha = ImageCaptcha(width=IMAGE_WIDTH, height=IMAGE_HEIGHT)  # 验证码图像生成函数
            captcha_char = create_random_char()
            captcha_image = Image.open(captcha.generate(captcha_char))
            filename = f"{i}.{captcha_char}.png"
            captcha_image.save(os.path.join(path, filename))


if __name__ == "__main__":
    create_captcha()
