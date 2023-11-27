import os
import random
import shutil
import argparse
from tqdm import tqdm
from omegaconf import OmegaConf


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_ratio", type=float, default=0.8)
    parser.add_argument("--base_cfg_path", type=str, default="configs/base_config.yaml")
    parser.add_argument("--dataset_root", type=str, default="dataset/Quickdraw-Dataset/png")
    parser.add_argument("--new_dataset_root", type=str, default="dataset/Quickdraw-Dataset/png_splitted")
    parser.add_argument("--use_limitation", action="store_true")
    parser.add_argument("--limitation", type=int, default=1000)
    args = parser.parse_args()

    base_cfg = OmegaConf.load(args.base_cfg_path)

    train_data_dir = os.path.join(args.new_dataset_root, "train")
    test_data_dir = os.path.join(args.new_dataset_root, "test")

    classes = os.listdir(args.dataset_root)
    classes = [_class for _class in classes if _class in base_cfg.target_categories]

    for class_name in tqdm(classes):
        class_dir = os.path.join(args.dataset_root, class_name)
        files = os.listdir(class_dir)
        random.shuffle(files)

        train_size = int(args.train_ratio * len(files))
        train_files = files[:train_size]
        test_files = files[train_size:]

        if args.use_limitation:
            train_files = [file for i, file in enumerate(train_files) if i<(args.limitation*args.train_ratio) ]
            test_files = [file for i, file in enumerate(test_files) if i<(args.limitation*(1-args.train_ratio))]

        os.makedirs(os.path.join(train_data_dir, class_name), exist_ok=True)
        for file in tqdm(train_files, leave=False):
            src = os.path.join(class_dir, file)
            dst = os.path.join(train_data_dir, class_name, file)
            shutil.copy(src, dst)

        os.makedirs(os.path.join(test_data_dir, class_name), exist_ok=True)
        for file in tqdm(test_files, leave=False):
            src = os.path.join(class_dir, file)
            dst = os.path.join(test_data_dir, class_name, file)
            shutil.copy(src, dst)
