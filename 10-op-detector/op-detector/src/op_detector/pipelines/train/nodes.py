# src/op_detector/pipelines/train/nodes.py

import os
import certifi

# Ensure SSL certificate checks use certifi’s bundle
os.environ["SSL_CERT_FILE"] = certifi.where()

import shutil
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models

def train_model(raw_images_dir: str, model_output: str, epochs: int):
    """
    Train a ResNet18 on images under raw_images_dir, skipping any sub-folder
    (label) that contains no valid image files. Uses certifi for SSL.
    """
    # 1) Prune out empty class folders
    valid_exts = {
        ".jpg", ".jpeg", ".png", ".ppm", ".bmp",
        ".pgm", ".tif", ".tiff", ".webp"
    }
    for cls in os.listdir(raw_images_dir):
        cls_dir = os.path.join(raw_images_dir, cls)
        if not os.path.isdir(cls_dir):
            continue
        if not any(
            os.path.splitext(f)[1].lower() in valid_exts
            for f in os.listdir(cls_dir)
        ):
            shutil.rmtree(cls_dir)
            print(f"⚠️  Skipped empty class '{cls}'")

    # 2) Build the dataset & loader
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    dataset = datasets.ImageFolder(root=raw_images_dir, transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    # 3) Instantiate & modify the model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet18(pretrained=True)  # will now verify SSL correctly
    model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))
    model.to(device)

    # 4) Training loop
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    model.train()
    for epoch in range(1, epochs + 1):
        running_loss = 0.0
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * imgs.size(0)
        epoch_loss = running_loss / len(loader.dataset)
        print(f"Epoch {epoch}/{epochs} — Loss: {epoch_loss:.4f}")

    # 5) Save checkpoint
    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    torch.save({
        "model_state": model.state_dict(),
        "classes":     dataset.classes
    }, model_output)
    print(f"✅  Model and class list saved to {model_output}")
