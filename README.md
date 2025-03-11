
# YOLOv10 物件偵測 API

本專案利用 **YOLOv10** 和 **FastAPI** 建立了一個RESTful API 服務能實現Yolov10物件偵測。  
您可以使用 **client.py** 發送圖片請求並獲得物件偵測結果，或使用 **client_loop_fpsCheck.py** 進行持續的 FPS 測試(小心不要讓伺服器爆炸阿!!)。

---

## **🚀 1. 安裝與設定**
### **1.1 環境需求**
- Python 3.10
- 支援 CUDA 的 GPU（本專案使用 CUDA 12.6，您可以根據需要調整版本）

### **1.2 安裝套件**
執行以下命令安裝所需的依賴：
```bash
pip install -r requirements.txt
```
或是
賦予腳本執行權限：
```bash
chmod +x install.sh
```
執行腳本：
```bash
./install.sh
```

然後請確保已安裝 **CUDA + cuDNN**
接著，您可以運行 `check_pytorch_gpu.py` 來確認是否支援 CUDA。

---

## **🚀 2. 使用方法**
### **2.1 啟動 YOLOv10 伺服器**
運行以下命令啟動伺服器：
```bash
python server.py
```
成功啟動後，API 伺服器將在 `http://127.0.0.1:8000` 上運行。

### **2.2 發送圖片請求**
您可以執行以下命令將圖片發送到伺服器：
```bash
python client.py
```
執行後，客戶端將上傳圖片至伺服器，並接收 YOLOv10 的物件偵測結果，下載並儲存偵測過的圖片，方便後續檢查。

---

## **🚀 3. API 規格**
| 方法  | 端點      | 參數               | 回應                |
|-------|-----------|--------------------|---------------------|
| `POST` | `/upload` | `image` (base64 編碼圖片) | 物件偵測結果 JSON    |

### **請求格式（JSON）**
您可以使用以下命令進行請求：
```bash
curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@目錄/yolov10_api/aa.jpg"
```

### **回應範例**
成功回應：
```json
{
    "speed(second)": speed,
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

### 參數說明：
- `image` 參數是以 base64 編碼的圖片數據。
- `speed(second)` 這裡指單張跑yolov10的時間，並非代表每秒處理的圖片數（處理速度）。
- `filename` 是上傳圖片的檔名。
- `message` 是物件偵測後的結果，通常以編碼字串形式返回。

---

## **🚀 4. 效能優化**
- **採用 FastAPI + Uvicorn** 提供高效能的 API 服務。
