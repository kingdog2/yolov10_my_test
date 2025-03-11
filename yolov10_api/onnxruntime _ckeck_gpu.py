import onnxruntime as ort

print(ort.__version__)
available_providers = ort.get_available_providers()
print(f"可用的執行提供者: {available_providers}")

if 'CUDAExecutionProvider' in available_providers:
    print("GPU 支援已啟用！")
else:
    print("GPU 支援未啟用，可能是沒有安裝 `onnxruntime-gpu` 或未正確配置 CUDA。")
