import json

# Load map
with open("The Lost Temple of Devastation 01.json") as f:
    data = json.load(f)

cells = data["cells"]

# Define symbols for readability
symbols = {
    0: "#",         # empty
    16: "#",        # wall
    66: "?",        # corridor / floor
    130: "?",       # room floor
    4: "?",         # door/archway
    131076: "?",    # door (bitmask variant)
    2097156: "=",   # portcullis
}

# Generate the ASCII map
txt_map = []
for row in cells:
    line = "|".join(symbols.get(cell, "?") for cell in row)
    txt_map.append(f"|{line}|")

# Print it
with open('map1.txt', 'w') as file:
    file.write("\n".join(txt_map))
print("\n".join(txt_map))
