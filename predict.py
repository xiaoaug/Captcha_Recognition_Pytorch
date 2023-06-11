import torch
import matplotlib.pyplot as plt

import cnn_model
import setting
import dataset


def predict() -> None:
    """
    预测
    :return: None
    """
    my_model.eval()
    print("----> Start Predicting")

    with torch.inference_mode():
        for idx, (image, label) in enumerate(dataloader, start=1):
            image, label = image.to(device), label.view(1, 4*36).to(device)
            pred_label = my_model(image)

            pred_label = pred_label.view(-1, 36)
            label = label.view(-1, 36)
            pred_label = torch.softmax(pred_label, dim=1)
            pred_label = torch.argmax(pred_label, dim=1)
            label = torch.argmax(label, dim=1)
            pred_label = pred_label.view(-1, 4)[0]
            label = label.view(-1, 4)[0]

            pred = ''.join([setting.ALL_CHAR[i] for i in pred_label.cpu().numpy()])
            true = ''.join([setting.ALL_CHAR[i] for i in label.cpu().numpy()])

            print('----> Pred: ' + pred)
            print('----> True: ' + true)

            plt.imshow(image.permute((0, 2, 3, 1))[0].cpu().numpy())
            plt.title(f'Predict: {pred}')
            plt.axis(False)
            plt.show()

            # 预测多少张图片结束？
            if idx >= 10:
                break
    print('----> Done')


if __name__ == '__main__':
    print('----> Checking Device')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f'----> Done: {device}')

    print('----> Creating Model')
    my_model = cnn_model.CNN().to(device)
    print('----> Done')

    print("----> Loading Checkpoint")
    my_model.load_state_dict(torch.load(setting.PTH_FILE, map_location=device))
    print("----> Done")

    dataloader = dataset.get_predict_data_loader()

    predict()
