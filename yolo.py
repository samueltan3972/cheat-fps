import cv2
import torch

img = cv2.imread("./ApexLegends.jpg")
print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")
print(torch.cuda.is_available())