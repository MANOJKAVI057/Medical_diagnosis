import torch

def preprocess_image(file_path):
    from PIL import Image
    import torchvision.transforms as transforms

    img = Image.open(file_path).convert("RGB")  # ensures 3 channels
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),  # converts to [C,H,W] and scales 0-1
        # optionally normalize here if your model expects it
    ])
    img_tensor = transform(img)  # shape [3,224,224]
    img_tensor = img_tensor.unsqueeze(0)  # add batch dimension -> [1,3,224,224]
    return img_tensor