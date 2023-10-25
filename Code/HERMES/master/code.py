# Loading libraries/modules ------------------------------------ #

from time import sleep
import asyncio
import adafruit_ds18x20, digitalio, adafruit_mlx90640
from adafruit_onewire.bus import OneWireBus
import board, busio, adafruit_bme680, adafruit_tsl2591, analogio
import circuitpython_dfrobot_gravity_drf0627_dual_uart as DualUart
# -------------------------------------------------------------- #

# Initialising sensors/modules --------------------------------- #

# IIC sensors -------------------------------------------------- #
i2c = busio.I2C(board.GP5, board.GP4)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
tsl = adafruit_tsl2591.TSL2591(i2c)
# -------------------------------------------------------------- #

# UART communication ------------------------------------------- #
pico = busio.UART(board.GP0, board.GP1)

hc12_air_out_uart = DualUart.DFRobot_IIC_Serial(i2c, sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_1, IA1=1, IA0=1) #yellow
hc12_air_in_uart = DualUart.DFRobot_IIC_Serial(i2c, sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_2, IA1=1, IA0=1) #red
hc12_sea_out_uart = DualUart.DFRobot_IIC_Serial(i2c, sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_1, IA1=0, IA0=1) #green
hc12_sea_in_uart = DualUart.DFRobot_IIC_Serial(i2c, sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_2, IA1=0, IA0=1) #blue

hc12_air_out_uart.begin(9600, hc12_air_out_uart.IIC_Serial_8N1)
hc12_air_in_uart.begin(9600, hc12_air_in_uart.IIC_Serial_8N1)
hc12_sea_out_uart.begin(9600, hc12_sea_out_uart.IIC_Serial_8N1)
hc12_sea_in_uart.begin(9600, hc12_sea_in_uart.IIC_Serial_8N1)

hc12_air_out_set = digitalio.DigitalInOut(board.GP3)
hc12_air_in_set = digitalio.DigitalInOut(board.GP12)
hc12_sea_out_set = digitalio.DigitalInOut(board.GP13)
hc12_sea_in_set = digitalio.DigitalInOut(board.GP14)

hc12_air_out_set.direction = digitalio.Direction.OUTPUT
hc12_air_in_set.direction = digitalio.Direction.OUTPUT
hc12_sea_out_set.direction = digitalio.Direction.OUTPUT
hc12_sea_in_set.direction = digitalio.Direction.OUTPUT

ph_pin = DualUart.DFRobot_IIC_Serial(i2c, sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_1, IA1=1, IA0=0)
cond_pin = DualUart.DFRobot_IIC_Serial(i2c, sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_2, IA1=1, IA0=0)
ph_pin.begin(9600, ph_pin.IIC_Serial_8N1)
cond_pin.begin(9600, cond_pin.IIC_Serial_8N1)
# -------------------------------------------------------------- #

# Analog sensors ----------------------------------------------- #
mq135 = analogio.AnalogIn(board.A0) #GP26
ultrasonic = analogio.AnalogIn(board.A2)
# -------------------------------------------------------------- #

# OneWire sensor ----------------------------------------------- #
ow_bus = OneWireBus(board.GP2)
ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, ow_bus.scan()[0])
# -------------------------------------------------------------- #


""" Helper methods ------------------------------------------- """

async def get_data():
    data = "\n----------------------------------------\nTemperature: {} °C\nWater temperature: {} °C\nHumidity: {}%\n".format(round(bme680.temperature,1),round(ds18b20.temperature,1), round(bme680.humidity))
    await hc12_sea_out(data)

async def mq135_ppm(sensor_value, scale = True):
    ppm = round(sensor_value * (1000/65535), 2)
    if scale == True:
        if ppm < 700:
           quality = "Excellent"
        elif ppm >= 600 and ppm < 800:
           quality = "Good"
        elif ppm >= 800 and ppm < 1100:
            quality = "Poor"
        elif ppm >= 1100 and ppm < 1500:
            quality = "Unhealthy"
        elif ppm >= 1500 and ppm < 2000:
            quality = "Very unhealthy"
        elif ppm >= 2000 and ppm < 3000:
            quality = "Hazardous"
        elif ppm >= 3000:
            quality = "Extreme"
        r = [ppm, quality]
        return r
    else:
        return ppm

async def ph(scale=True):
    ph_pin.write("R\r")
    value = ph_pin.read(32)
    x = ""
    for _ in value:
        x += chr(_)
    ph_value = x.split("*")
    if scale == True:
            if ph_value[0] < 2.0:
               quality = "Extremely Acidic"
            elif ph_value[0] >= 2.0 and ph_value[0] < 4.0:
               quality = "Acidic"
            elif ph_value[0] >= 4.0 and ph_value[0] < 6.0:
                quality = "Slightly Acidic"
            elif ph_value[0] >= 6.0 and ph_value[0] < 8.0:
                quality = "Normal"
            elif ph_value[0] >= 8.0 and ph_value[0] < 10.0:
                quality = "Slightly Basic"
            elif ph_value[0] >= 10.0 and ph_value[0] < 12.0:
                quality = "Basic"
            elif ph_value[0] >= 12.0:
                quality = "Extremely Basic"
            r = [ph_value[0], quality]
            return r
    else:
        return ph_value[0]


async def conductivity():
    cond_pin.write("R\r")
    value = cond_pin.read(32)
    r = ""
    for _ in value:
        r += chr(_)
    responce = r.split("*")
    return responce[0]


