"""
This is a boilerplate pipeline 'train'
generated using Kedro 1.0.0
"""
import os
import shutil
import torch
from torch import nn, optim
from torchvision import datasets, transforms, models

def train_model(
    raw_images_dir: str,
    model_output: str,
    epochs: int,
    batch_size: int,
    learning_rate: float
) -> None:
    """
    Train a ResNet18 classifier on the scraped fatigue-event images.
    """

    # 0) Remove any empty class folders so ImageFolder won't error
    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    for cls in os.listdir(raw_images_dir):
        cls_dir = os.path.join(raw_images_dir, cls)
        if os.path.isdir(cls_dir):
            if not any(f.lower().endswith(tuple(valid_exts)) for f in os.listdir(cls_dir)):
                shutil.rmtree(cls_dir)
                print(f"⚠️  Removed empty folder: {cls_dir}")

    # 1) Prepare dataset & loader
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    dataset = datasets.ImageFolder(raw_images_dir, transform=transform)
    loader  = torch.utils.data.DataLoader(
        dataset, batch_size=batch_size, shuffle=True
    )

    # 2) Build model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model  = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))
    model.to(device)

    # 3) Training loop
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
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

        epoch_loss = running_loss / len(dataset)
        print(f"Epoch {epoch}/{epochs} — Loss: {epoch_loss:.4f}")

    # 4) Save model + class map
    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    torch.save({
        "model_state": model.state_dict(),
        "classes":     dataset.classes
    }, model_output)
    print(f"✅  Model saved to {model_output}")
