import smbus, math
from time import sleep
bus = smbus.SMBus(0)
bus.write_byte_data(0x20, 0x07, 0x00)
bus.write_byte_data(0x20, 0x06, 0xff)
bus.write_byte_data(0x20, 0x01, 0xff)
sleep(0.5)
i = 0
while i < 8:
    n = 0
    sleep(0.1)
    while True:
        n += 1 
        aktiv = (n > 100+5*i)
        bus.write_byte_data(0x20, 0x01, int(math.pow(2, i))-1 + (int(math.pow(2,i)) if aktiv else 0))
        s = ((bus.read_byte_data(0x20, 0x08) & 0x80) > 0)
        if s and aktiv:
            i += 1
            n = 0
            break
        if s and not aktiv:
            i = 0
            n = 0
            break
        if n > (200-10*i): n = 0
        sleep(0.01)
