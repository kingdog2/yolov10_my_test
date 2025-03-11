# python 3.10 pytorch-cuda126 python 3.10
import random

from ultralytics import YOLOv10
import cv2

model = YOLOv10.from_pretrained('jameslahm/yolov10n')

source = 'aa.jpg'
img = cv2.imread(source)

results = model.predict(source=source, save=True)
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

cv2.imshow("YOLOv10 Detection", img)
cv2.waitKey(0)  # 按任意鍵關閉
cv2.destroyAllWindows()

cv2.imwrite("output.jpg", img)
print("標註結果已儲存為 output.jpg")
