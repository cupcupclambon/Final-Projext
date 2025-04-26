import threading
import board
import adafruit_lsm9ds1
import average
import math
import pigpio  # サーボモータ制御用

# サーボモータ制御用のピン設定
SERVO_PIN = 18  # GPIO 18
pi = pigpio.pi()  # pigpioを初期化

if not pi.connected:
    exit()

i2c = board.I2C()
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

# サーボモータを動かす関数
def move_servo_based_on_angle(angle):
    # 角度をパルス幅（500～2500の範囲）に変換
    pulsewidth = 500 + ((angle + 90) / 180) * 2000
    pulsewidth = max(500, min(2500, pulsewidth))  # パルス幅の範囲制限
    pi.set_servo_pulsewidth(SERVO_PIN, pulsewidth)

# 更新スレッド作成
def startThread():
    # センサーから加速度を取得し、Y軸の角度を元にサーボモータを動かす
    aveNum = 100
    accs = [average.MoveAverage(aveNum), average.MoveAverage(aveNum), average.MoveAverage(aveNum)]
    while True:
        vals = tuple(sensor.acceleration)
        accX = accs[0].add(vals[0])
        accY = accs[1].add(vals[1])
        accZ = accs[2].add(vals[2])

        # Y軸傾斜角度を算出
        gravLen = math.sqrt(accX ** 2 + accY ** 2 + accZ ** 2)  # 重力加速度の絶対値
        sinViaVerticalY = accY / gravLen
        degY = math.degrees(math.asin(sinViaVerticalY))

        # Y軸の傾きに応じてサーボを動かす
        move_servo_based_on_angle(degY)

thread = threading.Thread(target=startThread, daemon=True)
thread.start()

# プログラム終了時にサーボを停止
try:
    while True:
        pass  # サーボの制御はスレッド内で実行中
except KeyboardInterrupt:
    pass  # Ctrl+Cで終了

# サーボを停止
pi.set_servo_pulsewidth(SERVO_PIN, 0)
pi.stop()

