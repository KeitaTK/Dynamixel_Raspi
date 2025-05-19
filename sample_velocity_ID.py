import dynamixel_classes_for_Raspi as dyna
import time

try:
    motor_id = 1  # ここに制御したいDynamixelのIDを指定
    port = "/dev/ttyUSB0"  # シリアルポート名を設定

    dxl = dyna.Dynamixel(port, 57600)  # インスタンス化

    dxl.set_mode_velocity(motor_id)  # 速度制御モードに設定
    max_1 = 250
    dxl.set_max_velocity(motor_id, max_1)  # 速度の上限を設定
    dxl.enable_torque(motor_id)  # トルクをオンにする

    goal_velocity = 250  # 適当な回転速度を設定
    dxl.write_velocity(motor_id, goal_velocity)  # モーターを回転させる

    print("モーターを10秒間回転させます")
    time.sleep(10)  # 10秒間待機

    dxl.write_velocity(motor_id, 0)  # モーターを停止

except KeyboardInterrupt:  # Ctrl+Cが押されたら
    dxl.disable_torque(motor_id)  # トルクをオフ
    dxl.close_port()  # ポートを切断
