"""
Version 0.1:
* Set Heat and cool mode
* Set temperature
* schedule temp changes

Version 0.2:
* Read from external thermometer
* Set temperature based on external thermometer
* schedule temp changes based on external thermometer

Version 0.3:
"""


def set_temperature(temp):
    """Set the temperature of the minisplit"""
    pass


def set_mode(mode):
    """Set the mode of the minisplit"""
    pass


def _serial():
    import serial
    temp = 50

    with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as f:
        with open("example", "w") as bp:
            while True:
                for line in f:
                    line = line.decode("utf-8")
                    line = line.strip()
                    if len(line) < 1:
                        continue
                    if line[0] == "#":
                        description = line.strip()
                        continue
                    if "uint8_t rawTicks[291]" in line:
                        binary_data = []

                        data = line.strip().strip("uint8_t rawTicks[291] = {").strip(
                            "};  // Protocol=PulseDistance Raw-Data=0xCB23 144 bits LSB first")
                        data = data.split(" ")
                        bit_counter = 0

                        for pair in data:
                            split = pair.strip(",").split(",")
                            if len(split) != 2:
                                continue
                            on, off = split
                            on = int(on)
                            off = int(off)
                            if off > 30:
                                binary_data.append("5")
                                binary_data.append(" ")

                                continue

                            if off > 15:
                                binary_data.append("x")
                            else:
                                binary_data.append(".")
                            bit_counter += 1
                            if bit_counter % 8 == 0:
                                binary_data.append(" ")
                        bp.write(str("".join(binary_data)))
                        bp.write(str(temp))
                        print(temp)
                        temp += 1
                        bp.write("\n")

def read_protocol():
    with open("bp", "w") as bp:

        with open("protocol") as f:
            description = ""
            for line in f:
                if line[0] == "#":
                    description = line.strip()
                    continue
                if line[0] == "u":
                    binary_data = []

                    data = line.strip().strip("uint8_t rawTicks[291] = {").strip("};  // Protocol=PulseDistance Raw-Data=0xCB23 144 bits LSB first")
                    data = data.split(" ")
                    bit_counter = 0

                    for pair in data:
                        split = pair.strip(",").split(",")
                        if len(split) != 2:
                            continue
                        on, off = split
                        on = int(on)
                        off = int(off)
                        if off > 30:
                            binary_data.append("5")
                            binary_data.append(" ")

                            continue

                        if off > 15:
                            binary_data.append("x")
                        else:
                            binary_data.append(".")
                        bit_counter += 1
                        if bit_counter % 8 == 0:
                            binary_data.append(" ")
                    bp.write(str("".join(binary_data)))
                    bp.write(description)
                    bp.write("\n")


def binary_to_int():
    with open("binary") as f:
        for line in f:
            line = line.strip()
            line = line.replace(".", "0")
            line = line.replace("x", "1")
            print(line)

            # line = line[::-1]
            line_val = 0
            place_val = 1
            for a in line:
                line_val += int(a) * place_val
                place_val *= 2
            print(line_val)


"""
uint16_t rawData[291] = {3480,1670, 480,1270, 430,1270, 430,420, 480,420, 430,420, 430,1270, 480,420, 430,420, 480,1220, 480,1270, 430,420, 430,1270, 480,420, 430,420, 430,1270, 430,1270, 480,420, 430,1270, 430,1270, 480,420, 430,420, 430,1270, 480,420, 430,420, 430,1270, 480,420, 430,420, 430,420, 480,420, 430,420, 430,470, 430,420, 430,420, 480,420, 430,420, 430,420, 480,420, 430,420, 480,420, 430,420, 430,420, 480,420, 430,420, 430,470, 430,420, 430,1270, 480,370, 480,420, 430,420, 480,420, 430,420, 430,1270, 480,420, 430,420, 430,420, 480,420, 430,420, 480,1220, 480,1270, 430,1270, 430,420, 480,420, 430,420, 430,420, 480,420, 430,420, 480,420, 430,420, 430,1270, 480,1220, 480,420, 430,420, 480,420, 430,420, 430,1270, 430,1270, 480,420, 430,1270, 430,1270, 480,420, 430,420, 430,1270, 480,420, 430,420, 430,420, 480,420, 430,1270, 480,370, 480,420, 430,420, 430,470, 430,420, 430,420, 480,420, 430,420, 430,420, 480,420, 430,420, 480,420, 430,420, 430,420, 480,420, 430,420, 430,470, 430,420, 430,420, 480,420, 430,420, 480,370, 480,420, 430,420, 480,420, 430,420, 430,1270, 480,420, 430,420, 430,420, 480,420, 430,420, 480,1220, 480,420, 430,420, 430,420, 480,420, 430,420, 480,420, 430,420, 430,420, 480,420, 430,420, 480,420, 430,420, 430,420, 480,420, 430,420, 430,470, 430,1270, 430,1270, 430,420, 480,1270, 430,420, 430,1270, 480,420, 430,1270, 430};  // Protocol=PulseDistance Raw-Data=0xCB23 144 bits LSB first
"""
if __name__ == '__main__':
    # read_protocol()
    _serial()
    # binary_to_int()
