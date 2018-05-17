import os

MP3_PATH = '/Users/lfvarela/Desktop/UNHCR_files/Audio_mp3_luis'
FLAC_PATH = '/Users/lfvarela/Desktop/UNHCR_files/Audio_flac_luis'

def main():
	'''
	Converts files .mp3 files in MP3_PATH directory and to .flac files, and saves
	them in FLAC_PATH.
	'''
	files = os.listdir(MP3_PATH)
	for file in files:
		if file[-4:] == '.mp3':
			file_flac = file[:-4] + '.flac'
			os.system('ffmpeg -i %s %s' % (os.path.join(MP3_PATH, file), os.path.join(FLAC_PATH, file_flac)))


if __name__ == '__main__':
    main()
