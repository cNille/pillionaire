#!/usr/bin/python
import sys

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

red = u'\u001b[31m'
green = u'\u001b[32m'
white = u'\u001b[37m'
black = u'\u001b[30m'
reset = u'\u001b[0m'
whitebg = u'\u001b[47m'

def ascii_to_letters(numbers):
    i = 0
    result = ''
    size = len(numbers)
    while i < size:
        x = numbers[i]
        y = numbers[i+1] if i < size-1 else '' 
        #print x
        if x == '1' or x == '2' and y != ''and int(y) < 7:
            #print x,y
            ch = chr(int(x+y)+96) 
            result += ch
            i+=2
        else: 
            add = 96 if x != '0' else 95
            ch = chr(int(x) + add)
            result += ch
            i+=1
    return result

#print ascii_to_letters('345')
#print ascii_to_letters('381891926')


def letter_to_ascii(word):
    return "".join([
        str(ord(c) - 96)
        for c in word.lower()
    ])

#word, search = letter_to_ascii('Nille')
#word, search = letter_to_ascii('Cnille')
#word, search = letter_to_ascii('Christopher')

def pillionaire(word):
    search = letter_to_ascii(word)

    last_char = ''
    print whitebg + black + "Searching: %s (%s)" % (word, search) + reset 
    results = []
    try: 
        with open('pi-billion.txt') as f:
            count = 0
            for piece in read_in_chunks(f):
                count += 1
                if count % 100000 == 0:
                    msg = "Done... %d %%" % (count / 10000)
                    sys.stdout.write(u"\u001b[20D" + msg)
                    sys.stdout.flush()
                piece = last_char + piece
                if search in piece:
                    idx = piece.index(search)
                    position = idx + count *1024
                    before =  piece[idx-4:idx]
                    found = piece[idx:idx+len(search)]
                    after = piece[idx+len(search):idx+len(search)+4] 
                    numbers = white + before + green + found + white + after
                    b = white + ascii_to_letters(before)
                    f = green + ascii_to_letters(found)
                    a = white + ascii_to_letters(after)
                    txt = b+f+a 

                    results.append("Position %d: %s" % (position, numbers + ' -> ' + txt))
                last_char = piece[-1]

            sys.stdout.write(u"\u001b[20D" + "Done... 100%")
            sys.stdout.flush()
            print ""
            if len(results) == 0:
                print "No results found"
            else:
                print " %d results: " % len(results)
                for r in results:
                    print r
    except IOError:
        print "ERROR:"
        print "./pi-billion.txt is missing. Download from: %s" % "https://stuff.mit.edu/afs/sipb/contrib/pi/"



pillionaire(sys.argv[-1])
