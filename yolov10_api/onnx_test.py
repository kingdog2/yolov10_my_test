import onnxruntime as ort
import numpy as np
import cv2

print(ort.__version__)
# 創建會話，並檢查是否使用 INT8
providers = ort.get_available_providers()
print(providers)  # 這會顯示可用的計算提供者，可能會指示是否使用 INT8

# 載入 ONNX 模型
onnx_model = ort.InferenceSession("yolov10n.onnx", providers=['CUDAExecutionProvider'])


# 圖像縮放處理
def ratioresize(im, color=255):
    shape = im.shape[:2]
    new_h, new_w = 640, 640
    padded_img = np.ones((new_h, new_w, 3), dtype=np.uint8) * color

    r = min(new_h / shape[0], new_w / shape[1])
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))

    if shape[::-1] != new_unpad:
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)

    padded_img[: new_unpad[1], : new_unpad[0]] = im
    padded_img = np.ascontiguousarray(padded_img)
    return padded_img, 1 / r

image = cv2.imread("aa.jpg")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 圖像縮放處理
in_img, scale = ratioresize(image_rgb)
in_img = in_img / 255.0 - 0.5
in_img = np.transpose(in_img, (2, 0, 1))  # CHW
in_img = np.expand_dims(in_img, axis=0).astype(np.float32)

# 模型推理
output = onnx_model.run(None, {'images': in_img})
results = output[0][0]

# 分數篩選門檻 必須>0.25
print(results.shape)
print(results)
boxes = np.array([i for i in results if i[4] > 0.25])


print(boxes.shape)
print(boxes)

##座標縮放轉乘int32就好 分數和class不變
# boxes = (boxes * scale).astype(np.int32)
# [[179  38 292 145   0  45]
#  [122 146 233 186   0  48]
#  [ 13 282 167 471   0  41]
#  [283 117 323 169   0  42]]

print('-'*200)
print(boxes)
for box in boxes:
    # print(box)
    ##座標要轉乘int32
    x1, y1, x2, y2 = (box[:4] * scale).astype(np.int32)
    ##分數以及class_id
    conf = box[4]
    class_id = int(box[5])
    class_name = f"Class {class_id}"

    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)

    label = f"{class_name} ({conf*100:.2f}%)"
    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 顯示結果圖像
cv2.imshow("Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
