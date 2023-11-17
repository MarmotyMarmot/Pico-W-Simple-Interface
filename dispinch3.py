from machine import Pin, SPI, PWM
from time import time, sleep_ms
import framebuf


def make_buffer(filename, w, h):
    """making buffer from  .raw file, so it can be displayed on a display, don't use for big files, it has memory
    problem which SHOULD BE FIXED (PROBABLY CHANGE OF A WHOLE LIB, CAUSE IT TAKES TOO MUCH FLASH)"""
    display_buffer = bytearray(w * h * 2)
    with open(filename, "rb", buffering=1) as file:
        position = 0
        while position < (w * h * 2):
            current_byte = file.read(1)
            # if eof
            if len(current_byte) == 0:
                break
            # copy to buffer
            display_buffer[position] = ord(current_byte)
            position += 1
    file.close()
    img = framebuf.FrameBuffer(display_buffer, w, h, framebuf.RGB565)
    return img


class LCD_1inch3(framebuf.FrameBuffer):
    """
    Default taken GPIO pins nums :\n
    BL = 13\n
    DC = 8\n
    RST = 12\n
    MOSI = 11\n
    SCK = 10\n
    CS = 9"""

    def __init__(self, BL_pin=13, DC_pin=8, RST_pin=12, MOSI_pin=11, SCK_pin=10, CS_pin=9):
        self.width = 240
        self.height = 240
        self.buffer = 0
        while not self.buffer:
            try:
                self.buffer = bytearray(self.height * self.width * 2)
            except MemoryError as memerr:
                self.buffer = 0
                print(f"{memerr} {time()}")
                sleep_ms(1000)

        self.BL_pin = BL_pin
        self.DC_pin = DC_pin
        self.RST_pin = RST_pin
        self.MOSI_pin = MOSI_pin
        self.SCK_pin = SCK_pin
        self.CS_pin = CS_pin

        self.cs = Pin(self.CS_pin, Pin.OUT)
        self.rst = Pin(self.RST_pin, Pin.OUT)

        self.pwm = PWM(Pin(self.BL_pin))
        self.pwm.freq(1000)
        self.pwm.duty_u16(32768)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 1000_000)
        self.spi = SPI(1, 100000_000, polarity=0, phase=0, sck=Pin(self.SCK_pin), mosi=Pin(self.MOSI_pin), miso=None)
        self.dc = Pin(self.DC_pin, Pin.OUT)
        self.dc(1)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.red = 0x07E0
        self.green = 0x001f
        self.blue = 0xf800
        self.white = 0xffff

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def display_image(self, filename, width, height, pos_x, pos_y):
        buffer = make_buffer(filename, width, height)
        self.blit(buffer, pos_x, pos_y)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
