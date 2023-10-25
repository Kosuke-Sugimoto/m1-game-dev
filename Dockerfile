FROM tensorflow/tensorflow:2.12.0-gpu

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install \
    tqdm \
    wandb \
    omegaconf \
    opencv-python \
    scikit-learn \
    model-compression-toolkit \
    onnx \
    onnx-tf

WORKDIR /work
