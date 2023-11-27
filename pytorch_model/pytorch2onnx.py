import argparse
import torch
from torch import nn
from torchvision.models import mobilenet_v3_large

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pytorch_model_path", type=str, default="checkpoint/20231025_1508/4.pth")
    parser.add_argument("--onnx_model_path", type=str, default="checkpoint/20231025_1508/4_onnx.onnx")
    args = parser.parse_args()

    model = mobilenet_v3_large()
    model.classifier[3] = nn.Linear(1280, 11)
    model.load_state_dict(torch.load(args.pytorch_model_path, map_location="cpu"))
    model.eval()

    dummy_input = torch.rand((32, 3, 128, 128))

    torch.onnx.export(
        model,
        dummy_input,
        args.onnx_model_path,
        opset_version=12,
        input_names=['input'],
        output_names=['output']
    )
