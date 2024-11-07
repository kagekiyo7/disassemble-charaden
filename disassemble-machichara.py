# -*- coding: utf-8 -*-

import os
import sys

def extract(magic: bytes, content: bytes):
    ret = []
    offset = -1
    
    while True:
        offset = content.find(magic, offset+1)
        if offset == -1: break
        if int.from_bytes(content[offset-8:offset-4], byteorder="little") > 0xFFFF:
            continue
        size = int.from_bytes(content[offset-4:offset], byteorder="little")
        ret.append(content[offset:offset+size])
    
    return ret

def main(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    dir_name = os.path.dirname(file_path)
    
    with open(file_path, "rb") as f:
        charaden_content = f.read()
        
    mbacs = extract(b"MB", charaden_content)
    mtras = extract(b"MT", charaden_content)
    gifs = extract(b"GIF", charaden_content)
    jpegs = extract(b"\xFF\xD8\xFF\xE0\x00\x10JFIF", charaden_content)
    bmps = extract(b"BM", charaden_content)

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
    output(jpegs,  ext="jpg")
    output(bmps,  ext="bmp")

if __name__ == "__main__":
    for file_path in sys.argv[1:]:
        print("Start")
        main(file_path)
        print("End")
