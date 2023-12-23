import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = torch.relu(torch.max_pool2d(self.conv1(x), 2))
        x = torch.relu(torch.max_pool2d(self.conv2(x), 2))
        x = x.view(-1, 320)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.log_softmax(x, dim=1)

def load_model(model_path):
    model = torch.load(model_path, map_location=torch.device('cpu'))
    model.eval()
    return model

def predict(model, image_path):
    # Define the transformation
    transform = transforms.Compose([
        transforms.Resize((28, 28)),  # Resize the image to 28x28 pixels
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    # Load and transform the image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension

    # Make prediction
    with torch.no_grad():
        output = model(image)
        prediction = output.argmax(dim=1, keepdim=True)  # Get the index of the max log-probability
    return prediction.item()

def main():
    model_path = 'nnLib/mnist_cnn.pth'
    model = load_model(model_path)

    while True:
        image_path = input("Enter the path of the image file (or type 'exit' to quit): ").strip()
        if image_path.lower() == 'exit':
            break
        try:
            result = predict(model, image_path)
            print(f"Predicted class for {image_path}: {result}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

