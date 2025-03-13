##有兩種方法quantize_static & quantize_dynamic
##########!!!!!!!!!1  有兩種方法quantize_static================================================================
## quantize_static() 推薦先preprocess
# 1.python -m onnxruntime.quantization.preprocess --input yolov10n.onnx --output yolov10n_optimized.onnx --skip_symbolic_shape True

# 2.開轉quantize_static
# from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
# import numpy as np
# import onnx
#
# class DataReader(CalibrationDataReader):
#     def __init__(self):
#         self.data = iter([{"images": np.random.rand(1, 3, 640, 640).astype(np.float32)}])  # ####輸入不能改仍然用 float32
#
#     def get_next(self):
#         return next(self.data, None)
#
# quantize_static(
#     model_input="yolov10n_optimized.onnx",
#     model_output="yolov10n_int8_static.onnx",
#     calibration_data_reader=DataReader(),
#     weight_type=QuantType.QInt8  # 但裡面的權重能改 INT8
# )
#
# onnx.checker.check_model("yolov10n_int8_static.onnx")




##########!!!!!!!!!2  quantize_dynamic================================================================
## quantize_dynamic() 通常不需要preprocess
from onnxruntime.quantization import quantize_dynamic, QuantType
#Int8
quantize_dynamic("yolov10n.onnx", "yolov10n_int8_dynamic.onnx", weight_type=QuantType.QInt8)
