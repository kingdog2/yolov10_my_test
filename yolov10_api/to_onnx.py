from ultralytics import YOLOv10
model = YOLOv10.from_pretrained('jameslahm/yolov10n')

onnx_model_path = "yolov10n.onnx"
model.export(format='onnx')
print(f"模型已轉換為 ONNX 格式並儲存至: {onnx_model_path}")
