from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO('best.pt')

# Export the model
model.export(format='openvino')  # creates 'yolov8n_openvino_model/'

#load exported OpenVINO model
ov_model = YOLO('weights_openvino_model/')