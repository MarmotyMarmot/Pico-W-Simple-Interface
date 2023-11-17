from gc import collect
from time import sleep_ms, time, localtime

from machine import Pin, ADC, reset

from dispinch3 import LCD_1inch3


def set_time():
    try:
        from ntptime import settime
        settime()
        del settime
        return 1
    except OSError as ntpError:
        print(ntpError)
        from quicktools import logger
        logger(f"{ntpError}\n")
        del logger
        return 0


def get_time(t: tuple = localtime(time())):
    return f"{t[3]}:{t[4]}:{t[5]}"


if __name__ == '__main__':
    # set onboard LED pin
    onboard_led = Pin("LED", Pin.OUT)
    onboard_led.high()
    # connect to network
    from networktools import connect_to_network, get_external_data
    connect_to_network()
    # set time
    while not set_time():
        onboard_led.low()
        sleep_ms(10)
        onboard_led.high()

    # get data from the internet (through API)
    external_data = get_external_data()
    del connect_to_network, get_external_data
    collect()
    # make instance of LCD object
    LCD = LCD_1inch3()

    # set pinout for the keys and joystick
    keyA = Pin(15, Pin.IN, Pin.PULL_UP)
    keyB = Pin(17, Pin.IN, Pin.PULL_UP)
    keyX = Pin(19, Pin.IN, Pin.PULL_UP)
    keyY = Pin(21, Pin.IN, Pin.PULL_UP)

    up = Pin(2, Pin.IN, Pin.PULL_UP)
    down = Pin(18, Pin.IN, Pin.PULL_UP)
    left = Pin(16, Pin.IN, Pin.PULL_UP)
    right = Pin(20, Pin.IN, Pin.PULL_UP)
    ctrl = Pin(3, Pin.IN, Pin.PULL_UP)

    # set onboard temperature sensor
    temp_sens = ADC(4)

    from displaymanager import display

    # initialize display object
    disp = display(LCD, temp_sens, external_data)

    del display
    # make some colors
    purple = 0x10e0
    cyan = 0x1f0f
    red = 0x10f0
    black = 0x0000

    onboard_led.low()
    disp.refresh_all()
    
    last_interaction = time()
    disp_is_off = 0
    
    def int_A_handler(pin):
        disp.change_screen(1)
        disp.refresh_all()
        
        global last_interaction
        global disp_is_off
        disp_is_off = 0
        last_interaction = time()
    
    def int_B_handler(pin):
        disp.change_screen(2)
        disp.refresh_all()
        
        global last_interaction
        global disp_is_off
        disp_is_off = 0
        last_interaction = time()
    
    def int_X_handler(pin):
        disp.change_screen(3)
        disp.refresh_all()
        
        global last_interaction
        global disp_is_off
        disp_is_off = 0
        last_interaction = time()
    
    def int_Y_handler(pin):
        disp.change_screen(4)
        disp.refresh_all()
        
        global last_interaction
        global disp_is_off
        disp_is_off = 0
        last_interaction = time()
        
    keyA.irq(trigger=Pin.IRQ_RISING, handler=int_A_handler)
    keyB.irq(trigger=Pin.IRQ_RISING, handler=int_B_handler)
    keyX.irq(trigger=Pin.IRQ_RISING, handler=int_X_handler)
    keyY.irq(trigger=Pin.IRQ_RISING, handler=int_Y_handler)
    
    from quicktools import del_logs
    from quicktools import logger
    
    while True:
        # collect garbage
        collect()
        sleep_ms(10)

        try:
            sleep_ms(10)
            
            if (time() - last_interaction > 60 * 5) and (disp_is_off == 0):
                LCD.fill(black)
                LCD.show()
                disp_is_off = 1
                
            if time() - external_data['boot time'] >= 60 * 60:
                del_logs()
                LCD.fill(black)
                reset()
        except ValueError as err:
            logger(f"{err} {time()}\n")
            print(err)
            disp.just_display(["ERROR OCCURED", "PLEASE REBOOT"], black, red)
