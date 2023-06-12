# 识别验证码图片

识别验证码图片，输出验证码文字。使用 pytorch 实现。

训练 8 epoch，准确率为 85.42%。

本项目在 Ubuntu 22.04 搭建使用。Windows 用户请自行测试。

<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/d23ace40-6a32-4565-8679-6932572bd917" width="300">
<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/345b6f5f-7a8f-42f1-a62f-447e02dd1616" width="300">
<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/eef149c6-70cb-4442-9bba-2587b8104302" width="300">
<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/0807fd33-bb18-40a4-9190-c9818041e57f" width="300">

# 数据集如何获取？
1. 在 setting.py 中根据你自己的情况修改参数，当然保持默认设置也可以~
2. 在 create_captcha.py 中调整 `TRAIN_COUNT`、`TEST_COUNT`、`PREDICT_COUNT` 参数，这些参数决定了生成多少张验证码图片。
3. 运行 create_captcha.py 即可。

# 如何训练？

1. 在 setting.py 中根据你自己的情况修改参数，保持默认也可以。
2. 运行 train.py 即可。

# 如何预测？

1. 在 setting.py 中根据你自己的情况修改参数，保持默认也可以。
2. 调整 predict.py 文件中第 42 行的参数，这个参数决定了程序最终需要预测多少张图片。
3. 运行 predict.py 即可。

# 不想自己训练？

本项目提供训练好的模型，可以自行下载使用。下载后请将文件放在本项目的主文件夹内。

链接：https://www.123pan.com/s/H6UtVv-h7ei.html
提取码: qVxw