async def getter(t):
    r = "UNKNOWN COMMAND\n"
    if t.find(':')>-1:
        command, value =  t.split(":")
        #print("command: <{}>, value: <{}>".format(command, value))
        if command == "dist":
            await pico_t("d:{}".format(value))
            await asyncio.sleep(1)
            v = await pico_r()
            r = v.decode()
        elif command == "f":
            await pico_t("f:{}".format(value))
            await asyncio.sleep(1)
            v = await pico_r()
            r = v.decode()
        elif command == "turn":
            await pico_t("t:{}".format(value))
            v = await pico_r()
            r = v.decode()
        elif command == "s":
            await pico_t("s:{}".format(value))
            await asyncio.sleep(1)
            v = await pico_r()
            r = v.decode()
    else:
        if t == "temp":
            v = await get_value(t)
            r = "Temperature: {} °C\n".format(v)
        elif t == "wtemp":
            v = await get_value(t)
            r = "Water temperature: {} °C\n".format(v)
        elif t == "gas":
            v = await get_value(t)
            r = "Gas: {} ppm, {} quality\n".format(v[0], v[1])
        elif t == "hum":
            v = await get_value(t)
            r = "Humidity: {} %\n".format(v)
        elif t == "prs":
            v = await get_value(t)
            r = "Pressure: {} Pa\n".format(v)
        elif t == "irl":
            v = await get_value(t)
            r = "Infrared Light: {}\n".format(v)
        elif t == "vsl":
            v = await get_value(t)
            r = "Visible Light: {}\n".format(v)
        elif t == "ph":
            v = await get_value(t)
            r = "Ph: {}\n".format(v)
        elif t == "cond":
            v = await get_value(t)
            r = "Conductivity: {} μS\n".format(v)
        elif t == "head":
            await pico_t("g:{}".format(t))
            v = await pico_r()
            r = "Heading: {}°\n".format(v.decode())
        elif t == "lon":
            await pico_t("g:{}".format(t))
            await asyncio.sleep(0.5)
            v = await pico_r()
            if v.decode() != "NO FIX":
                r = "Longitude: {}\n".format(v.decode())
            else:
                r = "gps: {}\n".format(v.decode())
        elif t == "lat":
            await pico_t("g:{}".format(t))
            v = await pico_r()
            if v.decode() != "NO FIX":
                r = "Latitude: {}\n".format(v.decode())
            else:
                r = "gps: {}".format(v.decode())
        elif t == "camera":
            await pico_t("c")
            await asyncio.sleep(2)
            v = await pico_r()
            r = v.decode()
    return r


async def get_value(s, scale=True):
    if s == "gas":
        r = await mq135_ppm(mq135.value, scale)
    elif s == "temp":
        r = round(bme680.temperature, 1)
    elif s == "wtemp":
        r = round(ds18b20.temperature, 1)
    elif s == "irl":
        r = tsl.infrared
    elif s == "vsl":
        r = tsl.visible
    elif s == "ph":
        r = await ph()
    elif s == "cond":
        r = await conductivity()
    elif s == "hum":
        r = round(bme680.humidity)
    elif s == "prs":
        r = round(bme680.pressure)
    else:
        r = "unknown sensor"
    return r


async def command(msg):
    if msg.startswith("#"):
        return True
    else:
        return False


async def commander(msg):
    msg_split = msg.split("#")
    splitted_msg = msg_split[1].split("\r\n")
    print(splitted_msg)
    r = await getter(splitted_msg[0])
    return r


async def pico_t(msg):
    # command format: command:value
    #   turn -> turn(), s -> signal()
    #   e.g "turn:90" or "s:SOS"
    pico.write(msg.encode())


async def pico_r():
    responce = pico.read(32)
    print(responce.decode())
    return responce


async def hc12_air_out(m):
    hc12_air_out_uart.write(m)


async def hc12_air_in():
    await asyncio.sleep(0.1)
    r = hc12_air_in_uart.read(32)
    responce = ""
    for _ in r:
        responce += chr(_)
    return responce


async def hc12_sea_out(m):
    hc12_sea_out_uart.write(m)


async def hc12_sea_in():
    await asyncio.sleep(0.1)
    r = hc12_sea_in_uart.read(32)
    responce = ""
    for _ in r:
        responce += chr(_)
    return responce


async def hc12_set(pin, uart, frequency):
    pin.value = False
    await asyncio.sleep(0.1)
    uart.write("AT+{}\r\n".format(frequency))
    sleep(0.1)
    value = uart.read(32)
    r = ""
    for _ in value:
        r += chr(_)
    print(r)
    pin.value = True
    await asyncio.sleep(0.1)


async def main():
    await hc12_set(hc12_air_out_set, hc12_air_out_uart, "C022")
    await hc12_set(hc12_air_in_set, hc12_air_in_uart, "C027")
    await hc12_set(hc12_sea_out_set, hc12_sea_out_uart, "C032")
    await hc12_set(hc12_sea_in_set, hc12_sea_in_uart, "C037")
    await get_data()

    while True:
        try:
            if hc12_air_in_uart.available():
                while hc12_air_in_uart.available():
                    message = await hc12_air_in()
                    print(message)

                    if await command(message):
                        m = await commander(message)
                        await hc12_air_out(m)
                    else:
                        print("Air input")
                        await hc12_sea_out(message)

            if hc12_sea_in_uart.available():
                message = await hc12_sea_in()
                print(message)

                if await command(message):
                    m = await commander(message)
                    await hc12_sea_out(m)
                else:
                    print("Sea input")
                    await hc12_air_out(message)

        except Exception as e:
            print(e)
            await asyncio.sleep(3)
# -------------------------------------------------------------- #

""" Main loop ------------------------------------------------ """

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
