from mutagen.mp3 import MP3
from os import listdir
import re
import sys

def main():
    if len(sys.argv) != 2:
        print('Syntax: {} <directory>'.format(sys.argv[0]))
        sys.exit(0)
    AUDIO_DIR = sys.argv[1]

    total = 0
    max_ = 0
    min_ = float('inf')
    above_30 = 0

    for file in listdir(AUDIO_DIR):
        if re.match('.*\.mp3', file):
            audio = MP3(AUDIO_DIR + file)
            length = audio.info.length
            total += length
            if length > 30 * 60: above_30 += 1
            min_ = min(length, min_)
            max_ = max(length, max_)

    print('total:', total)
    print('max:', max_)
    print('min:', min_)
    print('# of files over 30 min:', above_30)


if __name__ == '__main__':
	main()
