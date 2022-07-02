import time
import PIL.ImageGrab
import pyfirmata

# Naming of LED pins connected to Arduino
TLR = 2
TLG = 3
TLB = 4
BLR = 5
BLG = 6
BLB = 7
TRR = 8
TRG = 9
TRB = 10
BRR = 11
BRG = 12
BRB = 13
# ^^ Using Arduino Mega so all pins here are PWM compatible.

# Connects to Arduino first and set up pin configuration
while True:
    try:
        print("Connecting to Arduino.....")
        board = pyfirmata.Arduino('COM4')
        for i in range(2, 14):
            board.digital[i].mode = pyfirmata.PWM
        print("Connected!")
        break
    except Exception as e:
        print("Error --> " + str(e))
        time.sleep(1)


# Gets Dominant Colour of an image at a certain coordinate
def get_dominant_color(pil_img, x, y):
    img = pil_img.copy()
    img.convert("RGB")
    dominant_color = img.getpixel((x, y))
    format = str(dominant_color).replace("(", "")
    format = str(format).replace(")", "")
    formatted = str(format).replace(",", "")
    formatted = formatted.split(" ")
    return formatted


# Gets current pixel values at specified coordinates
def getColours():
    image = PIL.ImageGrab.grab()
    TopLeftLED = get_dominant_color(image, 485, 421)
    TopRightLED = get_dominant_color(image, 1479, 442)
    BottomLeftLED = get_dominant_color(image, 485, 645)
    BottomRightLED = get_dominant_color(image, 1479, 656)
    singleLine = TopLeftLED[0] + " " + TopLeftLED[1] + " " + TopLeftLED[2] + " " + TopRightLED[0] + " " + \
                 TopRightLED[1] + " " + TopRightLED[2] + " " + BottomLeftLED[0] + " " + BottomLeftLED[1] + " " + \
                 BottomLeftLED[2] + " " + BottomRightLED[0] + " " + BottomRightLED[1] + " " + BottomRightLED[2]
    SendToSerial(singleLine)


# Sends data to Arduino Serial.
def SendToSerial(LEDColour):
    LEDColour = str(LEDColour).split(" ")
    try:
        divider = 0.00255
        j = 0
        for i in range(2, 14):
            board.digital[i].write(float(LEDColour[j]) * divider)
            j += 1

    except Exception as e:
        print(str(e))


while True:
    getColours()
