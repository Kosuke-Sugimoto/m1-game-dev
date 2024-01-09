"""dataset.py

モジュールの説明ではないが、
Dataset, DataLoader の高速化について参考になる記事があったのでメモ
https://qiita.com/sugulu_Ogawa_ISID/items/62f5f7adee083d96a587

"""

# python 3.9 以上なら型ヒントで tuple が使えるが、今回は 3.8 のため Tuple を利用
# python 3.10 以上なら型ヒントで | が使えるが、今回は 3.8 のため Union を利用
import os
import gc
import torch
import argparse
from tqdm import tqdm
from glob import glob
from PIL import Image
from typing import Optional, Union, Tuple
from omegaconf import OmegaConf
from collections import defaultdict
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from sklearn.model_selection import train_test_split


class QuickdrawDataset(Dataset):
    def __init__(self, 
                 imagelist: list, 
                 path2idx: dict, 
                 num_categories: int,
                 img_size: Union[int, Tuple[int, int]]):

        self.imagelist = imagelist
        self.path2idx = path2idx
        self.num_categories = num_categories

        if isinstance(img_size, tuple):
            self.img_size = img_size
        else:
            self.img_size = (img_size, img_size)
        
        self.transform = transforms.Compose([
            transforms.Resize(self.img_size),
            transforms.ToTensor()
        ])

    def __getitem__(self, idx):
        img_path = self.imagelist[idx]
        img_idx = self.path2idx[img_path]

        label = F.one_hot(torch.LongTensor([img_idx]), num_classes=self.num_categories).squeeze()

        img = Image.open(img_path)
        img = self.transform(img).squeeze()

        return img, label

    def __len__(self):
        return len(self.imagelist)


class MyCollator(object):
    def __init__(self, 
                 num_channels: int,
                 num_categories: int,
                 img_size: Union[int, Tuple[int, int]]):

        self.num_channels = num_channels
        self.num_categories = num_categories
        
        if isinstance(img_size, tuple):
            self.img_size = img_size
        else:
            self.img_size = (img_size, img_size)
    
    def __call__(self, batch):
        batch_size = len(batch)

        imgs = torch.zeros((batch_size, self.num_channels, *self.img_size))
        labels = torch.zeros((batch_size, self.num_categories))

        for bid, (img, label) in enumerate(batch):
            imgs[bid] = img.unsqueeze(0).repeat(self.num_channels, 1, 1)
            labels[bid] = label

        return imgs, labels


def build_dataloader(imagelist: list,
                     batch_size: int,
                     path2idx: dict,
                     num_workers: Optional[int],
                     num_channels: int,
                     num_categories: int,
                     img_size: Union[int, Tuple[int, int]],
                     is_train: bool,
                     device: Union[str, torch.device]):
    dataset = QuickdrawDataset(imagelist, path2idx, num_categories, img_size)
    collate_fn = MyCollator(num_channels, num_categories, img_size)

    if num_workers is None:
        # os.cpu_count(), os.cpu_count()//2 - 1
        # などを指定すると(恐らく)メモリが足りなくなるため調整
        num_workers = os.cpu_count() // 4

    dataloader = DataLoader(dataset,
                            batch_size=batch_size,
                            shuffle=is_train,
                            num_workers=num_workers,
                            drop_last=True,
                            collate_fn=collate_fn,
                            pin_memory=(device != "cpu"))

    return dataloader


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_dir", type=str, default="dataset/Quickdraw-Dataset/png")
    parser.add_argument("--base_cfg_path", type=str, default="configs/base_config.yaml")
    parser.add_argument("--train_cfg_path", type=str, default="configs/train_config.yaml")
    args = parser.parse_args()

    base_cfg = OmegaConf.load(args.base_cfg_path)
    train_cfg = OmegaConf.load(args.train_cfg_path)

    num_categories = len(base_cfg.target_categories)

    # train_list, test_list を定義
    # path から idx への対応を持つ dict も定義
    # defaultdict で 初期値が list の dict 作成
    category2idx = dict(zip(base_cfg.target_categories, range(num_categories)))
    full_imagelist = glob(os.path.join(args.dataset_dir, "**", "*.png"), recursive=True)
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
    
    del category2idx, full_imagelist, idx2pathlist
    gc.collect()

    train_dataloader = build_dataloader(
        imagelist=train_imagelist,
        batch_size=train_cfg.train_batch_size,
        path2idx=path2idx,
        num_workers=train_cfg.num_workers,
        num_channels=train_cfg.num_channels,
        num_categories=num_categories,
        img_size=train_cfg.img_size,
        is_train=True,
        device=torch.device(train_cfg.device)
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
        device=torch.device(train_cfg.device)
    )

    for data in tqdm(train_dataloader):
        imgs, labels = data
