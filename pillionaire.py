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
        if x == '1' or x == '2' and y != ''and int(y) < 7:
            ch = chr(int(x+y)+96) 
            result += ch
            i+=2
        else: 
            add = 96 if x != '0' else 95
            ch = chr(int(x) + add)
            result += ch
            i+=1
    return result

def letter_to_ascii(word):
    return "".join([
        str(ord(c) - 96)
        for c in word.lower().replace(' ', '')
    ])

def pillionaire(word, stop_at_first):
    search = letter_to_ascii(word)

    last_char = ''
    print whitebg + black + "Searching: %s (%s)" % (word, search) + reset 
    results = []
    try: 
        with open('pi-billion.txt') as f:
            count = 0
            for piece in read_in_chunks(f):
                count += 1
                if count % 100000 == 0 and not stop_at_first:
                    msg = "Done... %d %%" % (count / 10000)
                    sys.stdout.write(u"\u001b[20D" + msg)
                    sys.stdout.flush()
                piece = last_char + piece
                if search in piece:
                    idx = piece.index(search)
                    position = idx + count *1024
                    before =  piece[idx-5:idx]
                    found = piece[idx:idx+len(search)]
                    after = piece[idx+len(search):idx+len(search)+5] 
                    numbers = white + before + green + found + white + after
                    b = white + ascii_to_letters(before)
                    f = green + word 
                    a = white + ascii_to_letters(after)
                    txt = b+f+a 

                    results.append("Position %d: %s" % (position, numbers + ' -> ' + txt))
                    if stop_at_first:
                        pos_str = "{:,}".format(position)
                        return position, "At position %s we find %s: %s" % (pos_str, word, numbers + ' -> ' + txt)
                last_char = piece[-1]

                if len(results) > 20:
                    break

            if stop_at_first:
                return
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

if len(sys.argv) == 2:
    pillionaire(sys.argv[-1], False)

else:
    print "Who is most PI in sana?"
    sanians = [
        "alex",
        "anna",
        "chris",
        "damjan",
        "elyes",
        "emil",
        "faruk",
        "fredrik",
        "jaro",
        "jaromir",
        "jasmine",
        "jenny",
        "jesper",
        "joel",
        "jon",
        "ludvig",
        "lundgren",
        "mai",
        "miru",
        "miruna",
        "nille",
        "oscar",
        "patrik",
        "petter",
        "samuel",
        "seb",
        "sebastian",
        "sofie",
        "susanna",
        "ulf",
        "vale",
        "victor",
        "viktor",
            ]
    results = [(s,pillionaire(s, True)) for s in sanians]
    no_match = [r[0] for r in results if not r[1]]
    results = [r[1] for r in results if r[1]]

    results.sort(key=lambda x: x[0])
    for r in results:
        print r[1]

    print "Not within a billion digits..."
    for r in no_match:
        print r

