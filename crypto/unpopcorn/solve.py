m = 57983

def unbutterpop(ints):
    for p_inv in range(1, m+1):
        unbuttered = list(map(lambda x: x * p_inv % m, ints))
        unxored = list(map(lambda x: x ^ 42, unbuttered))
        try:
            possible_flag = bytes(unxored)
            flag = possible_flag.decode('ascii')
            print(flag)
        except (ValueError, UnicodeDecodeError):
            pass

def unchurn(hex_str_list):
    decimal_ints = list(map(lambda x: int(x, 16), hex_str_list))
    unrotated = decimal_ints[-16:] + decimal_ints[:-16]
    return list(map(lambda x: (x >> 3), unrotated))

message = open("message.txt").read()
hex_str_list = message.split(" ")
unbutterpop(unchurn(hex_str_list))
