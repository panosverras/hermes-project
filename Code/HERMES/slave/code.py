""" Loading libraries/modules -------------------------------- """
from time import sleep
from adafruit_motor import motor
import adafruit_mlx90640
import adafruit_gps
import adafruit_bno055
import neopixel
import board, digitalio, analogio, pwmio, busio, asyncio, time
# -------------------------------------------------------------- #

""" Initialising sensors/modules ----------------------------- """

# IIC sensors -------------------------------------------------- #
i2c = busio.I2C(board.GP9, board.GP8)
bno055 = adafruit_bno055.BNO055_I2C(i2c)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
gps_iic = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
gps_iic.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps_iic.send_command(b"PMTK220,1000")
# -------------------------------------------------------------- #

# UART communication ------------------------------------------- #
pico = busio.UART(board.GP4, board.GP5)
# -------------------------------------------------------------- #

# Analog sensors ----------------------------------------------- #
ultrasonic_r = analogio.AnalogIn(board.A0) #GP26
ultrasonic_l = analogio.AnalogIn(board.A1) #GP27
ultrasonic_f = analogio.AnalogIn(board.A2) #GP28
# -------------------------------------------------------------- #

# Neopixel ----------------------------------------------------- #
pixels_pin = board.GP19
pixels_num = 40
pixels = neopixel.NeoPixel(pixels_pin, pixels_num)

pixel_colors = {
    'yellow': (255, 140, 0),
    'blue': (0, 0, 150),
    'white': (150, 150, 150),
    'red': (150, 0, 0),
    'off':(0, 0, 0)
    }
# -------------------------------------------------------------- #

# Thrusters ---------------------------------------------------- #
# PWM ---------------------------------------------------------- #
in1 = pwmio.PWMOut(board.GP0, frequency=50)
in2 = pwmio.PWMOut(board.GP1, frequency=50)
in3 = pwmio.PWMOut(board.GP2, frequency=50)
in4 = pwmio.PWMOut(board.GP3, frequency=50)

motor_a = motor.DCMotor(in1, in2)
motor_b = motor.DCMotor(in3, in4)
# ------------------------------------------------------------- #

""" Helper methods ------------------------------------------ """

async def signal(mc, color=pixel_colors["white"]):
    dot_lenght = 0.25
    dash_lenght = (dot_lenght * 3)
    morse_codes = {
        "K": ("-.-"), #I wish to communicate with you
        "L": (".-.."), #You should stop your vessel instantly
        "U": ("..-"), #You are running into danger
        "CB": ("-.-. -..."), #I require immediate assistance
        "IL": (".. ._.."), #I can only proceed at slow speed
        "FO": (".._. ---"), #I will keep close to you
        "NG": ("-. __."), #You are in a dangerous position
        "SOS": ("... --- ..."), #Save Our Ship
    }

    if mc in morse_codes:
        for e in morse_codes[mc]:
            for _ in range(0,15,2):
                pixels[_] = pixel_colors['yellow']
            if e == '.':
                await asyncio.sleep(dot_lenght)
            else:
                await asyncio.sleep(dash_lenght)
            for _ in range(0,40):
                if _ != 20:
                    pixels[_] = pixel_colors["off"]
            await asyncio.sleep(dot_lenght)
            await teeth([20,], pixel_colors["blue"])
        for e in morse_codes[mc]:
            for _ in range(24,40,2):
                pixels[_] = pixel_colors['yellow']
            if e == '.':
                await asyncio.sleep(dot_lenght)
            else:
                await asyncio.sleep(dash_lenght)
            for _ in range(0,40):
                if _ != 20:
                    pixels[_] = pixel_colors["off"]
            await asyncio.sleep(dot_lenght)
            await teeth([20,], pixel_colors["blue"])
        return True
    else:
        return False


async def teeth(t, c):
    pixels.fill(pixel_colors["off"])
    for tooth in t:
        pixels[tooth] = c


