import random
import numpy as np
import torch
from tqdm import tqdm
from typing import Any, Union
from torch.utils.data import DataLoader


def seed_everything(seed_value):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def evaluate(model: Any,
             dataloader: DataLoader,
             device: Union[str, torch.device]):

    total_correct, total_labels = 0, 0

    model.to(device)
    model.eval()

    with torch.no_grad():
        for data in tqdm(dataloader):
            imgs, labels = data
            imgs, labels = imgs.to(device), labels.to(device)

            outputs = model(imgs)

            # ont-hot なので index を求めれば解答へ変換可能
            _, predict_indice = torch.max(outputs.data, 1)
            _, gt_indice = torch.max(labels.data, 1)

            total_labels += labels.size(0)
            total_correct += (predict_indice == gt_indice).sum().item()

    eval_acc = (100 * total_correct / total_labels)

    return eval_acc
