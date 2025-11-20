import minimalmodbus
import time
import threading


class YZ16Pump:
    def __init__(self, port: str, slave_address: int = 1):
        # 初始化 Modbus RTU 连接
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        self.instrument.serial.baudrate = 38400
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
        self.instrument.serial.bytesize = 8
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 1
        self.instrument.mode = minimalmodbus.MODE_RTU
        time.sleep(1)

    def enable_remote(self):
        """锁定键盘 (reg0x0000=0xFF00)，允许通过 Modbus 写入参数。"""
        self.instrument.write_register(0x0000, 0xFF00, functioncode=6)
        time.sleep(0.1)

    def disable_remote(self):
        """解锁键盘 (reg0x0000=0x0000)，恢复本地键盘输入。"""
        self.instrument.write_register(0x0000, 0x0000, functioncode=6)
        time.sleep(0.1)

    def CW(self):
        """设置顺时针方向 (reg0x0002=0x0000)。"""
        self.enable_remote()
        self.instrument.write_register(0x0002, 0x0000, functioncode=6)
        time.sleep(0.1)

    def CCW(self):
        """设置逆时针方向 (reg0x0002=0xFF00)。"""
        self.enable_remote()
        self.instrument.write_register(0x0002, 0xFF00, functioncode=6)
        time.sleep(0.1)

    def setRPM(self, rpm: float):
        """设置目标转速 (reg0x0003)，范围 1–600 rpm。使用单寄存器写入功能码 0x06。"""
        if not (1 <= rpm <= 600):
            raise ValueError(f"RPM 必须在 1~600 之间，当前: {rpm}")
        self.enable_remote()
        self.instrument.write_register(0x0003, int(rpm), functioncode=6)
        time.sleep(0.1)

    def start(self):
        """启动泵 (reg0x0001=0xFF00)。"""
        self.enable_remote()
        self.instrument.write_register(0x0001, 0xFF00, functioncode=6)
        time.sleep(0.1)

    def stop(self):
        """停止泵 (reg0x0001=0x0000)。"""
        self.enable_remote()
        self.instrument.write_register(0x0001, 0x0000, functioncode=6)
        time.sleep(0.1)

    def read_rpm(self) -> float:
        """读取当前实时速度 (reg0x0003)，返回 rpm。"""
        return self.instrument.read_register(0x0003, 0, functioncode=3)


if __name__ == '__main__':
    pump_port = 'COM11'  # 根据实际串口号调整
    pump = YZ16Pump(pump_port)

    # 启动流程示例
    pump.CW()            # 顺时针
    pump.setRPM(100)     # 1–600 rpm
    pump.start()         # 开始运行

    # 实时速度监控
    stop_event = threading.Event()
    def monitor(interval=0.5):
        while not stop_event.is_set():
            current = pump.read_rpm()
            print(f'[实际转速]: {current} RPM')
            time.sleep(interval)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()

    input("输入任意键并回车停止运行...\n")
    stop_event.set()
    pump.stop()
    print("泵已停止。")
