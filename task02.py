import struct, zlib

data = bytearray(open("challenge.png", "rb").read())

# 1. Brute-force the real height: it must reproduce the CRC stored in IHDR
width = struct.unpack(">I", data[16:20])[0]
stored_crc = struct.unpack(">I", data[29:33])[0]

for h in range(1, 5000):
    ihdr = b"IHDR" + struct.pack(">II", width, h) + data[24:29]
    if zlib.crc32(ihdr) == stored_crc:
        data[20:24] = struct.pack(">I", h)
        print("Real height:", h)
        break

# 2. Delete the fake IEND chunk (12 bytes) hidden in the middle of the file
fake_iend = b"\x00\x00\x00\x00IEND\xaeB`\x82"
pos = data.find(fake_iend)          # first hit = fake, last hit = real one
print("Fake IEND at offset:", hex(pos))
del data[pos:pos + 12]

open("challenge_fixed.png", "wb").write(data)
print("Saved challenge_fixed.png")
