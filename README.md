# YOLOv10 物件偵測 API

本專案使用 **YOLOv10 + FastAPI** 建立 Restful API 服務，并透過 ONNX Runtime 進行 GPU 推論，以確保本機環境 **FPS ≥ 10**。  
可用 **client.py** 發送圖片請求，獲得推論結果。

---

## **🚀 1. 安裝與設定**
### **1.1 環境需求**
- Python 3.10+
- GPU (支援 CUDA)  本專案使用CUDA12.6 可自己做版本調整
- 無需對外網路下載模型

### **1.2 安裝套件**
請確保已安裝 **CUDA + cuDNN**，然後執行：
```bash
pip install -r requirements.txt
```

---

## **🚀 2. 使用方法**
### **2.1 啟動 YOLOv10 伺服器**
```bash
python server.py
```
成功啟動後，API 伺服器會運行在 `http://127.0.0.1:8000`。

### **2.2 發送圖片請求**
```bash
python client.py
```
執行後，客戶端會發送圖片至伺服器，接收 YOLOv10 物件偵測結果並下載偵測圖片於客戶端以方便檢查。

---

## **🚀 3. API 規格**
| 方法  | 端點      | 參數               | 回應                |
|-------|-----------|--------------------|---------------------|
| `POST` | `/upload` | `image` (base64 編碼圖片) | 物件偵測結果 JSON    |

### **請求格式（JSON）**
使用以下命令進行請求：
```bash
curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@C:/Users/f2201/Downloads/yolov10_api/aa.jpg"
```

### **回應範例**
成功回應：
```json
{
    "speed(second)": fps,
    "filename": "aa.jpg",
    "message": "encoded_string"
}
```

若出現錯誤，將返回以下格式：
```json
{
    "message": "錯誤訊息"
}
```

### 說明：
- `image` 參數是以 base64 編碼的圖片數據。
- `fps` 代表每秒處理的圖片數（處理速度）。
- `filename` 是圖片的檔名。
- `message` 是經過處理後的物件偵測結果，通常以編碼字串形式返回。

## **🚀 4. 測試圖片**
請將 **圖片 (1280x720)** 放入 `images/` 目錄，並修改 `client.py` 來選擇測試圖片。

---

## **🚀 5. 效能優化**
- **使用 ONNX Runtime GPU** 加速推論。
- **預先載入模型** 以避免記憶體無限增長。
- **使用 FastAPI + Uvicorn** 提供高效能 API。

