# model_loader.py

import torch
from torchvision import models, transforms
from PIL import Image
import json

# Load class labels
with open("labels.json", "r") as f:
    class_names = json.load(f)

# Load the model
def load_model(model_path="poultry_model.pt", num_classes=4):
    from torchvision.models import mobilenet_v2, MobileNet_V2_Weights
    weights = MobileNet_V2_Weights.DEFAULT
    model = mobilenet_v2(weights=weights)
    model.classifier[1] = torch.nn.Linear(model.last_channel, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

model = load_model()

# Image transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Prediction function with calibrated confidence
def predict(image_file, confidence_threshold=0.60, entropy_threshold=1.2):
    image = Image.open(image_file).convert('RGB')
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        logits = outputs.squeeze(0)
        probabilities = torch.nn.functional.softmax(logits, dim=0)

        confidence, predicted = torch.max(probabilities, 0)
        confidence = confidence.item()

        
        entropy = -torch.sum(probabilities * torch.log(probabilities + 1e-9)).item()
        if confidence < confidence_threshold or entropy > entropy_threshold:
            return {
                "disease": "Unknown",
                "confidence": f"{round(confidence * 100, 2)}%"
            }

        return {
            "disease": class_names[predicted.item()],
            "confidence": f"{round(confidence * 100, 2)}%"
        }


