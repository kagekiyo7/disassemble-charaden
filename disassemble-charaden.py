# -*- coding: utf-8 -*-

import os
import sys

def extract(magic: bytes, content: bytes):
    ret = []
    offset = 0
    
    while True:
        offset = content.find(magic, offset)
        if (offset == -1):
            break
        if (int.from_bytes(content[offset-2:offset]) != 0):
            offset += 1
            continue
        size = int.from_bytes(content[offset-4:offset-2], byteorder="little")
        ret.append(content[offset:offset+size])
        offset += 1
    
    return ret

def main(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    dir_name = os.path.dirname(file_path)
    
    with open(file_path, "rb") as f:
        charaden_content = f.read()
        
    mbacs = extract(b"MB", charaden_content)
    mtras = extract(b"MT", charaden_content)
    gifs = extract(b"GIF", charaden_content)

    def output(contents, ext):
        i = 0
        for content in contents:
            output_path = os.path.join(dir_name, f"{file_name}_{i}.{ext}")
            
            with open(output_path, "wb") as f:
                f.write(content)
            
            print(f"{os.path.basename(output_path)}: done!")
            i += 1
    
    output(mbacs, ext="mbac")
    output(mtras, ext="mtra")
    output(gifs,  ext="gif")

if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        main(file_path)
