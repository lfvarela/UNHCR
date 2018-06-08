import os

path_mp3 = './audio_mp3_Kevin'
path_flac = './audio_flac_Kevin'
files = os.listdir(path_mp3)
for file in files:
	if file[-4:] == '.mp3':
		file_flac = file[:-4] + '.flac'
		os.system('ffmpeg -i %s %s' % (os.path.join(path_mp3, file), os.path.join(path_flac, file_flac)))