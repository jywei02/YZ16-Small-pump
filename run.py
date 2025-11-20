import time

from YZ16_300 import YZ16Pump

pump = YZ16Pump("COM11")
pump.CW()
pump.setRPM(100)   # 1–600rpm
pump.start()
# 启动泵
pump.start()
print("小泵已启动，输入 'q' 并回车以停止...")

try:
    while True:
        user_input = input()
        if user_input.strip().lower() == 'q':
            break
        else:
            print("请输入 'q' 停止运行。")
except KeyboardInterrupt:
    print("\n用户中断操作")

# 停止泵
pump.stop()
print("小泵已停止")
'''
from YZ16pump import YZ16Pump

# 初始化串口和泵
pump = YZ16Pump("COM11")  # 修改为你实际使用的端口

# 准备控制
pump.unlock()
time.sleep(0.2)
pump.lock()
time.sleep(0.2)

# 设置运行方向和转速
pump.CW()          # 顺时针旋转，可改为 pump.CCW()
time.sleep(0.2)
pump.setRPM(100)    # 设置转速为 90，可根据需要调整
time.sleep(0.2)

# 启动泵
pump.start()
print("小泵已启动，输入 'q' 并回车以停止...")

try:
    while True:
        user_input = input()
        if user_input.strip().lower() == 'q':
            break
        else:
            print("请输入 'q' 停止运行。")
except KeyboardInterrupt:
    print("\n用户中断操作")

# 停止泵
pump.stop()
print("小泵已停止")
'''