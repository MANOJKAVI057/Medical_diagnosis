import cv2

def fake_heatmap(image_path: str) -> str:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    heatmap = cv2.applyColorMap(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLORMAP_JET)
    output_path = image_path.replace("temp/", "temp/heatmap_")
    cv2.imwrite(output_path, heatmap)
    return output_path