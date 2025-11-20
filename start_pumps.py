
import time
from YZ16pump import YZ16Pump

pump = YZ16Pump("COM11")  # Use the updated class we built earlier

pump.unlock()
time.sleep(0.2)

pump.lock()
time.sleep(0.2)

pump.CW()  # or pump.CCW()
time.sleep(0.2)

pump.setRPM(90) # Enter RPM
time.sleep(0.2)

pump.start()
time.sleep(60) # Enter 60 to run 60 seconds

pump.stop()
