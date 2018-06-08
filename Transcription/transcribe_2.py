import io
import os
import time
import tqdm
import sys, os, multiprocessing, csv


# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech

FLAC_PATH = '/Users/lfvarela/Desktop/UNHCR_files/Audio_flac_luis'
TRANSCRIPS_PATH = '/Users/lfvarela/Desktop/UNHCR_files/Transcripts_luis'
GCS_PATH = 'gs://cs50-audio-flac/Audio_flac_luis'
NUM_WORKERS = 8

def transcribe_file(gcs_uri):
    print('INPUT', gcs_uri)
    try:
        client = speech.SpeechClient()
        audio = speech.types.RecognitionAudio(uri=gcs_uri)
        config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
        sample_rate_hertz=8000,
        language_code='en-US',
        use_enhanced=True,
        # A model must be specified to use enhanced model.
        model='phone_call',
        speech_contexts=[speech.types.SpeechContext(phrases=['refugee', 'children', 'address', 'donation', 'email', 'number','monthly','happy', 'tomorrow','help',
        'refugees', 'thank', 'family', 'families', 'Middle East', 'donation', 'USA for UNHCR', 'UNHCR', 'United Nations','difference','tremendous','critical'])])
        operation = client.long_running_recognize(config, audio)
        response = operation.result(timeout = 6000)
        transcript_path1 =  os.path.join(TRANSCRIPS_PATH, 'Transcripts1', gcs_uri.split('/')[-1][:-5] + '.txt')
        transcript_path2 =  os.path.join(TRANSCRIPS_PATH, 'Transcripts2', gcs_uri.split('/')[-1][:-5] + '.txt')
        transcript_path3 =  os.path.join(TRANSCRIPS_PATH, 'Transcripts3', gcs_uri.split('/')[-1][:-5] + '.txt')

        with open(transcript_path1, 'w') as f:
            for result in response.results:
                f.write(result.alternatives[0].transcript + '\n')

        with open(transcript_path2, 'w') as f1:
            for result in response.results:
                for word_info in result.alternatives[0].words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    f1.write('{}\t{}\t{}\n'.format(word, start_time.seconds + start_time.nanos * 1e-9, end_time.seconds + end_time.nanos * 1e-9))

        with open(transcript_path3, 'w') as f2:
            for result in response.results:
                start_time = result.alternatives[0].words[0].start_time
                end_time = result.alternatives[0].words[-1].end_time
                f2.write('{}\t{}\t{}\n'.format(result.alternatives[0].transcript, start_time.seconds + start_time.nanos * 1e-9, end_time.seconds + end_time.nanos * 1e-9))
        return 0
    except Exception as e:
        print('Unable to transcribe {}'.format(gcs_uri))
        print(e)
        return 1


def create_folders():
    if not os.path.exists(TRANSCRIPS_PATH):
    	os.mkdir(TRANSCRIPS_PATH)

    if not os.path.exists(os.path.join(TRANSCRIPS_PATH, 'Transcripts1')):
        os.mkdir(os.path.join(TRANSCRIPS_PATH, 'Transcripts1'))

    if not os.path.exists(os.path.join(TRANSCRIPS_PATH, 'Transcripts2')):
        os.mkdir(os.path.join(TRANSCRIPS_PATH, 'Transcripts2'))

    if not os.path.exists(os.path.join(TRANSCRIPS_PATH, 'Transcripts3')):
        os.mkdir(os.path.join(TRANSCRIPS_PATH, 'Transcripts3'))


def main():
    audio_files = os.listdir(FLAC_PATH)
    audio_files_no_repeat = []
    for f in audio_files:
        if os.path.exists(os.path.join(TRANSCRIPS_PATH, 'Transcripts1', f[:-5] + '.txt')):
            print('File {} already transcribed'.format(f))
        else:
            audio_files_no_repeat.append(os.path.join(GCS_PATH, f))

    print('HERE', audio_files_no_repeat)

    pool = multiprocessing.Pool(processes=NUM_WORKERS)
    failures = sum(tqdm.tqdm(pool.imap_unordered(transcribe_file, audio_files_no_repeat), total=len(audio_files_no_repeat)))
    print('Done transcribing.')
    print('There were {} failures'.format(failures))
    pool.close()
    pool.terminate()

if __name__ == '__main__':
    create_folders()
    main()
