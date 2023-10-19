# 识别验证码图片

识别验证码图片，输出验证码文字。使用 pytorch 实现。

训练 8 epoch，准确率为 85.42%。

本项目测试环境为 Ubuntu 22.04，python 版本为 3.10.13。Windows 用户请自行测试。

<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/d23ace40-6a32-4565-8679-6932572bd917" width="300">
<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/345b6f5f-7a8f-42f1-a62f-447e02dd1616" width="300">
<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/eef149c6-70cb-4442-9bba-2587b8104302" width="300">
<img src="https://github.com/xiaoaug/Captcha_Recognition_Pytorch/assets/39291338/0807fd33-bb18-40a4-9190-c9818041e57f" width="300">

# 如何安装？

```
git clone https://github.com/xiaoaug/Captcha_Recognition_Pytorch.git  # 下载
cd Captcha_Recognition_Pytorch
pip install -r requirements.txt  # 安装
```

# 数据集如何获取？

1. 在 create_captcha.py 中根据自己的需求调整 9~17 行的参数（默认也可以）。
2. 运行 create_captcha.py 即可：`python create_captcha.py`。

# 如何训练？

1. 在 train.py 中根据你自己的需求调整 12~18 行的参数（默认也可以）。
2. 运行 train.py 即可：`python train.py`。

> 该项目每轮训练中，只要训练准确率比之前高，就会生成 pth 文件。若该轮训练的准确率比以往训练的准确率低，则不生成 pth 文件。

# 如何预测？
1. 在 predict.py 中根据你自己的需求调整 9~10 行的参数（默认也可以）。
2. 运行 predict.py 即可：`python predict.py`。

# 不想自己训练？

本项目提供训练好的模型，可以自行下载使用。下载后请将文件放在本项目的主文件夹内。

链接：https://www.123pan.com/s/H6UtVv-h7ei.html
提取码: qVxw

