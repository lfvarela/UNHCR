import io
import os
import random

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech


FLAC_PATH = '/Users/lfvarela/Desktop/UNHCR_files/Audio_flac_luis'
TRANSCRIPS_PATH = '/Users/lfvarela/Desktop/UNHCR_files/Transcripts_luis'
GCS_PATH = 'gs://cs50-audio-flac/Audio_flac_luis'


def transcribe_file(gcs_uri):
	"""Transcribe the given audio file using an enhanced model."""
	try:
		client = speech.SpeechClient()
		audio = speech.types.RecognitionAudio(uri=gcs_uri)
		config = speech.types.RecognitionConfig(
			encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
			sample_rate_hertz=8000,
			language_code='en-US',
			# Enhanced models are only available to projects that
			# opt in for audio data collection.
			use_enhanced=True,
			# A model must be specified to use enhanced model.
			model='phone_call',
			enable_word_time_offsets=True,
			speech_contexts=[speech.types.SpeechContext(phrases=['refugee',
				'refugees', 'Syria', 'family', 'families', 'Middle East', 'donation', 'USA for UNHCR', 'UNHCR', 'United Nations'])])

		operation = client.long_running_recognize(config, audio)

		print('Waiting for operation to complete...')
		response = operation.result(timeout=600)

		# Each result is for a consecutive portion of the audio. Iterate through
		# them to get the transcripts for the entire audio file.
		transcript_path =  os.path.join(TRANSCRIPS_PATH, gcs_uri.split('/')[-1][:-5] + '.txt')
		with open(transcript_path, 'w') as f:
			for result in response.results:
				# The first alternative is the most likely one for this portion.
				print('Confidence: {}'.format(result.alternatives[0].confidence))
				print('Transcript: {}'.format(result.alternatives[0].transcript))
				f.write(result.alternatives[0].transcript + ' ')
	except Exception as e:
		print(e)

def main():
	audio_files = os.listdir(FLAC_PATH)
	#random.shuffle(audio_files)


	transcribe_file(os.path.join(GCS_PATH, 'U4U_NHCIInboundDRTV_CustomerService__3172000916_030118.flac')) # to test if works
	# i = 0
	# for file in audio_files:
	# 	transcribe_file(os.path.join(GCS_PATH, file))
	# 	i += 1
	# 	print(i)
	return

if __name__ == '__main__':
	main()
