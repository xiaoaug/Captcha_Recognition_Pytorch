import string
import os

ALL_CHAR = string.digits + string.ascii_lowercase  # 获取所有小写字母和数字
ALL_CHAR_LEN = len(ALL_CHAR)  # 36
CAPTCHA_NUM_LEN = 4  # 每张验证码图片所包含的字符数量

# 图像大小
IMAGE_HEIGHT = 100
IMAGE_WIDTH = 180
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)

BATCH_SIZE = 64         # 一次训练的样本量
NUM_WORKERS = 2         # 有多少子进程将用于数据的加载，若使用 Windows 建议设置为 0
NUM_EPOCHS = 8          # 训练轮数
LEARNING_RATE = 1e-3    # 训练学习率

TRAIN_DATASETS_PATH = os.path.join(os.getcwd(), 'datasets/train_set')   # 用来训练的图片路径
TEST_DATASETS_PATH = os.path.join(os.getcwd(), 'datasets/test_set')     # 用来测试的图片路径
PREDICT_DATASETS_PATH = os.path.join(os.getcwd(), 'datasets/pred_set')  # 用来预测的图片路径
PTH_PATH = os.getcwd()  # 训练完成后的模型保存位置
CONTINUE_TRAIN = False  # 是否使用以前的 pth 文件继续训练？
PTH_FILE = f'{PTH_PATH}/checkpoint_85.4293%.pth'  # 调用之前生成好的 pth 文件并继续训练


if __name__ == '__main__':
    print(TRAIN_DATASETS_PATH)
    print(LEARNING_RATE)
