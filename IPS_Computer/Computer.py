class INSError(Exception):
    pass


class UndefinedRegisterError(INSError):
    pass
    # def __init__(self, register):
    #     super().__init__(f"The name of the undefined register is {register}.")


class UndefinedInstructionError(INSError):
    pass


class UndefinedScriptArgumentError(INSError):
    pass


def CLR(reg):
    # CLR x
    # clear x
    
    register[reg] = 0


def INC(reg):
    # INC x
    # increase x value by 1
    
    if reg not in register:
        raise UndefinedRegisterError(reg)
    register[reg] += 1


def DEC(reg):
    # DEC x
    # decrease x value by 1 (0 if register already at 0)
    
    if reg not in register:
        raise UndefinedRegisterError(reg)
    register[reg] = max(0, register[reg] - 1)


def JEQ(x,y,pt_new):
    # JEQ x y pt_new
    # if x == y go with pointer to pt_new
    
    global pointer
    if x not in register:
        raise UndefinedRegisterError(x)
    elif y not in register:
        raise UndefinedRegisterError(y)
    elif register[x] == register[y]:
        pointer = int(pt_new) - 2


def JNE(x, y, pt_new):
    # JNE x y pt_new
    # if x != y go with pointer to pt_new

    global pointer
    if x not in register:
        raise UndefinedRegisterError(x)
    elif y not in register:
        raise UndefinedRegisterError(y)
    elif register[x] != register[y]:
        pointer = int(pt_new) - 2


def JMP(pt_new):
    # JMP pt_new
    # go with pointer to pt_new

    global pointer
    pointer = int(pt_new) - 2


def CON(reg, const):
    # CON x y
    # repeated INC on x by y

    register[reg] = int(const)


def DEL(reg):
    # DEL x
    # remove register x from list of registers
    
    del register[reg]


def PRT(reg):
    # PRT x
    # print on screen value of x

    if reg not in register:
        raise UndefinedRegisterError(reg)
    print(f"{reg}: {register[reg]}")


INSTRUCTIONS = {
    "CLR",
    "INC",
    "DEC",
    "JEQ",
    "JNE",
    "JMP",
    "CON",
    "DEL",
    "PRT",
}


register = {}
pointer = -1


def run_file(filename, *args):
    global pointer

    try:
        with open(filename, "r") as op:
            instr = [
                [args[int(word[1:])] if word.startswith("#") else word for word in line.split() if not line.startswith("%")]
                for line in op
            ]
    except IndexError:
        raise UndefinedScriptArgumentError(" ".join((filename,) + args))

    pointer = 0
    while True:
        if pointer >= len(instr):
            break
        if not instr[pointer]:
            pointer += 1
            continue

        if instr[pointer][0].upper() in INSTRUCTIONS:
            globals()[instr[pointer][0].upper()](*instr[pointer][1:])
        else:
            try:
                pointer_saved = pointer
                run_file(f"Functions/INS_{instr[pointer][0].upper()}.ips", *instr[pointer][1:])
                pointer = pointer_saved
            except FileNotFoundError:
                raise UndefinedInstructionError(instr[pointer][0].upper())
        pointer += 1


def main(filename):
    try:
        if filename.endswith(".ips"):
            reg_file = open(f"{filename[:-4]}.reg", "r")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        reg_file = open("Register.txt", "r")
    try:
        for line in reg_file:
            line = line.split()
            if len(line) < 2:
                continue
            register[line[0]] = int(line[1])
    finally:
        reg_file.close()

    run_file(filename)


if __name__ == "__main__":
    try:
        main("Test/Factorial.ips")
    finally:
        print("\nProgram terminated with following values:")
        with open("Output.txt", "w") as op:
            for reg, val in register.items():
                if val is not None:
                    print(f"{reg}: {val}", file=op)
                    print(f"{reg}: {val}")
