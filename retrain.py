import os
import glob
import random
import argparse
import numpy as np
import torch
from torch import nn, optim
from torchvision import transforms
from torchvision.models import mobilenet_v3_large
from PIL import Image
from tqdm import tqdm
from sklearn.model_selection import train_test_split


def seed_everything(seed_value):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


TARGET = [
    "bird", "cat", "dog", "fish",
    "scorpion", "snake", "spider",
    "sword", "tiger", "rifle", "leaf"
]


class Dataset(torch.utils.data.Dataset):
    def __init__(self, imagelist: list, path2idx: dict):
        self.imagelist = imagelist
        self.path2idx = path2idx
        
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])

    def __getitem__(self, idx):
        img_path = self.imagelist[idx]
        img_idx = self.path2idx[img_path]
        label = torch.zeros(len(TARGET))
        label[img_idx] = 1
        img = Image.open(img_path)
        img = self.transform(img)
        img = torch.stack([img, img, img], dim=1)
        img = img.squeeze(0)

        return img, label

    def __len__(self):
        return len(self.imagelist)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_dir", type=str, default="dataset/Quickdraw-Dataset/png")
    parser.add_argument("--retrain_model_path", type=str, default="checkpoint/retrained_mobilenetv3")
    args = parser.parse_args()

    target2idx = dict(zip(TARGET, range(len(TARGET))))
    imagelist = glob.glob(os.path.join(args.dataset_dir, "**", "*.png"), recursive=True)
    path2idx = {path: target2idx[path.split("/")[-2]] for path in imagelist}
    idx2pathlist = {}
    for path, idx in path2idx.items():
        if idx not in idx2pathlist.keys():
            idx2pathlist[idx] = []
        idx2pathlist[idx].append(path)
    
    train_imagelist = []
    test_imagelist = []

    for idx, pathlist in idx2pathlist.items():
        train_pathlist, test_pathlist = train_test_split(pathlist, test_size=0.1)
        train_imagelist.extend(train_pathlist)
        test_imagelist.extend(test_pathlist)

    model = mobilenet_v3_large(pretrained=True)
    model.classifier[3] = nn.Linear(in_features=1280, out_features=len(TARGET))

    train_dataset = Dataset(train_imagelist, path2idx)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_dataset = Dataset(test_imagelist, path2idx)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32, shuffle=True)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(),
                          lr=0.001,
                          momentum=0.9)

    last_content = []

    for epoch in range(20):
        model.to("cuda")
        model.train()

        for data in tqdm(train_loader):
            inputs, labels = data
            inputs, labels = inputs.to("cuda"), labels.to("cuda")

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        model.to("cuda")
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data in tqdm(test_loader):
                images, labels = data
                images, labels = images.to("cuda"), labels.to("cuda")
                outputs = model(images)
                _, predicted_indice = torch.max(outputs.data, 1)
                _, gt_indice = torch.max(labels.data, 1)
                total += labels.size(0)
                correct += (predicted_indice == gt_indice).sum().item()
        val_acc = (100 * correct / total)
        print('Accuracy: %.2f%%' % val_acc)

        last_content.append(f"{epoch} eval_acc: {val_acc}\n")

        torch.save(model.state_dict(), f"{args.retrain_model_path}_{epoch}.pth")

    with open("retrain.txt", "w") as file:
        file.writelines(last_content)
