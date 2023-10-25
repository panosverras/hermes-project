""" Loading libraries/modules -------------------------------- """
from time import sleep
import busio, board, asyncio, digitalio, usb_cdc
# -------------------------------------------------------------- #

""" Initialising sensors/modules ----------------------------- """

hc12_air_out_uart = busio.UART(board.GP0, board.GP1)
hc12_air_in_uart = busio.UART(board.GP4, board.GP5)

hc12_air_out_set = digitalio.DigitalInOut(board.GP2)
hc12_air_in_set = digitalio.DigitalInOut(board.GP3)

hc12_air_in_set.direction = digitalio.Direction.OUTPUT
hc12_air_out_set.direction = digitalio.Direction.OUTPUT

serial = usb_cdc.data
# -------------------------------------------------------------- #

""" Helper methods ------------------------------------------- """

async def hc12_set_pin(pin, uart, frequency):
    pin.value = False
    await asyncio.sleep(0.1)
    uart.write(b"AT+{}\r\n".format(frequency))
    sleep(0.1)
    value = uart.read(32)
    r = ""
    for _ in value:
        r += chr(_)
    print(r)
    pin.value = True
    await asyncio.sleep(0.1)

async def hc12_air_out(msg):
    hc12_air_out_uart.write(msg)

async def hc12_air_in():
    responce = hc12_air_in_uart.read(32)
    return responce

async def serial_out(msg):
    serial.write(msg)

async def serial_in():
    msg = bytearray()
    msg = serial.read(serial.in_waiting)
    return msg

async def main():
    await hc12_set_pin(hc12_air_out_set, hc12_air_out_uart, "C027")
    await hc12_set_pin(hc12_air_in_set, hc12_air_in_uart, "C022")
    while True:
        try:
            message = bytearray()
            if serial.in_waiting > 0:
                message = await serial_in()
                await hc12_air_out(message)
                print(message.decode())

            if hc12_air_in_uart.in_waiting > 0:
                message = await hc12_air_in()
                await serial_out(message)
                print(message.decode())

        except Exception as e:
            print(e)
            sleep(5)
# -------------------------------------------------------------- #

""" Main loop ------------------------------------------------ """

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