async def analog_to_cm(side):
    old_range = (8000 - 46000)
    new_range = (150 - 20)
    if side == "f":
        r = (((ultrasonic_f.value - 46000) * new_range) / old_range) + 20
    elif side == "r":
        r = (((ultrasonic_r.value - 46000) * new_range) / old_range) + 20
    elif side == "l":
        r = (((ultrasonic_l.value - 46000) * new_range) / old_range) + 20
    else:
        r = "unknown side"
    return round(r, 1)


async def thruster(motor, direction, speed=1.0):
    if motor == "R":
        if direction == "r":
            motor_a.throttle = speed
            await asyncio.sleep(0.3)
            motor_b.throttle = speed
        elif direction == "l":
            motor_a.throttle = -speed
            await asyncio.sleep(0.3)
            motor_b.throttle = -speed
        else:
            motor_a.throttle = 0.0
    elif motor == "L":
        if direction == "r":
            motor_b.throttle = speed
            await asyncio.sleep(0.3)
            motor_a.throttle = speed
        elif direction == "l":
            motor_b.throttle = -speed
            await asyncio.sleep(0.3)
            motor_a.throttle = -speed
        else:
            motor_b.throttle = 0.0


async def turn(target_orientation):
    if target_orientation in range(0,360):
        current_orientation = bno055.euler[0]
        angular_distance = ((target_orientation - current_orientation + 540)% 360)-180
        if angular_distance > 20:
            await thruster("R","r", 0.1)
        elif angular_distance < -20:
            await thruster("L","r", 0.1)
        while abs(angular_distance) > 20:
            current_orientation = bno055.euler[0]
            angular_distance = ((target_orientation - current_orientation + 540)% 360)-180
            await asyncio.sleep(0.1)
        await thruster("R","s")
        await thruster("L","s")
        return True
    else:
        return False


async def forward(wait, speed=0.1):
    motor_a.throttle = speed
    await asyncio.sleep(0.3)
    motor_b.throttle = -speed
    await asyncio.sleep(wait)
    motor_a.throttle = 0
    motor_b.throttle = 0


async def gps(msg):
    gps_iic.update()
    if gps_iic.has_fix:
        if msg == "lat":
            r = gps_iic.latitude
        elif msg == "lon":
            r = gps_iic.longitude
        elif msg == "head":
            r = gps_iic.track_angle_deg
    else:
        if msg == "head":
            r = bno055.euler[0]
        else:
            r = "NO FIX"
    return r


async def camera():
    frame = [0] * 768
    count = 0
    try:
        mlx.getFrame(frame)
    except ValueError as e:
        print(e)
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            if t > 30:
                count += 1
    print(count)
    if count > 300:
        r = "Object found\n"
    else:
        r = "Everything ok\n"
    return r


async def pico_t(msg):
    pico.write(msg.encode())


async def pico_r():
    responce = pico.read(32)
    s = responce.decode().strip()
    print(s)

    if s.find(':')>-1:
        command, value =  s.split(":")
        #print("command: <{}>, value: <{}>".format(command, value))
        if command == "s":
            if await signal(value):
                await pico_t("signal() OK\n")
            else:
                await pico_t("unknown signal()\n")
        elif command == "t":
            if await turn(int(value)):
                await pico_t("turn() OK\n")
            else:
                await pico_t("unknown head()\n")
        elif command == "g":
            await asyncio.sleep(0.5)
            await pico_t(str(await gps(value)))
        elif command == "d":
            await pico_t(str(await analog_to_cm(value)))
            #await pico_t("100.0")
        elif command == "f":
            await forward(int(value))
            await pico_t("forward() OK\n")
        else:
            await pico_t("unknown command\n")
    else:
        if s == "c":
            await pico_t(await camera())


async def main():
    try:
        await teeth([20,], pixel_colors["blue"])
        while True:
            if pico.in_waiting > 0:
                await pico_r()
    except Exception as e:
        print(e)
        await teeth([16, 18, 20, 22], pixel_colors["red"])
        await asyncio.sleep(5)
# -------------------------------------------------------------- #


# Main loop ---------------------------------------------------- #
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
