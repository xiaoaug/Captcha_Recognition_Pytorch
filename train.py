import os
import torch
from torch import nn
from tqdm import tqdm
from torch.autograd import Variable

import cnn_model
import dataset
import plot_curves

# setting
BATCH_SIZE = 64  # 一次训练的样本量
NUM_WORKERS = 2  # 有多少子进程将用于数据的加载，若使用 Windows 建议设置为 0
NUM_EPOCHS = 8  # 训练轮数
LEARNING_RATE = 1e-3  # 训练学习率
PTH_PATH = os.getcwd()  # 训练完成后的模型保存位置
CONTINUE_TRAIN = False  # 是否使用以前的 pth 文件继续训练？
PTH_FILE = f"{PTH_PATH}/checkpoint_85.4293%.pth"  # 调用以前训练好的 pth 文件继续训练


def calculate_acc(pred_label, target_label) -> float:
    """
    计算准确率
    :param pred_label: 预测标签
    :param target_label: 目标标签
    :return: 准确率
    """
    pred_label, target_label = pred_label.view(-1, 36), target_label.view(-1, 36)
    pred_label = torch.softmax(pred_label, dim=1)  # softmax 处理完后取最大索引
    pred_label = torch.argmax(pred_label, dim=1)
    target_label = torch.argmax(target_label, dim=1)
    pred_label, target_label = pred_label.view(-1, 4), target_label.view(-1, 4)
    correct_list = []
    for i, j in zip(target_label, pred_label):
        if torch.equal(input=i, other=j):
            correct_list.append(1)
        else:
            correct_list.append(0)
    acc = sum(correct_list) / len(correct_list)
    return acc


def train_step(
    model: torch.nn.Module,
    dataloader: torch.utils.data.DataLoader,
    loss_function: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    curr_epoch: int,
) -> tuple[float, float]:
    """
    单轮训练
    :param model: 模型
    :param dataloader: 训练数据集
    :param loss_function: 损失函数
    :param optimizer: 优化器
    :param curr_epoch: 当前训练的轮数
    :return: [平均损失, 平均准确度]
    """
    model.train()
    all_loss, all_acc = [], []
    aver_loss, aver_acc = 0.0, 0.0  # 平均损失，平均准确率

    t = tqdm(enumerate(dataloader, start=1), total=len(dataloader))  # 进度条

    for batch_idx, (image, label) in t:
        image, label = Variable(image).to(device), Variable(label).to(
            device
        )  # 将数据发送到目标设备
        pred_label = model(image)  # 前向传递
        loss = loss_function(pred_label, label)  # 计算损失
        optimizer.zero_grad()  # 优化器清零
        loss.backward()  # 反向传播
        optimizer.step()  # 优化器更新

        acc = calculate_acc(pred_label=pred_label, target_label=label)
        all_acc.append(float(acc))
        all_loss.append(float(loss.item()))
        aver_acc = torch.mean(torch.Tensor(all_acc))  # 平均准确率
        aver_loss = torch.mean(torch.Tensor(all_loss))  # 平均损失

        t.set_description(f"[Train Epoch = {curr_epoch}/{NUM_EPOCHS}]")
        t.set_postfix(Train_Loss=f"{aver_loss:.4f}", Train_Acc=f"{aver_acc:.4f}")

    return aver_loss, aver_acc


def test_step(
    model: torch.nn.Module,
    dataloader: torch.utils.data.DataLoader,
    loss_function: torch.nn.Module,
    curr_epoch: int,
) -> tuple[float, float]:
    """
    单轮验证测试
    :param model: 模型
    :param dataloader: 测试数据集
    :param loss_function: 损失函数
    :param curr_epoch: 当前训练的轮数
    :return: [平均损失, 平均准确度]
    """
    model.eval()
    all_loss, all_acc = [], []
    aver_loss, aver_acc = 0.0, 0.0  # 平均损失，平均准确率

    t = tqdm(enumerate(dataloader, start=1), total=len(dataloader))  # 进度条

    with torch.inference_mode():
        for batch_idx, (image, label) in t:
            image, label = Variable(image).to(device), Variable(label).to(
                device
            )  # 将数据发送到目标设备
            pred_label = model(image)  # 前向传播
            loss = loss_function(pred_label, label)  # 计算损失
            acc = calculate_acc(pred_label=pred_label, target_label=label)
            all_acc.append(float(acc))
            all_loss.append(float(loss.item()))
            aver_acc = torch.mean(torch.Tensor(all_acc))  # 平均准确率
            aver_loss = torch.mean(torch.Tensor(all_loss))  # 平均损失

            t.set_description(f"[Test  Epoch = {curr_epoch}/{NUM_EPOCHS}]")
            t.set_postfix(Test_Loss=f"{aver_loss:.4f}", Test_Acc=f"{aver_acc:.4f}")

    return aver_loss, aver_acc


def train(
    model: torch.nn.Module,
    train_dataloader: torch.utils.data.DataLoader,
    test_dataloader: torch.utils.data.DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_function: torch.nn.Module = nn.CrossEntropyLoss(),
) -> dict[str, list]:
    """
    训练
    :param model: 模型
    :param train_dataloader: 训练数据集
    :param test_dataloader: 测试数据集
    :param optimizer: 优化器
    :param loss_function: 损失函数
    :return: dict{ 训练平均损失, 训练准确度, 测试平均损失, 测试准确度 }
    """
    global best_acc
    # 创建空结果字典，用于后期 plt 绘图
    results = {"train_loss": [], "train_acc": [], "test_loss": [], "test_acc": []}

    print("----> Start Training")

    # 循环执行训练和测试
    for epoch in range(1, NUM_EPOCHS + 1):
        train_loss, train_acc = train_step(
            model=model,
            dataloader=train_dataloader,
            loss_function=loss_function,
            optimizer=optimizer,
            curr_epoch=epoch,
        )
        test_loss, test_acc = test_step(
            model=model,
            dataloader=test_dataloader,
            loss_function=loss_function,
            curr_epoch=epoch,
        )

        # 生成 pth 文件
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(
                model.state_dict(), f"{PTH_PATH}/checkpoint_{test_acc*100:.4f}%.pth"
            )

        # 更新结果字典
        results["train_loss"].append(train_loss)
        results["train_acc"].append(train_acc)
        results["test_loss"].append(test_loss)
        results["test_acc"].append(test_acc)

    print("----> Done")
    return results


if __name__ == "__main__":
    print("----> Checking Device")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"----> Done: {device}")

    best_acc = 0.0  # 最佳正确率

    print("----> Creating Model")
    my_model = cnn_model.CNN().to(device)
    loss_fn = nn.MultiLabelSoftMarginLoss().to(device)  # 损失函数
    optim = torch.optim.Adam(params=my_model.parameters(), lr=LEARNING_RATE)  # 优化器
    print("----> Done")

    if CONTINUE_TRAIN:
        print("----> Loading Checkpoint")
        my_model.load_state_dict(torch.load(PTH_FILE))
        print("----> Done")

    model_results = train(
        model=my_model,
        train_dataloader=dataset.get_train_data_loader(),
        test_dataloader=dataset.get_test_data_loader(),
        optimizer=optim,
        loss_function=loss_fn,
    )
    plot_curves.plot_curves(model_results)
