FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python-is-python3 \
    cmake \
    build-essential \
    libopencv-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install --index-url https://download.pytorch.org/whl/cu117 \
    torch==2.0.0+cu117 \
    torchvision==0.15.1+cu117 \
    torchaudio==2.0.1 \
    && pip install \
    tqdm \
    wandb \
    omegaconf \
    opencv-python

# ==================== gsutil インストール ===========================
# ubuntu の /bin/sh には source コマンドがないため、代わりに . を用いる
WORKDIR /tmp
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-449.0.0-linux-x86_64.tar.gz
RUN tar -xf google-cloud-cli-449.0.0-linux-x86_64.tar.gz
RUN ./google-cloud-sdk/install.sh --rc-path /root/.bashrc --path-update true --quiet
RUN . /root/.bashrc
# ===================================================================

WORKDIR /work
