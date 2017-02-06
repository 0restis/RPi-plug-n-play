#
#   Python code for RPi to read Morse-encoded
#   message from manual switch input and decode
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
	else:
            return 0.2

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
	GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(led, GPIO.OUT)

        flag = False
	tStart = 0
	tEnd = 0
	s = ""
	# reads 22-character message - length arbitrarily chosen  
	while len(s) < 22:
            while True: 
                    inputState = GPIO.input(button)
                    if (inputState == False) and (not flag):
                            tStart = time.time()
                            if tStart - tEnd > 1.2:
                                    print 'new letter: '
                                    s = s + ' '
                            flag = True
                    elif inputState == True and flag:
                            tEnd = time.time()
                            flag = False
                            break
            if (tEnd - tStart) < 0.6:
                    print '.'
                    s = s + '.'
            else:
                    print '-'
                    s = s + '-'
        print '\n' + 'Encoded message characters: '
        print s.split()
        print '\n' + 'Corrupted characters will be denoted by $ ' \
              + '\n' + 'Decoded message is: ' + '\n\n' + fromMorse(s) + '\n'
        
if __name__ == "__main__":
        main()
