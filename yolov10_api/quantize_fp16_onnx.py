##量化成FP16
from onnxruntime.transformers.float16 import convert_float_to_float16
import onnx

onnx_model = onnx.load("yolov10n.onnx")
fp16_model = convert_float_to_float16(onnx_model, keep_io_types=True)
onnx.save(fp16_model, "yolov10n_fp16.onnx")