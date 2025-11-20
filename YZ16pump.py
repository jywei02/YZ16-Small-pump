import minimalmodbus
import time


class YZ16Pump:
    def __init__(self, port: str, slave_address: int = 1):
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        self.instrument.serial.baudrate = 38400
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
        self.instrument.serial.bytesize = 8
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 1
        self.instrument.mode = minimalmodbus.MODE_RTU
        time.sleep(1)

    def unlock(self):
        """Allow remote control by unlocking the pump."""
        self.instrument.write_register(0x00, 0x0000, functioncode=16)
        time.sleep(0.1)

    def lock(self):
        """Lock control (enable remote control)."""
        self.instrument.write_register(0x00, 0xFF00, functioncode=16)
        time.sleep(0.1)

    def CW(self):
        """Set pump direction to Clockwise."""
        # self.lock()
        self.unlock()
        time.sleep(0.2)

        self.lock()
        time.sleep(0.2)

        self.instrument.write_register(0x02, 0x0000, functioncode=16)
        time.sleep(0.1)

    def CCW(self):
        """Set pump direction to Counter-clockwise."""
        # self.lock()
        self.unlock()
        time.sleep(0.2)

        self.lock()
        time.sleep(0.2)

        self.instrument.write_register(0x02, 0xFF00, functioncode=16)
        time.sleep(0.1)


    def setRPM(self, rpm: float):
        """Set speed in RPM (1–100)."""
        if not (1 <= rpm <= 100):
            raise ValueError(f'RPM must be between 1 and 100. Got: {rpm}')
        self.instrument.write_register(0x03, rpm, functioncode=6)
        time.sleep(0.1)


    def start(self):
        """Start the pump motor."""
        self.instrument.write_register(0x01, 0xFF00, functioncode=6)
        time.sleep(0.1)

    def stop(self):
        """Stop the pump motor."""
        try:
            self.instrument.write_register(0x01, 0x0000, functioncode=6)
            time.sleep(0.1)
        except minimalmodbus.InvalidResponseError as e:
            if "Wrong write data" in str(e):
                print("Pump is stopping...")
            else:
                raise

    def read_status(self):
        """Print debug information for current pump state."""
        status = {
            "Lock": self.instrument.read_register(0x00),
            "Start/Stop": self.instrument.read_register(0x01),
            "Direction": self.instrument.read_register(0x02),
            "RPM": self.instrument.read_register(0x03),
        }
        print("Pump Status:")
        for k, v in status.items():
            print(f"  {k}: {v}")
        return status


# Example Usage
if __name__ == '__main__':
    pump = YZ16Pump("COM14")  # Use the updated class we built earlier

    pump.unlock()
    time.sleep(0.2)

    pump.lock()
    time.sleep(0.2)

    pump.CW()  # or pump.CCW()
    time.sleep(0.2)

    pump.setRPM(20)
    time.sleep(0.2)

    pump.start()
    time.sleep(5)

    pump.setRPM(70)
    time.sleep(5)

    pump.stop()
