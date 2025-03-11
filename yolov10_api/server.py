# 運行 API
# netstat -ano | findstr :8000d
# curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@C:/Users/f2201/Downloads/yolov10_api/aa.jpg"
import time
import base64
from fastapi import FastAPI, File, UploadFile
from starlette.responses import JSONResponse
import random
from ultralytics import YOLOv10
import cv2
model = YOLOv10.from_pretrained('jameslahm/yolov10n')


app = FastAPI()
print("="*200)

@app.get("/")
def hello_world():
    return "Hello World"


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # print(1111111111)
    try:
        # 讀取圖片並保存
        with open(f"./recv_img/uploaded_{file.filename}", "wb") as buffer:
            buffer.write(await file.read())

        start_time = time.time()

        ##1
        # results = model.predict(source=f"./recv_img/uploaded_{file.filename}", save_dir='./save')#save=True)
        ##2
        img = cv2.imread(f"./recv_img/uploaded_{file.filename}")
        results = model.predict(source=f"./recv_img/uploaded_{file.filename}", save=True)
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

                label = f"Class {cls}: {conf:.2f}"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        cv2.imwrite(f"./detect_img/detect_{file.filename}", img)
        cv2.destroyAllWindows()
        end_time = time.time()
        # 計算速度
        speed = 1 / (end_time - start_time)
        print(speed)

        # 圖片轉成base64
        with open(f"./detect_img/detect_{file.filename}", "rb") as image_file:
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