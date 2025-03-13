##精度轉成速度
# 運行 API
# netstat -ano | findstr :8000d
# curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@C:/Users/f2201/Downloads/yolov10_api/aa.jpg"
import time
import base64
from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse
import cv2
import numpy as np
import onnxruntime as ort

# 載入 ONNX 模型 CUDAExecutionProvider  CPUExecutionProvider
onnx_model = ort.InferenceSession("yolov10n_int8_static.onnx", providers=['CUDAExecutionProvider'])
print("模型載入成功")
app = FastAPI()
print("="*200)
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
def onnx_dectect(client_img):
    print('-z'*100)
    print(client_img)



    # 載入並處理圖像
    image = cv2.imread(f"./recv_img/uploaded_{client_img}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 圖像縮放處理
    in_img, scale = ratioresize(image_rgb)
    in_img = in_img / 255.0 - 0.5
    in_img = np.transpose(in_img, (2, 0, 1))  # CHW
    in_img = np.expand_dims(in_img, axis=0).astype(np.float32) # 輸入不會量化float32

    # 模型推理
    output = onnx_model.run(None, {'images': in_img})
    results = output[0][0]

    # 分數篩選門檻 必須>0.25
    # print(results.shape)
    # print(results)
    boxes = np.array([i for i in results if i[4] > 0.25])

    # print(boxes.shape)
    # print(boxes)

    ##座標縮放轉乘int32就好 分數和class不變
    # boxes = (boxes * scale).astype(np.int32)
    # [[179  38 292 145   0  45]
    #  [122 146 233 186   0  48]
    #  [ 13 282 167 471   0  41]
    #  [283 117 323 169   0  42]]

    # print('-' * 200)
    # print(boxes)
    for box in boxes:
        # print(box)
        ##座標要轉乘int32
        x1, y1, x2, y2 = (box[:4] * scale).astype(np.int32)
        ##分數以及class_id
        conf = box[4]
        class_id = int(box[5])
        class_name = f"Class {class_id}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)

        label = f"{class_name} ({conf * 100:.2f}%)"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(f"./detect_img_onnx/detect_{client_img}", image)

@app.get("/")
def hello_world():
    return "Hello World"


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 讀取圖片並保存
        with open(f"./recv_img/uploaded_{file.filename}", "wb") as buffer:
            buffer.write(await file.read())

        start_time = time.time()

        ##使用轉成onnx的yolov10辨識
        onnx_dectect(file.filename)


        end_time = time.time()
        # 計算速度
        speed = 1 / (end_time - start_time)
        print(speed)

        # 圖片轉成base64
        with open(f"./detect_img_onnx/detect_{file.filename}", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # 返回JSON响应
        return JSONResponse(
            status_code=200,
            content={
                "speed(second)": speed,
                "filename": file.filename,
                "message": encoded_string
            }
        )

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)