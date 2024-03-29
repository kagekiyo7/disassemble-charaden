# -*- coding: utf-8 -*-

import os
import sys

def extract(magic: bytes, binary: bytes):
    ret = []
    file_i = 0
    while True:
        file_i = binary.find(magic, file_i)
        if (file_i == -1):
            break
        if (int.from_bytes(binary[file_i-2:file_i]) != 0):
            file_i += 1
            continue
        size = int.from_bytes(binary[file_i-4:file_i-2], byteorder="little")
        ret.append(binary[file_i:file_i+size])
        file_i += 1
    return ret

def main(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    dir_name = os.path.dirname(file_path)
    with open(file_path, "rb") as f:
        target_binary = f.read()
    gifs = extract("MB".encode(), target_binary)
    mbacs = extract("MT".encode(), target_binary)
    mtras = extract("GIF".encode(), target_binary)

    def output(binaries, ext):
        i = 0
        for binary in binaries:
            output_path = os.path.join(dir_name, f"{file_name}_{i}.{ext}")
            with open(output_path, "wb") as f:
                f.write(binary)
                print(f"{os.path.basename(output_path)}: done!")
            i += 1
    output(gifs,  ext="gif")
    output(mbacs, ext="mbac")
    output(mtras, ext="mtra")

if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        main(file_path)