with open("100MB.bin", "wb") as out:
    out.seek((100*1024*1024) - 1)
    out.write('\0')