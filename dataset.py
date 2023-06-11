import os
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import setting


class CaptchaDataset(Dataset):
    def __init__(self, path: str, transform=None, label_transform=None):
        super(Dataset, self).__init__()
        self.image_paths = [os.path.join(path, image_name) for image_name in os.listdir(path)]
        self.transform = transform
        self.label_transform = label_transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image_name = image_path.split('.')[-2]  # 裁切后就剩下四位的验证码字符串
        assert len(image_name) == setting.CAPTCHA_NUM_LEN  # 不符合要求的 label 则抛异常

        image = Image.open(image_path).convert('RGB')
        if self.transform is not None:
            image = self.transform(image)

        # 对图片名（label）做独热编码
        label = []
        for i in image_name:
            tmp = [0] * setting.ALL_CHAR_LEN
            tmp[setting.ALL_CHAR.find(i)] = 1  # 将索引对应的值置 1
            label += tmp
        if self.label_transform is not None:
            label = self.label_transform(label)
        return image, torch.Tensor(label)


def get_train_data_loader() -> torch.utils.data.DataLoader:
    """
    获取训练数据
    :return: 训练数据
    """
    print('----> Loading Train Data')
    train_transform = transforms.Compose([
        transforms.Resize((setting.IMAGE_HEIGHT, setting.IMAGE_WIDTH)),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    train_dataset = CaptchaDataset(setting.TRAIN_DATASETS_PATH, transform=train_transform)
    train_dataloader = DataLoader(
        dataset=train_dataset,
        batch_size=setting.BATCH_SIZE,  # 每次训练的样本数
        shuffle=True,  # 打乱训练集的数据
        num_workers=setting.NUM_WORKERS)  # 子进程数
    print('----> Done')
    return train_dataloader


def get_test_data_loader() -> torch.utils.data.DataLoader:
    """
    获取测试数据
    :return: 测试数据
    """
    print('----> Loading Test Data')
    test_transform = transforms.Compose([
        transforms.Resize((setting.IMAGE_HEIGHT, setting.IMAGE_WIDTH)),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    test_dataset = CaptchaDataset(setting.TEST_DATASETS_PATH, transform=test_transform)
    test_dataloader = DataLoader(
        dataset=test_dataset,
        batch_size=setting.BATCH_SIZE,  # 每次测试的样本数
        shuffle=False,  # 不打乱测试集的数据
        num_workers=setting.NUM_WORKERS)  # 子进程数
    print('----> Done')
    return test_dataloader


def get_predict_data_loader() -> torch.utils.data.DataLoader:
    """
    获取预测数据
    :return: 预测数据
    """
    print('----> Loading Pred Data')
    pred_transform = transforms.Compose([
        transforms.Resize((setting.IMAGE_HEIGHT, setting.IMAGE_WIDTH)),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    pred_dataset = CaptchaDataset(setting.PREDICT_DATASETS_PATH, transform=pred_transform)
    pred_dataloader = DataLoader(
        dataset=pred_dataset,
        batch_size=1,   # 每次预测的样本数
        shuffle=False,  # 不打乱预测集的数据
        num_workers=setting.NUM_WORKERS)  # 子进程数
    print('----> Done')
    return pred_dataloader


if __name__ == '__main__':
    split_name = './datasets/pred_set/0.octd.png'.split('.')[-2]
    print(split_name)

    a = CaptchaDataset('./datasets/pred_set')
    b = a.__getitem__(0)
    print(b[0])
    print(b[1])
    c = get_train_data_loader()
    print(c)
