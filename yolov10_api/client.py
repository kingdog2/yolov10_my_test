import os
import requests
import base64

def upload_file_yolov10_detect():
    try:
        img = input("請輸入想要yolov10_dete的檔案: ")

        if os.path.exists(img):
            print(f"檔案 {img} 存在")
            if img.endswith(".jpg") or img.endswith(".jpeg"):
                img_type = "image/jpeg"
            elif img.endswith(".png"):
                img_type = "image/png"
            else:
                raise ValueError("並非圖片格式!!!!")
            ##開啟
            with open(img, "rb") as f:
                files = {"file": (img, f, img_type)}
                response = requests.post(url, files=files)
            ##查看回傳狀態碼
            if response.status_code == 200:
                response_data = response.json()
                print(f"接收 {response_data}")
                base64_string = response_data["message"]

                #Base64解碼
                img_data = base64.b64decode(base64_string)

                with open("detect_"+img, "wb") as f:
                    f.write(img_data)

                print(f"存檔成功 detect_{img}")
            else:
                print(f"POST請求失敗: {response.status_code}, {response.text}")
        else:
            print(f"檔案 {img} 不存在或不符合副檔名")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/upload/"
    while True:
        upload_file_yolov10_detect()
