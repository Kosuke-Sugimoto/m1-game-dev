import os
import argparse
import tensorflow as tf
import numpy as np
import model_compression_toolkit as mct
from typing import Union
from pathlib import Path
from datetime import datetime
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from model_compression_toolkit.target_platform_capabilities.tpc_models.tflite_tpc.latest import get_keras_tpc_latest
from model_compression_toolkit.exporter.model_exporter.keras.export_serialization_format import KerasExportSerializationFormat


def get_dataset(
    train_cfg: DictConfig,
    dataset_dir: Union[str, Path]
    ):

    datagen = ImageDataGenerator(
        horizontal_flip=True,
        validation_split=0.2
    )

    train_data = datagen.flow_from_directory(
        os.path.join(dataset_dir, "train"),
        target_size=(128, 128),
        color_mode="rgb",
        batch_size=train_cfg.train_batch_size,
        class_mode="categorical",
        subset="training",
        shuffle=True
    )

    test_data = datagen.flow_from_directory(
        os.path.join(dataset_dir, "test"),
        target_size=(128, 128),
        color_mode="rgb",
        batch_size=train_cfg.test_batch_size,
        class_mode="categorical",
        subset="validation",
        shuffle=False
    )

    return train_data, test_data


def gen_representative_dataset(_images, num_calibration_iterations):
    def _generator():
        for _ind in range(num_calibration_iterations):
            yield [tf.expand_dims(_images[0][_ind, :, :, :], axis=0)]
    return _generator


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_cfg_path", type=str, default="configs/base_config.yaml")
    parser.add_argument("--train_cfg_path", type=str, default="configs/train_config.yaml")
    parser.add_argument("--dataset_dir", type=str, default="dataset/Quickdraw-Dataset/png_splitted")
    parser.add_argument("--checkpoint_filename", type=str, default="retrained_model.h5")
    parser.add_argument("--quantized_filename", type=str, default="quantized_model.tflite")
    parser.add_argument("--checkpoint_dir", type=str, default=f"checkpoint/tensorflow/{datetime.now().strftime('%Y%m%d_%H%M')}")
    parser.add_argument("--base_model_trainable", action="store_true")
    parser.add_argument("--num_calibration_itr", type=int, default=20)
    args = parser.parse_args()

    base_cfg = OmegaConf.load(args.base_cfg_path)
    train_cfg = OmegaConf.load(args.train_cfg_path)

    float_model = MobileNetV3Small(input_shape=(128, 128, 3), include_top=False, weights="imagenet")
    float_model.trainable = args.base_model_trainable
    float_model = tf.keras.Sequential([
        float_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        Dense(len(base_cfg.target_categories), activation="softmax")
    ])

    train_data, test_data = get_dataset(train_cfg, args.dataset_dir)

    os.makedirs(args.checkpoint_dir)
    checkpoint = ModelCheckpoint(os.path.join(args.checkpoint_dir, args.checkpoint_filename), monitor="val_accuracy", verbose=1, save_best_only=True, mode="max")
    earlystop = EarlyStopping(monitor="val_accuracy", patience=2, verbose=1, restore_best_weights=True)

    float_model.compile(loss="categorical_crossentropy", optimizer=Adam(train_cfg.learning_rate), metrics=["accuracy"])
    float_model.fit(train_data, validation_data=test_data, batch_size=train_cfg.train_batch_size, epochs=train_cfg.num_epochs, callbacks=[checkpoint, earlystop])
    test_score = float_model.evaluate(test_data, verbose=0)
    print(f"Float model test accuracy: {test_score[1]:02.4f}")

    representative_dataset = gen_representative_dataset(train_data.next(), args.num_calibration_itr)

    tflite_int8_tpc = get_keras_tpc_latest()

    qat_model, _, _ = mct.qat.keras_quantization_aware_training_init(float_model,
                                                                     representative_dataset,
                                                                     core_config=mct.core.CoreConfig(),
                                                                     target_platform_capabilities=tflite_int8_tpc)
    qat_model.compile(loss="categorical_crossentropy", optimizer=Adam(train_cfg.learning_rate), metrics=["accuracy"], run_eagerly=True)
    test_score = qat_model.evaluate(test_data, verbose=0)
    print(f"PTQ model test accuracy: {test_score[1]:02.4f}")

    earlystop = EarlyStopping(monitor="val_accuracy", patience=2, verbose=1, restore_best_weights=True)
    qat_model.fit(train_data, validation_data=test_data, batch_size=train_cfg.train_batch_size, epochs=train_cfg.num_epochs, callbacks=[earlystop])
    test_score = qat_model.evaluate(test_data, verbose=0)
    print(f"QAT model test accuracy: {test_score[1]:02.4f}")

    quantized_model = mct.qat.keras_quantization_aware_training_finalize(qat_model)
    quantized_model.compile(loss="categorical_crossentropy", optimizer=Adam(train_cfg.learning_rate), metrics=["accuracy"])
    test_score = quantized_model.evaluate(train_data, verbose=0)
    print(f"Quantized model test accuracy: {test_score[1]:02.4f}")

    mct.exporter.keras_export_model(model=quantized_model, save_model_path=os.path.join(args.checkpoint_dir, args.quantized_filename),
                                    target_platform_capabilities=tflite_int8_tpc,
                                    serialization_format=KerasExportSerializationFormat.TFLITE)
