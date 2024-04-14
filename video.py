import os
import pdb
import pickle
import shutil
import time
import io

import cv2
import google.generativeai as genai
import pandas as pd
import torch
from dotenv import load_dotenv
from pyannote.audio import Pipeline
from moviepy.editor import VideoFileClip
from pyannote.audio import Pipeline
from prompters import *

### CONFIGURE KEYS IN A .ENV FILE###
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
HUGGING_FACE_KEY=os.environ["HUGGING_FACE_KEY"]

### CONFIGURE ###
video_file_name = "DG Check-in-20230705_084639-Meeting Recording (online-video-cutter.com) (1).mp4"

FRAME_EXTRACTION_DIRECTORY = "frames"
FRAME_PREFIX = "_frame"
AUDIO_FILE = "DG Check-in-20230705_084639-Meeting Recording (online-video-cutter.com) (1).wav"

class File:
  def __init__(self, file_path: str, display_name: str = None):
    self.file_path = file_path
    if display_name:
      self.display_name = display_name
    self.timestamp = get_timestamp(file_path)

  def set_file_response(self, response):
    self.response = response


def extract_audio(video_file_path, audio_path, codec='mp3'):
    # Load the video file
    video = VideoFileClip(video_file_path)
    
    # Extract the audio from the video
    audio = video.audio
    #buffer = io.BytesIO()
    # Write the audio to a file in the specified format
    audio.write_audiofile(audio_path, codec=codec)
    # buffer.seek(0)
    # return buffer


def get_timestamp(filename):
  """Extracts the frame count (as an integer) from a filename with the format
     'output_file_prefix_frame00:00.jpg'.
  """
  parts = filename.split(FRAME_PREFIX)
  if len(parts) != 2:
      return None  # Indicates the filename might be incorrectly formatted
  return parts[1].split('.')[0]

def create_frame_output_dir(output_dir):
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  else:
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def extract_frame_from_video(video_file_path):
  print(f"Extracting {video_file_path} at 1 frame per second. This might take a bit...")
  create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
  vidcap = cv2.VideoCapture(video_file_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  frame_duration = 1 / fps  # Time interval between frames (in seconds)
  output_file_prefix = os.path.basename(video_file_path).replace('.', '_')
  frame_count = 0
  count = 0
  while vidcap.isOpened():
      success, frame = vidcap.read()
      if not success: # End of video
          break
      if int(count / fps) == frame_count: # Extract a frame every second
          min = frame_count // 60
          sec = frame_count % 60
          time_string = f"{min:02d}:{sec:02d}"
          image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
          output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
          cv2.imwrite(output_filename, frame)
          frame_count += 1
      count += 1
  vidcap.release() # Release the capture object\n",
  print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

def make_request(prompt, files):
  request = [prompt]
  for file in files:
    request.append(file.timestamp)
    request.append(file.response)
    # request.append(get_timestamp(file.display_name))
    # request.append(file)
  return request

def upload_video(vid_name, df, do_upload):

    shutil.rmtree(FRAME_EXTRACTION_DIRECTORY)
    os.mkdir(FRAME_EXTRACTION_DIRECTORY)

    video_file_name = vid_name
    extract_frame_from_video(video_file_name) 
    # Process each frame in the output directory
    files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
    files = sorted(files)
    files_to_upload = []
    for file in files:
        files_to_upload.append(
            File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))

    # Upload the files to the API
    # Only upload a 10 second slice of files to reduce upload time.
    # Change full_video to True to upload the whole video.
    full_video = True

    uploaded_files = []
    print(f'Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit...')
    new_df = []

    for file in files_to_upload if full_video else files_to_upload[40:50]:
        print(f'Uploading: {file.file_path}...')
        # response = genai.upload_file(path=file.file_path)
        response = do_upload(path=file.file_path)
        file.set_file_response(response)
        uploaded_files.append(file)
        new_df.append((response.name, response.display_name, prefix))

    new_df = pd.DataFrame(new_df, columns=['uid', 'display_name', 'origin_name'])
    df = pd.concat((df, new_df), axis=0)
        

    print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")

    # List files uploaded in the API
    for n, f in zip(range(len(uploaded_files)), genai.list_files()):
        print(f.uri)

    ### SPEAKER CLASSIFICATION ###
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=HUGGING_FACE_KEY)
    pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    diarization = pipeline("DG Check-in-20230705_084639-Meeting Recording (online-video-cutter.com) (1).wav")

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")

    ### SPEAKER CLASSIFICATION ###

    audio_name = prefix + '.mp3'
    #audio_file = genai.upload_file(path=audio_name)
    audio_file = do_upload(path=audio_name)
    df = pd.concat((df, pd.DataFrame({'uid' : [audio_file.name], 
                                     'display_name' : [audio_file.display_name], 
                                     'origin_name' : [prefix]})), axis=0
                                     )
    
    return df


