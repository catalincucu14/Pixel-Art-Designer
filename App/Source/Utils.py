COLOR = "#99AAB5"
COLOR_HOVER = "#404EED"
BACKGROUND = " #2C2F33"
BACKGROUND_DARK = "#23272A"


def css(target, *properties):
    result = ""
    for i in properties:
        result = result + f"\t{i};\n"
    return f"{target}{{\n{result}}}"


def merge_css(*properties):
    result = ""
    for i in properties:
        result += f"{i}\n"
    return result


def color_darkness(color):
    return (0.299 * int(color[1:3], 16) + 0.587 * int(color[3:5], 16) + 0.114 * int(color[5:7], 16)) / 255
