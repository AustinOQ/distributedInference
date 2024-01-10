import torch
from PIL import Image
from torchvision import transforms

#creator must tell us which splits work. In future we may want to include sizes of splits in tuples. 
supported_splits=[ [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)], [(0,1),(2,3),(4,5)], [(0,2),(3,5)], [(0,5)] ]

#creator should include name of virtual env that has been tested w this nn. 
virtual_env_name="/home/austin/venv/yolo/bin/activate"

#activate the virtual env as soon as this file is imported by server.py


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
    for i in range(layer_start, layer_end):
        out= run_full_model(model, input_tensor)
    return out