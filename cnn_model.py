from torch import nn
import create_captcha


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=(1, 1)),  # [batch, 3, 180, 100] -> [batch, 16, 180, 100]
            nn.MaxPool2d(2, 2),  # [batch, 16, 180, 100] -> [batch, 16, 90, 50]
            nn.BatchNorm2d(16),  # BatchNorm 批规范化，加速模型收敛速度
            nn.ReLU(),

            nn.Conv2d(16, 64, kernel_size=3, padding=(1, 1)),  # [batch, 16, 90, 50] -> [batch, 64, 90, 50]
            nn.MaxPool2d(2, 2),  # [batch, 64, 90, 50] -> [batch, 64, 45, 25]
            nn.BatchNorm2d(64),
            nn.ReLU(),

            nn.Conv2d(64, 512, kernel_size=3, padding=(1, 1)),  # [batch, 64, 45, 25] -> [batch, 512, 45, 25]
            nn.MaxPool2d(2, 2),  # [batch, 512, 45, 25] -> [batch, 512, 22, 12]
            nn.BatchNorm2d(512),
            nn.ReLU(),

            nn.Conv2d(512, 512, kernel_size=3, padding=(1, 1)),  # [batch, 512, 22, 12] -> [batch, 512, 22, 12]
            nn.MaxPool2d(2, 2),  # [batch, 512, 22, 12] -> [batch, 512, 11, 6]
            nn.BatchNorm2d(512),
            nn.ReLU(),
        )
        self.fc = nn.Linear(512 * 11 * 6, create_captcha.ALL_CHAR_LEN * create_captcha.CAPTCHA_NUM_LEN)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(-1, 512 * 11 * 6)
        x = self.fc(x)
        return x


if __name__ == '__main__':
    model = CNN()
    print(model)
