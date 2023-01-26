from crc import Calculator, Crc16

# example:
# dostajemy ramkę w postaci bajtów albo innej

# dostajemy ramkę z wyspecyfikowanymi elementami

example = "000000010100000000100000001"  # with SOF


def splited_can(message, is_sof=True):
    if is_sof:
        new_message = message[1:]

    id = new_message[:11]
    new_message = new_message[11:]
    RTR = new_message[:1]
    new_message = new_message[1:]
    IDE = new_message[:1]
    new_message = new_message[1:]
    r0 = new_message[:1]
    new_message = new_message[1:]
    DLC = new_message[:4]
    new_message = new_message[4:]
    data_length = int(DLC, 2) * 8
    data = new_message[:data_length]

    print(f"ID: {id}")
    print(f"RTR: {RTR}")
    print(f"IDE: {IDE}")
    print(f"r0: {r0}")
    print(f"DLC: {DLC}")
    print(f"Data: {data}")

    return id, RTR, IDE, r0, DLC, data


splited_can(example)

id = "00000010100"
id_stuffed = "000010010100"
RTR = "0"
IDE = "0"
r0 = "0"
DLC = "0001"
DLC_stuffed = "10001"
data = "00000001"
data_stuffed = "000001001"

looked_up_crc = b"111011101010011"

specified_dict = {
    "id": id,
    "RTR": RTR,
    "IDE": IDE,
    "r0": r0,
    "DLC": DLC,
    "data": data
}

specified_dict_stuffed = {
    "id": id_stuffed,
    "RTR": RTR,
    "IDE": IDE,
    "r0": r0,
    "DLC": DLC_stuffed,
    "data": data_stuffed
}


class Frame:
    def __init__(self, input_msg, is_sof=True):
        self.input_msg = input_msg

        if type(input_msg) == dict:
            self.id = input_msg.get("id")
            self.RTR = input_msg.get("RTR")
            self.IDE = input_msg.get("RTR")
            self.r0 = input_msg.get("r0")
            self.DLC = input_msg.get("DLC")
            self.data = input_msg.get("data")
        else:
            self.id, self.RTR, self.IDE, self.r0, self.DLC, self.data = splited_can(self.input_msg, is_sof)

        if is_sof:
            self.msg = "0" + self.id + self.RTR + self.IDE + self.r0 + self.DLC + self.data
        else:
            self.msg = self.id + self.RTR + self.IDE + self.r0 + self.DLC + self.data

        self.msg_bytes = bytes(self.msg, "ascii")

        self.CRC = ""
        self.msg = ""
        self.msg_crc = ""
        self.msg_stuffed = ""

    def calculate_crc(self):
        calculator = Calculator(Crc16.CCITT)
        crc = calculator.checksum(self.msg_bytes)
        print(crc == looked_up_crc)

    def stuffing(self):
        ones = 0
        zeros = 0
        for bit in self.msg:
            self.msg_stuffed += bit

            if bit == "0":
                zeros += 1
                ones = 0
            elif bit == "1":
                ones += 1
                zeros = 0

            if zeros == 5:
                self.msg_stuffed += "0"
                zeros = 1
            elif ones == 5:
                self.msg_stuffed += "1"
                ones = 1

    def printer(self):
        print(f"Input message without CRC: ")
        print(f"Message without stuffing: ")
        print(f"Message with stuffing {self.msg}")


# frame_sof = Frame(specified_dict, is_sof=True)
# frame_sof.calculate_crc()
#
# frame_non_sof = Frame(specified_dict, is_sof=False)
# frame_non_sof.calculate_crc()
#
# frame_sof_stuffed = Frame(specified_dict_stuffed, is_sof=True)
# frame_sof_stuffed.calculate_crc()
#
# frame_non_sof_stuffed = Frame(specified_dict_stuffed, is_sof=False)
# frame_non_sof_stuffed.calculate_crc()
