with open("data//1KB.bin", "wb") as out:
    out.seek((1024) - 1)
    out.write('\0')

with open("data//10KB.bin", "wb") as out:
    out.seek((10*1024) - 1)
    out.write('\0')

with open("data//100KB.bin", "wb") as out:
    out.seek((100*1024) - 1)
    out.write('\0')

with open("data//1MB.bin", "wb") as out:
    out.seek((1024*1024) - 1)
    out.write('\0')

with open("data//10MB.bin", "wb") as out:
    out.seek((10*1024*1024) - 1)
    out.write('\0')

with open("data//100MB.bin", "wb") as out:
    out.seek((100*1024*1024) - 1)
    out.write('\0')