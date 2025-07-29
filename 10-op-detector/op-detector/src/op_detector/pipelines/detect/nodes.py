"""
This is a boilerplate pipeline 'detect'
generated using Kedro 1.0.0
"""
# src/op_detector/pipelines/detect/nodes.py

from PIL import Image
import torch
from torchvision import transforms, models

def detect_op_character(image_path: str, model_path: str) -> None:
    """
    Load the trained ResNet checkpoint at `model_path`, predict the class
    of the image at `image_path`, and print the label.
    """
    # 1) Load checkpoint
    ckpt = torch.load(model_path, map_location="cpu")
    classes = ckpt["classes"]
    # 2) Rebuild model architecture
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, len(classes))
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    # 3) Prepare image
    img = Image.open(image_path).convert("RGB")
    prep = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    tensor = prep(img).unsqueeze(0)  # add batch dim
    # 4) Predict
    with torch.no_grad():
        out = model(tensor)
        idx = int(out.argmax(dim=1))
    print(f"🔍 Predicted character: {classes[idx]}")
