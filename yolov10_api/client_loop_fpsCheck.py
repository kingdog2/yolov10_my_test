####按下 'S' 鍵停止程式...!!!!!!!!!!!!!!!
import subprocess
import time

import keyboard
def send_api():
    cmd = 'curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@C:/Users/f2201/Downloads/yolov10_api/aa.jpg"'
    process = subprocess.Popen(cmd, stdout=subproceㄋss.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    stdout, stderr = process.communicate()

    print("輸出結果:", stdout)
    print("錯誤資訊:", stderr)
if __name__ == "__main__":
    print("按下 'S' 鍵停止程式...")
    start_time = time.time()
    frame_num = 0
    bad = 0
    while True:
        if keyboard.is_pressed("s"):  # 監聽 's' 鍵
            print("程序已停止")
            end_time = time.time()
            break

        send_api()
        frame_num+=1
    print(f"總共 {frame_num} 張")
    print(f"經過 {end_time - start_time} 秒")
    print(f"FPS = {frame_num/(end_time - start_time)}")