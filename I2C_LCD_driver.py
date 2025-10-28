import smbus
import time

class lcd:
    ADDRESS = 0x27
    LCD_CHR = 1
    LCD_CMD = 0
    LINE_1 = 0x80
    LINE_2 = 0xC0
    ENABLE = 0b00000100

    def __init__(self):
        self.bus = smbus.SMBus(0)
        self.lcd_init()

    def lcd_init(self):
        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)
        time.sleep(0.0005)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | 0x08
        bits_low = mode | ((bits << 4) & 0xF0) | 0x08
        self.bus.write_byte(self.ADDRESS, bits_high)
        self.lcd_toggle_enable(bits_high)
        self.bus.write_byte(self.ADDRESS, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(0.0005)
        self.bus.write_byte(self.ADDRESS, (bits | self.ENABLE))
        time.sleep(0.0005)
        self.bus.write_byte(self.ADDRESS, (bits & ~self.ENABLE))
        time.sleep(0.0005)

    def lcd_display_string(self, message, line):
        if line == 1:
            self.lcd_byte(self.LINE_1, self.LCD_CMD)
        elif line == 2:
            self.lcd_byte(self.LINE_2, self.LCD_CMD)
        for char in message.ljust(16):
            self.lcd_byte(ord(char), self.LCD_CHR)
