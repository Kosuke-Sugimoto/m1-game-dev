import os
import argparse
import numpy as np
from PIL import Image

TARGET = [
    "bird", "cat", "dog", "fish",
    "scorpion", "snake", "spider",
    "sword", "tiger", "rifle", "leaf"
]

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=str, nargs="*", default=TARGET)
    args = parser.parse_args()

    for now_trg in args.target:
        npy_file = np.load(f"dataset/Quickdraw-Dataset/npy/{now_trg}.npy")
        npy_file = npy_file.reshape(-1, 28, 28)

        for idx in range(len(npy_file)):
            if idx == 0:
                os.makedirs(f"dataset/Quickdraw-Dataset/png/{now_trg}", exist_ok=True)

            img = npy_file[idx]
            img = Image.fromarray(img)
            img.save(f"dataset/Quickdraw-Dataset/png/{now_trg}/{idx}.png")
