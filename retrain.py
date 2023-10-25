import os
import argparse
import torch
import wandb
from tqdm import tqdm
from glob import glob
from pathlib import Path
from typing import Union, Any
from datetime import datetime
from collections import defaultdict
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights
from sklearn.model_selection import train_test_split

from dataset import build_dataloader
from utils import seed_everything, evaluate


def retrain(model: Any,
            optimizer: Any,
            criterion: Any,
            num_categories: int,
            base_cfg: DictConfig,
            train_cfg: DictConfig,
            dataset_dir: Union[str, Path],
            checkpoint_dir: Union[str, Path],
            run_name: str):

    now_device = torch.device(train_cfg.device)
    
    category2idx = dict(zip(base_cfg.target_categories, range(num_categories)))
    
    full_imagelist = glob(os.path.join(dataset_dir, "**", "*.png"), recursive=True)
    trg_imagelist = [path for path in full_imagelist
                     if path.split("/")[-2] in base_cfg.target_categories]
    
    path2idx = {path: category2idx[path.split("/")[-2]] for path in trg_imagelist}
    
    idx2pathlist = defaultdict(list)
    for path, idx in path2idx.items():
        idx2pathlist[idx].append(path)
    
    train_imagelist, test_imagelist = [], []
    for _, pathlist in idx2pathlist.items():
        train_pathlist, test_pathlist = train_test_split(pathlist, test_size=0.1)
        train_imagelist.extend(train_pathlist)
        test_imagelist.extend(test_pathlist)

    train_dataloader = build_dataloader(
        imagelist=train_imagelist,
        batch_size=train_cfg.train_batch_size,
        path2idx=path2idx,
        num_workers=train_cfg.num_workers,
        num_channels=train_cfg.num_channels,
        num_categories=num_categories,
        img_size=train_cfg.img_size,
        is_train=True,
        device=now_device
    )
    test_dataloader = build_dataloader(
        imagelist=test_imagelist,
        batch_size=train_cfg.test_batch_size,
        path2idx=path2idx,
        num_workers=train_cfg.num_workers,
        num_channels=train_cfg.num_channels,
        num_categories=num_categories,
        img_size=train_cfg.img_size,
        is_train=False,
        device=now_device
    )

    artifact = wandb.Artifact(
        name=f"{run_name}",
        type="model_weight",
        description="model weights"
    )

    for epoch in tqdm(range(train_cfg.num_epochs)):
        epoch_loss = 0

        for itr, data in enumerate(tqdm(train_dataloader, leave=False)):
            imgs, labels = data
            imgs, labels = imgs.to(now_device), labels.to(now_device)

            model.to(now_device)
            model.train()

            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.data

        eval_acc = evaluate(model, test_dataloader, now_device)
        epoch_loss /= (itr+1)

        wandb.log({"train_loss": epoch_loss, "test_acc": eval_acc})

        if epoch % train_cfg.num_epochs_per_save == 0:
            path = os.path.join(checkpoint_dir, f"{epoch}.pth")
            torch.save(model.state_dict(), path)
            artifact.add_file(local_path=path, name=f"epoch{epoch}_weight")

    wandb.log_artifact(artifact)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_name", type=str, default="quickdraw-dataset")
    parser.add_argument("--run_name", type=str, default=datetime.now().strftime("%Y%m%d_%H%M"))
    parser.add_argument("--dataset_dir", type=str, default="dataset/Quickdraw-Dataset/png")
    parser.add_argument("--checkpoint_dir", type=str, default="checkpoint")
    parser.add_argument("--base_cfg_path", type=str, default="configs/base_config.yaml")
    parser.add_argument("--train_cfg_path", type=str, default="configs/train_config.yaml")
    parser.add_argument("--retrain_filename", type=str, default="retrained_mobilenetv3")
    args = parser.parse_args()

    base_cfg = OmegaConf.load(args.base_cfg_path)
    train_cfg = OmegaConf.load(args.train_cfg_path)

    args.checkpoint_dir = os.path.join(args.checkpoint_dir, args.run_name)
    os.makedirs(args.checkpoint_dir)

    num_categories = len(base_cfg.target_categories)

    seed_everything(train_cfg.seed)

    wandb.init(
        project=args.project_name,
        name=args.run_name,
        config=dict(train_cfg)
    )

    model = mobilenet_v3_large(weights=MobileNet_V3_Large_Weights.DEFAULT)
    model.classifier[3] = nn.Linear(in_features=1280, out_features=num_categories)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(),
                          lr=train_cfg.learning_rate,
                          momentum=train_cfg.momentum)

    retrain(model, 
            optimizer, 
            criterion,
            num_categories=num_categories,
            base_cfg=base_cfg,
            train_cfg=train_cfg,
            dataset_dir=args.dataset_dir,
            checkpoint_dir=args.checkpoint_dir,
            run_name=args.run_name)
