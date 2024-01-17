import time
import torch
from PIL import Image
from torchvision import transforms

#creator must tell us which splits work. [   first split arangment:[(start split 1, end split 1, size in mb), (second hop start, seconf hop end, size)], next split arrangment:[...],...]
global supported_splits
supported_splits=[ [(0,0,0),(1,1,0),(2,2,0),(3,3,0),(4,4,0),(5,5,0)], [(0,1,0),(2,3,0),(4,5,0)], [(0,2,0),(3,5,0)], [(0,5,0)] ]

def load_image(image_path):
    # Define the transformation
    transform = transforms.Compose([
        transforms.Resize((640, 640)),  # Resize the image to 640x640 pixels
        transforms.ToTensor(),          # Convert to a PyTorch tensor
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Normalize
    ])

    # Load the image and apply the transformation
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)  # Add a batch dimension

def run_full_model(model, input_tensor):
    """
    Run an input tensor through the entire YOLOv5 model.

    :param model: YOLOv5 model.
    :param input_tensor: Input tensor for the model.
    :return: Output after processing through the model.
    """
    with torch.no_grad():
        return model(input_tensor)


def getModel():
    return torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def predict(model, layer_start, layer_end):
    # Process an image
    input_tensor = load_image("testImage.jpg")
    out=0
    for i in range(layer_start, layer_end):
        time.sleep(1)
        #out=0
        #out= run_full_model(model, input_tensor)
    return out