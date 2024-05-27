import sys
import json
from stack import Stack
from memory import Memory


class DataPath:
    def __init__(self):
        self.data_memory: Memory = Memory()
        self.instruction_memory: Memory = Memory()

        self.return_stack: Stack = Stack()
        self.data_stack: Stack = Stack()

        self.input_buffer: list[int] = []
        self.output_buffer: list[int] = []


class ControlUnit:
    def __init__(self, data_path: DataPath):
        self.data_path = data_path

        self.instruction_pointer: int = 0
        self.instruction_counter: int = 0
        self.ticks = 0
        self.exit_flag = False

        self.no_operand_match = {
            "add": self.add,
            "sub": self.sub,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "inc": self.inc,
            "eql": self.is_equals,
            "less": self.is_less,
            "lrg": self.is_greater,
            "dec": self.dec,
            "pop": self.pop,
            "comp": self.compare,
            "dup": self.duplicate,
            "ret": self.ret,
            "read": self.read_from_stack,
            "save": self.save_from_stack,
            "swap": self.swap,
            "hlt": self.halt,
            "nop": self.nop,
        }

        self.one_operand_match = {
            "push": self.push,
            "read": self.read_operand,
            "save": self.save_operand,
            "jmp": self.jump,
            "jmz": self.jump_if_zero,
            "jnz": self.jump_if_not_zero,
        }

    def tick(self):
        self.ticks += 1

    def push(self, operand: int):
        self.data_path.data_stack.push(operand)
        self.tick()

    def pop(self):
        self.data_path.data_stack.pop()
        self.tick()

    def duplicate(self):
        self.data_path.data_stack.push(self.data_path.data_stack.peek())
        self.tick()

    def swap(self):
        self.data_path.data_stack.swap()
        self.tick()

    def add(self):
        y = self.data_path.data_stack.pop()
        self.tick()
        x = self.data_path.data_stack.pop()
        self.tick()

        result = x + y
        self.tick()

        self.data_path.data_stack.push(result)
        self.tick()

    def sub(self):
        y = self.data_path.data_stack.pop()
        self.tick()
        x = self.data_path.data_stack.pop()
        self.tick()

        result = x - y
        self.tick()

        self.data_path.data_stack.push(result)
        self.tick()

    def mul(self):
        y = self.data_path.data_stack.pop()
        self.tick()
        x = self.data_path.data_stack.pop()
        self.tick()

        result = x * y
        self.tick()

        self.data_path.data_stack.push(result)
        self.tick()

    def div(self):
        y = self.data_path.data_stack.pop()
        self.tick()
        x = self.data_path.data_stack.pop()
        self.tick()

        result = x // y
        self.tick()

        self.data_path.data_stack.push(result)
        self.tick()

    def mod(self):
        y = self.data_path.data_stack.pop()
        self.tick()
        x = self.data_path.data_stack.pop()
        self.tick()

        result = x % y
        self.tick()

        self.data_path.data_stack.push(result)
        self.tick()

    def inc(self):
        x = self.data_path.data_stack.pop()
        self.tick()

        result = x + 1
        self.tick()

        self.data_path.data_stack.push(result)
        self.tick()

    def dec(self):
        x = self.data_path.data_stack.pop()
        self.tick()

        result = x - 1
        self.tick()

        self.data_path.data_stack.push(result)
        self.tick()

    def compare(self):
        x = self.data_path.data_stack.pop()
        self.tick()
        y = self.data_path.data_stack.pop()
        self.tick()

        z = x - y

        if z < -1:
            z = -1
        if z > 1:
            z = 1

        self.tick()

        self.data_path.data_stack.push(z)
        self.tick()

    def is_equals(self):
        x = self.data_path.data_stack.pop()
        self.tick()
        y = self.data_path.data_stack.pop()
        self.tick()

        if x == y:
            self.data_path.data_stack.push(-1)
        else:
            self.data_path.data_stack.push(0)
        self.tick()

    def is_less(self):
        x = self.data_path.data_stack.pop()
        self.tick()
        y = self.data_path.data_stack.pop()
        self.tick()

        if y < x:
            self.data_path.data_stack.push(-1)
        else:
            self.data_path.data_stack.push(0)
        self.tick()

    def is_greater(self):
        x = self.data_path.data_stack.pop()
        self.tick()
        y = self.data_path.data_stack.pop()
        self.tick()

        if y > x:
            self.data_path.data_stack.push(-1)
        else:
            self.data_path.data_stack.push(0)
        self.tick()

    def read_from_stack(self):
        address = self.data_path.data_stack.pop()
        self.tick()

        assert address != 1, "can't read from output device"
        if address == 0:
            value = self.data_path.input_buffer.pop(0)
        else:
            value = self.data_path.data_memory.read(address)
        self.tick()

        self.data_path.data_stack.push(value)
        self.tick()

    def read_operand(self, address: int):
        assert address != 1, "can't read from output device"
        if address == 0:
            value = self.data_path.input_buffer.pop(0)
        else:
            value = self.data_path.data_memory.read(address)
        self.tick()

        self.data_path.data_stack.push(value)
        self.tick()

    def save_from_stack(self):
        address = self.data_path.data_stack.pop()
        self.tick()

        value = self.data_path.data_stack.pop()
        self.tick()

        assert address != 0, "can't write to input device"
        if address == 1:
            self.data_path.output_buffer.append(value)
        else:
            self.data_path.data_memory.write(address, value)
        self.tick()

    def save_operand(self, address: int):
        value = self.data_path.data_stack.pop()
        self.tick()

        assert address != 0, "can't write to input device"
        if address == 1:
            self.data_path.output_buffer.append(value)
        else:
            self.data_path.data_memory.write(address, value)
        self.tick()

    def jump(self, address: int):
        self.data_path.return_stack.push(self.instruction_pointer)
        self.tick()
        self.instruction_pointer = address
        self.tick()

    def jump_if_zero(self, address: int):
        self.tick()
        if self.data_path.data_stack.pop() == 0:
            self.jump(address)
        else:
            self.instruction_pointer += 1

    def jump_if_not_zero(self, address: int):
        self.tick()
        if self.data_path.data_stack.pop() != 0:
            self.jump(address)
        else:
            self.instruction_pointer += 1

    def ret(self):
        address = self.data_path.return_stack.pop()
        self.tick()
        self.instruction_pointer = address
        self.tick()

    def halt(self):
        self.exit_flag = True
        self.tick()

    def nop(self):
        self.tick()

    def handle_command(self):
        command = self.data_path.instruction_memory.read(self.instruction_pointer)
        if "operand" not in command.keys():
            self.no_operand_match[command["opcode"]]()
        else:
            self.one_operand_match[command["opcode"]](command["operand"])

        if command["opcode"] not in ["jmp", "jmz", "jnz"]:
            self.instruction_pointer += 1

        print(command, self.data_path.data_stack, self.data_path.return_stack)


def simulate(source_path: str, input_path:str, result_path: str):
    data_path = DataPath()
    control_unit = ControlUnit(data_path)

    with open(source_path, "r") as source_file:
        source = json.load(source_file)

    with open(input_path, "r") as input_file:
        data_path.input_buffer = list(map(ord, list(input_file.read()))) + [0]

    for variable in source["memory"]:
        data_path.data_memory.allocate(variable["size"])
        data_path.data_memory.write(variable["idx"], 0)

    for instruction in source["instructions"]:
        data_path.instruction_memory.allocate(1)
        data_path.instruction_memory.write(instruction["idx"], instruction)

    while not control_unit.exit_flag:
        control_unit.handle_command()
        control_unit.instruction_counter += 1

    print(f"System time: {control_unit.ticks}, instructions: {control_unit.instruction_counter}")

    with open(result_path, "w") as result_file:
        for c in data_path.output_buffer:
            if c != 0: result_file.write(chr(c))


if __name__ == "__main__":
    # assert len(sys.argv) == 3, "Usage: python machine.py <source> <input> <target>"
    # simulate(sys.argv[1], sys.argv[2], sys.argv[3])

    simulate("dest.json", "input.txt", "result.txt")
