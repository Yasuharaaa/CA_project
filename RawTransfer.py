from PIL import Image
rawData = open("0.raw", 'rb').read()
imgSize = (3648,5472)
# Use the PIL raw decoder to read the data.
# the 'F;16' informs the raw decoder that we are reading
# a little endian, unsigned integer 16 bit data.
img = Image.frombytes('L', imgSize, rawData, 'raw', 'F;16')
img.save("foo.png")
