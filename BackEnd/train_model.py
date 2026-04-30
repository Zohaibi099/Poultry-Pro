import os
import pandas as pd
import torch
import torch.nn as nn
from torchvision import transforms, models
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

print("📁 Loading CSV and preparing dataset...")

# -----------------------
# 📁 Dataset Config
# -----------------------
csv_path = "C:/Users/Zohaib/Desktop/Poultry Pro/dd/train_data.csv"
image_folder = "C:/Users/Zohaib/Desktop/Poultry Pro/dd/train"
df = pd.read_csv(csv_path)

# -----------------------
# 🔠 Label Encoding
# -----------------------
label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['label'])
num_classes = len(label_encoder.classes_)

# -----------------------
# 🧪 Train/Val Split
# -----------------------
train_df, val_df = train_test_split(df, test_size=0.2, stratify=df['label_encoded'], random_state=42)

# -----------------------
# 🧰 Custom Dataset Class
# -----------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),  # Converts to [0, 1] tensor
    transforms.Normalize([0.485, 0.456, 0.406], 
                         [0.229, 0.224, 0.225])  # ImageNet normalization
])

class PoultryDataset(Dataset):
    def __init__(self, dataframe):
        self.data = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_name = os.path.join(image_folder, self.data.iloc[idx, 0])
        label = self.data.iloc[idx, 2]
        image = Image.open(img_name).convert('RGB')
        image = self.transform(image)
        return image, label

print("✅ Dataset ready. Creating loaders...")

train_data = PoultryDataset(train_df)
val_data = PoultryDataset(val_df)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32)

# -----------------------
# 🧠 Load Pretrained Model
# -----------------------
print("🔁 Loading pretrained MobileNetV2 model...")
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
model.classifier[1] = nn.Linear(model.last_channel, num_classes)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

# -----------------------
# 🏋️ Training Loop
# -----------------------
print("🚀 Starting training loop...")
train_acc_list = []
val_acc_list = []

for epoch in range(10):
    print(f"\n📚 Epoch {epoch+1}/10 -------------------------------")
    
    model.train()
    total, correct = 0, 0
    for batch_idx, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        if (batch_idx + 1) % 10 == 0:
            print(f"🌀 Batch {batch_idx+1}/{len(train_loader)} - Loss: {loss.item():.4f}")

    train_acc = correct / total
    train_acc_list.append(train_acc)

    # Validation
    model.eval()
    total, correct = 0, 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    val_acc = correct / total
    val_acc_list.append(val_acc)

    print(f"✅ Epoch {epoch+1} Complete — Train Acc: {train_acc:.4f}, Val Acc: {val_acc:.4f}")

# -----------------------
# 💾 Save Model
# -----------------------
torch.save(model.state_dict(), 'poultry_model.pt')
print("\n✅ Model saved as poultry_model.pt")

# -----------------------
# 📊 Plot Accuracy Graph
# -----------------------
plt.plot(train_acc_list, label='Train Accuracy')
plt.plot(val_acc_list, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training vs Validation Accuracy')
plt.legend()
plt.savefig('accuracy_plot.png')
print("📈 Accuracy plot saved as accuracy_plot.png")
