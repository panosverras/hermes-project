# HERMES project
WRO2023 Future Innovators project (smartbirds team)

![HERMES logo](/images/HERMES-logo.png "HERMES logo")

HERMES is a project created by **smartbirds** team (Greece) for their participation to the World Robot Olympiad^TM^ 2023.
Team consists of 3 high school students, Niobe, Thymios, Faidon and their coach Mr. Panos Verras.

## Why we created HERMES?

![WRO2023 theme - Connecting the World](/images/CONNECTING-THE-WORLD-2023-01-3.png "WRO2023 theme - Connecting the World")

After lots of research on this season’s theme “Connecting the World”, we came to the idea of HERMES, a multifunctional robotic system that maintains a more stable telecommunication network/infrastructure working as single node (p2p) or in combination with other units (HERMES mesh network). HERMES is based on our research on the fields of today’s IT infrastructure, undersea cable networks, socio-economic impact of IT on our daily life, marine traffic, ship design, underwater and overwater scientific and climate data and UN Sustainability Goals.

Since the beginning of time, waterways have played an important role in human communications, linking geographies and societies far and wide. Today, water not only facilitates transportation and trade but also connects nations and continents across the globe through the worldwide system of computer networks. The internet connects over 5 billion people around the world, with an impressive 99% of data being transferred through undersea fiber-optic cables. Damage on the physical underwater infrastructure could cause a multitude of problems due to internet outage, especially in cases of remote areas where an entire community relies on a few cables or even just one.

Every year, the underwater communication network undergoes between 100 and 150 faults. Most of these cable faults occur in water depths shallower than 200 meters, within a distance of approximately 1000 meters from the coastline. The internet downtime period resulting from cable faults depends on weather and climate conditions and it may take up to several months for a complete repair. Moreover, as global overseas shipping continues to grow and thus traffic in shallower waters surges, cable incidents and pollution will only increase, especially in congestion points, such as canals and rivers.

Loss of internet connectivity presents significant challenges for nations, governments and everyday people. However, the complete absence of internet access in remote regions is equally detrimental. Extending internet access to remote areas ultimately gives these communities access to vital resources and services by helping them connect to the rest of the world.

The problems arising from lack of internet access are numerous and complex, so innovative ideas and advanced technologies are the solution. Our project, HERMES, can help.

HERMES is an innovative robotic solution designed to act as a data bypass link in the event of an undersea cable fault, ensuring uninterrupted data flow. HERMES can also replace the role of underwater fiber-optic cables near the shore and therefore open valuable sea lanes that were restricted to protect those cables. Additionally, HERMES can provide an internet connection to remote regions. The robot also has environmental monitoring functions and other capabilities which focus on its surroundings.

## HERMES key features

**Wireless Network Technology:** The central idea behind this robotic solution is to decrease the possibility of cable damage, by replacing the cable communications with a wireless network, until repaired or permanently.
**Navigation and Bypass:** HERMES is able to navigate to the coordinates of the accident and bypass the communication.
**Network Extender for Remote Areas:** A system that can also run as a network extender for unreachable remote areas.
**Environmental Monitoring:** Additionally, our model operates as a station to collect data and monitor the environment, in order to identify environmental anomalies and spot air and water pollution.
**Safety in water:** Hermes can warn vessels and assist in search and rescue missions by detecting the presence of living organisms.

## How we created HERMES
HERMES system consists of 3 parts, although its name was given by the main vessel. 

![HERMES system](/images/HERMES-system.png "HERMES system")

All 3 subsystems where designed in Fusion 360 and 3D printed. Due to restrictions on printing volume but also on our concept of using two colors, these susbsystems consist of several parts. In folder Design/STL you can find all these parts organized by the subsystem name. Using those files you will be able to slice and print an exact copy of HERMES, land station and underwater station. Indicatively, printing time required is more than 200 hours on a low-cost printer (like the one we used).

Raspberry Pi PICO is used as the main controller on all subsystems. Especially HERMES included two of them in order to balance proccessing speed and control in a better way all its functionalities. Programming language used is Python and in specific controllers are using [Circuitpython](https://circuitpython.org/) that is a user-friendly python version dedicated to micro-controllers. In folder Code you can find our programs for its one of the subsystems. Please mention that HERMES includes two PICO's so you will find two programs in that folder.

Electronics used are from several manufacturers, depending on their capabilities, their availability and our purpose (present our idea at WRO2023). Below you may find a list of the ones we used and a diagram for their connection.

### HERMES
- 2x Rasperry Pi PICO
- 2x Pico expansion board
- 3x IIC to UART module
- 4x HC12 RF module
- 4x RF waterproof antenna
- 1x PH sensor kit
- 1x Conductivity sensor kit
- 1x DS18B20 waterproof sensor
- 1x TSL2591 sensor
- 1x BME680 sensor
- 1x MQ135 sensor
- 1x GPS module
- 1x BNO 055 Euler angles sensor
- 1x Thernal imaging camera
- 2x Solar panel 3.5W
- 2x Solar power manager 10000mAh
- 1x DC step-down 5v dual usb
- 1x Dual motor driver module
- 2x thruster (dc motor)

![HERMES circuit](/images/HERMES-circuit.png "HERMES circuit")

### LAND station
- 1x Rasperry Pi PICO
- 1x Pico expansion board
- 2x HC12 RF module
- 4x RF waterproof antenna

![LAND station circuit](/images/STATION-circuit.png "LAND station circuit")

### UNDERWATER station
- 1x Rasperry Pi PICO
- 1x Pico expansion board
- 2x HC12 RF module
- 4x RF waterproof antenna

![LAND station circuit](/images/STATION-circuit.png "LAND station circuit")




## Innovation and social impact of HERMES
HERMES is a truly innovative addition to today's interconnected society. 

**Safety and Reliability for Users:** HERMES aims to increase the safety and reliability of telecom systems for users, making essential everyday networks more secure and with a steadier infrastructure. 
**A Global Transformation:** Our vision is to alter worldwide communications for the better, by establishing the most stable transmission system ever. 
**Rapid Deployment and Integration:** Being a low cost and open source project it allows the rapid deployment and integration into the global internet infrastructure.

> Humankind now can rely on this stable communication network for critical sectors of daily life such as good health and well being (goal 3), quality education (goal 4), reduced inequalities (goal 10), decent work and economic growth (goal 8) and many more.


