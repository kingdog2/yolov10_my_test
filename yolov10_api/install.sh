#!/bin/bash

# 顯示開始安裝訊息
echo "=== 開始安裝專案依賴 ==="

# 檢查 Python 版本（需 Python 3.10 以上）
PYTHON_VERSION=$(python3 -V 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

# 解析主版本號和次版本號
MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

# 確保 Python 版本 >= 3.10
if [[ "$MAJOR" -lt 3 ]] || [[ "$MAJOR" -eq 3 && "$MINOR" -lt 10 ]]; then
    echo "錯誤：需要 Python 3.10 或以上版本，當前版本為 $PYTHON_VERSION"
    exit 1
fi

# 建立虛擬環境（如果不存在）
if [ ! -d "venv" ]; then
    echo "創建虛擬環境..."
    python3 -m venv venv
fi

# 啟動虛擬環境
echo "啟動虛擬環境..."
source venv/bin/activate

# 升級 pip（保持 pip 最新）
echo "升級 pip..."
pip install --upgrade pip

# 安裝 requirements.txt 中的所有依賴
echo "安裝專案依賴..."
pip install -r requirements.txt

# 完成訊息
echo "=== 安裝完成！你現在可以開始使用專案 ==="

# 退出腳本
exit 0
