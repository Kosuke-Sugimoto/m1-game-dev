import os
import argparse
import numpy as np
from PIL import Image
from tqdm import tqdm
from omegaconf import OmegaConf


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg_path", type=str, default="configs/base_config.yaml")
    parser.add_argument("--npy_dir", type=str, default="dataset/Quickdraw-Dataset/npy")
    parser.add_argument("--png_dir", type=str, default="dataset/Quickdraw-Dataset/png")
    args = parser.parse_args()

    cfg = OmegaConf.load(args.cfg_path)
    target_categories = cfg.target_categories

    for now_trg in tqdm(target_categories):
        npy_file = np.load(os.path.join(args.npy_dir, f"{now_trg}.npy"))
        npy_file = npy_file.reshape(-1, 28, 28)

        now_trg_dir = os.path.join(args.png_dir, now_trg)

        if os.path.exists(now_trg_dir):
            continue
        else:
            os.makedirs(now_trg_dir)

        for idx in tqdm(range(len(npy_file)), leave=False):
            img = npy_file[idx]
            img = Image.fromarray(img)
            img.save(os.path.join(now_trg_dir, f"{idx}.png"))
