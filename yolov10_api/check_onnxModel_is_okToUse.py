####查看 onnx模型資訊
import onnx.helper

# 载入 ONNX 模型
model = onnx.load("yolov10n_int8_dynamic.onnx")

print("\n=== Model的输入資訊:")
for input_tensor in model.graph.input:
    elem_type = input_tensor.type.tensor_type.elem_type
    elem_type_str = onnx.helper.tensor_dtype_to_np_dtype(elem_type)
    shape = [dim.dim_value if dim.dim_value > 0 else "dynamic" for dim in input_tensor.type.tensor_type.shape.dim]
    print(f"Input Name: {input_tensor.name}, Type: {elem_type_str}, Shape: {shape}")

print("\n=== Model中的節點資訊 (node's name and Operator Type):")
for node in model.graph.node:
    print(f"Node: {node.name}, OpType: {node.op_type}")

print("\n=== Model的權重資訊:")
for initializer in model.graph.initializer:
    elem_type = initializer.data_type
    elem_type_str = onnx.helper.tensor_dtype_to_np_dtype(elem_type)
    print(f"Weight_Name: {initializer.name}, Data_Type: {elem_type_str}")
