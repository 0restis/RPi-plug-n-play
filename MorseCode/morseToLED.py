#
#   Python code for RPi to read keyboard input, encode
#   to Morse and output encoded message to LEDs
#
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

cMap = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',   ' ': ' ',
                    
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' }

cMapRev = {value:key for key,value in cMap.items()}

def toMorse(s):
    return ' '.join(cMap.get(i.upper(), defaultValue) for i in s)

def fromMorse(s):
    return ''.join(cMapRev.get(i, defaultValue) for i in s.split())

def TimedSwitch(onTime):
	GPIO.output(led, 1)
	time.sleep(onTime) 
	GPIO.output(led, 0)
	time.sleep(offTime)

def TimeForCharacter(character):
	if character == '.':
            return 0.3
	elif character == '-':
	    return 0.7

def main():
        global button
        global led
        global offTime
        global defaultValue
        defaultValue = '$'
        button = 19 
        led = 21
        offTime = 0.2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led, GPIO.OUT)
        print 'Input message: '
        userInput = raw_input()
        print '\n' + 'Decoded message: ' + '\n' + toMorse(userInput) + '\n'
        for char in userInput:
            print 'Letter : ' + char + ' , Morse : ' + toMorse(char)
            for morse in toMorse(char):
                if morse == '.' or morse == '-':
                    TimedSwitch(TimeForCharacter(morse))
                else:
                    time.sleep(1)

if __name__ == "__main__":
    main()