class MockFile:
   def __init__(self, name, display_name):
      self.name = name
      self.display_name = display_name

class MockUpload:
    def __init__(self):
        self.counter =0

    def __call__(self, path):
       self.counter += 1
       return MockFile(self.counter, display_name=path)


def fetch_with_retries(uid, max_retries=100):
    retries = 0
    success = False
    while retries < max_retries and not success:
        try:
            response = genai.get_file(uid)
            success = True
            return response
        except Exception as e:
            wait_time = 2 ** retries  # Exponential backoff
            print(f"Error fetching {uid}: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
    print(f"Failed to fetch {uid} after {max_retries} attempts.")
    return None


def get_frames_and_audio(test_file):
    df = pd.read_csv('file_manifest.csv')
    df = df[df['origin_name'] == test_file]

    frame_uids = df[df['display_name'].str.contains('jpg')]['uid'].to_list()
    audio_uid = df[df['display_name'].str.contains('mp3')]['uid'].iloc[0]

    frames = [fetch_with_retries(frame) for frame in frame_uids]
    audio = fetch_with_retries(audio_uid)
  

def get_speaker_frequencies(audio_file):
  # .wav file is passed in
  pass

def get_frames():

  # Specify the path of your pickle file
  pickle_file_path = 'testSample1.pkl'

  # Open the file in binary read mode
  with open(pickle_file_path, 'rb') as file:
      # Deserialize the pickled list of objects
      loaded_objects = pickle.load(file)
  

  return loaded_objects

def get_audio(test_file):
  df = pd.read_csv('file_manifest.csv')

  df = df[df['origin_name'] == test_file]
  audio_uid = df[df['display_name'].str.contains('mp3')]['uid'].iloc[0]
  audio = genai.get_file(audio_uid)

  return audio

def get_speaker_freq(wav_file):
    pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HUGGING_FACE_KEY)

    # send pipeline to GPU (when available)

    pipeline.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    # apply pretrained pipeline
    diarization = pipeline(wav_file)

    speaker_freq = {}
    # print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if speaker not in speaker_freq:
           speaker_freq[speaker]=0
        speaker_freq[speaker]+=1
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    return speaker_freq

def run_prompts(filename, members):
    

    video_path = filename
    mp3_path = 'audio.mp3'
    wav_path = 'audio.wav'

    mp3_audio = extract_audio(video_path, mp3_path, codec='mp3')
    wav_audio = extract_audio(video_path, wav_path, codec='pcm_s16le')
    extract_frame_from_video(filename)


    ### UPLOAD FILES ###
    files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
    files = sorted(files)
    files_to_upload = []
    for file in files:
        files_to_upload.append(
            File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))

    full_video = True

    uploaded_files = []
    print(f'Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit...')

    for file in files_to_upload if full_video else files_to_upload[40:50]:
        print(f'Uploading: {file.file_path}...')
        response = genai.upload_file(path=file.file_path)
        file.set_file_response(response)
        uploaded_files.append(file)

    print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")

    

    ####

    
    speaker_frequencies = get_speaker_freq(wav_path)
    audio_file = genai.upload_file(path=mp3_path)

    future_tasks = FutureTaskPrompter()
    effort = MeetingEffortPrompter()
    participation = MeetingParticipationPrompter()
    professionalism = MeetingProfessionalismPrompter()
    respect = MeetingRespectPrompter()
    productivity = MeetingProductivityPrompter()
    scribe = MeetingScribePrompter()



    response = {}

    summary = scribe.prompt(uploaded_files, audio_file, members)
    response['scribe'] = summary
    print(summary)

    productivity_eval = productivity.prompt(uploaded_files, audio_file, speaker_frequencies)
    response['meetingFeedback']= [productivity_eval]
    print(productivity_eval)

    participation_eval = participation.prompt(uploaded_files, audio_file, speaker_frequencies)
    response['meetingFeedback'].append(participation_eval)
    print(participation_eval)

    respect_eval = respect.prompt(uploaded_files, audio_file)
    response['meetingFeedback'].append(respect_eval)
    print(respect_eval)

    effort_eval = effort.prompt(uploaded_files, audio_file)
    response['meetingFeedback'].append(effort_eval)
    print(effort_eval)

    professionalism_eval = professionalism.prompt(uploaded_files, audio_file)
    response['meetingFeedback'].append(professionalism_eval)
    print(professionalism_eval)

    future_task_list = future_tasks.prompt(uploaded_files, audio_file)
    response['futureTasks'] = future_task_list
    print(future_task_list)

    print(response)

    return response


### TESTING MAIN FUNCTION CALL 
if __name__ == '__main__':
   video = 'testSample1.mp4'
   members = ['Pedro', 'Vara', 'Noah', "Rich"]
   run_prompts(video, members)















