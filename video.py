import google.generativeai as genai
import cv2
import os
import shutil
from pyannote.audio import Pipeline
import torch
from dotenv import load_dotenv
import pdb
import pandas as pd
import pickle

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


class MeetingEffort:
  def __init__(self):
        pass
  def prompt(self, frames, audio):
      prompt = """You have been provided with timestamped image frames and an audio recording of a recent meeting. Analyze the content and the conversation to evaluate if every member showed genuine preparation, technical knowledge(not asking clueless and repetitive questions), interest to have defined follow-up tasks, shows up on time for meeting. If even one person demonstrates a lack of either of those, note that in a general sense--don't name people by their names.  """
  # #prompt = "What was the first thing said in the meeting?"
  # # Set the model to Gemini 1.5 Pro.
      model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
  # Make the LLM request.
      request = make_request(prompt, frames)
      request.append(audio)
      response = model.generate_content(request,
                                  request_options={"timeout": 600})
      return response

class MeetingParticipation:
    def __init__(self):
        pass
    def prompt(self, frames, audio, speaker_frequencies):
        prompt = """You have been provided with timestamped image frames and an audio file of a recent meeting, speaker frequency dictionary and speaker timestamps. Conduct an analysis of overall participation in the meeting. Consider the following:

Assessment of Speaking Time:

Review the total speaking time for each participant as indicated by the speaker frequency dictionary. Identify if some people dominated the conversation excessively more due to significant discrepancies in speaking time among participants.
Role-Based Insights:

Consider the roles of the speakers (e.g., manager, student, staff). Discuss whether the distribution of speaking time seems appropriate based on their roles. Mention if the primary speaker was a manager and if their level of participation was suitable.
Equality of Participation Among Non-Managers:

Specifically assess how non-managerial participants engaged in the conversation. Identify if there were any individuals who were particularly quiet or disproportionately vocal. Stay general about the participation.
Recommendations for Participation Balance:

Suggest practical ways to ensure a more balanced and inclusive participation in future meetings, particularly for those who were less engaged.
Please provide a concise summary of your findings and recommendations to enhance participation equality and meeting effectiveness."""
    # #prompt = "What was the first thing said in the meeting?"
    # # Set the model to Gemini 1.5 Pro.
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    # Make the LLM request.
        request = make_request(prompt, frames)
        request.append(audio)
        request.append(str(speaker_frequencies))
        request.append("""
from pyannote.audio import Pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="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")

# send pipeline to GPU (when available)
import torch
pipeline.to(torch.device("cuda"))

# apply pretrained pipeline

start=3.2s stop=17.0s speaker_SPEAKER_00
start=17.7s stop=32.1s speaker_SPEAKER_00
start=32.5s stop=33.0s speaker_SPEAKER_00
start=33.3s stop=37.0s speaker_SPEAKER_00
start=38.1s stop=38.6s speaker_SPEAKER_00
start=38.8s stop=39.5s speaker_SPEAKER_00
start=40.2s stop=61.1s speaker_SPEAKER_00
start=61.7s stop=65.5s speaker_SPEAKER_00
start=65.7s stop=80.0s speaker_SPEAKER_00
start=80.5s stop=81.6s speaker_SPEAKER_00
start=82.2s stop=84.3s speaker_SPEAKER_00
start=85.8s stop=90.5s speaker_SPEAKER_03
start=91.6s stop=92.0s speaker_SPEAKER_00
start=92.1s stop=101.2s speaker_SPEAKER_00
start=102.1s stop=102.4s speaker_SPEAKER_03
start=103.7s stop=110.2s speaker_SPEAKER_02
start=111.3s stop=118.7s speaker_SPEAKER_02
start=119.5s stop=122.1s speaker_SPEAKER_02
start=123.8s stop=134.8s speaker_SPEAKER_00
start=135.3s stop=151.6s speaker_SPEAKER_00
start=151.9s stop=155.0s speaker_SPEAKER_00
start=155.5s stop=160.1s speaker_SPEAKER_00
start=160.6s stop=164.7s speaker_SPEAKER_00
start=166.6s stop=167.6s speaker_SPEAKER_02
start=168.6s stop=168.9s speaker_SPEAKER_00
start=173.6s stop=174.1s speaker_SPEAKER_00
start=175.5s stop=186.5s speaker_SPEAKER_00
start=187.0s stop=210.8s speaker_SPEAKER_00
start=211.5s stop=211.9s speaker_SPEAKER_00
start=212.4s stop=214.7s speaker_SPEAKER_00
start=215.2s stop=224.5s speaker_SPEAKER_00
start=224.9s stop=228.0s speaker_SPEAKER_00
start=229.6s stop=230.0s speaker_SPEAKER_00
start=230.6s stop=242.9s speaker_SPEAKER_00
start=243.5s stop=247.7s speaker_SPEAKER_00
start=247.9s stop=261.9s speaker_SPEAKER_00
start=262.2s stop=262.5s speaker_SPEAKER_03
start=263.6s stop=265.6s speaker_SPEAKER_01
start=266.6s stop=267.2s speaker_SPEAKER_01
start=267.7s stop=273.2s speaker_SPEAKER_01
start=273.4s stop=282.2s speaker_SPEAKER_01
start=282.9s stop=285.0s speaker_SPEAKER_01
start=286.0s stop=290.6s speaker_SPEAKER_01
start=291.0s stop=295.0s speaker_SPEAKER_02
start=296.4s stop=299.6s speaker_SPEAKER_02
start=297.2s stop=300.5s speaker_SPEAKER_03
start=300.2s stop=304.7s speaker_SPEAKER_02
start=305.5s stop=308.9s speaker_SPEAKER_01
start=305.7s stop=305.8s speaker_SPEAKER_02
start=305.8s stop=306.7s speaker_SPEAKER_03
start=308.6s stop=310.2s speaker_SPEAKER_03
start=310.6s stop=312.8s speaker_SPEAKER_01
start=312.8s stop=313.2s speaker_SPEAKER_03
start=313.6s stop=315.3s speaker_SPEAKER_01
start=316.1s stop=318.3s speaker_SPEAKER_01
start=319.0s stop=319.8s speaker_SPEAKER_00
start=320.1s stop=321.7s speaker_SPEAKER_00
start=322.6s stop=323.3s speaker_SPEAKER_00
start=323.8s stop=324.3s speaker_SPEAKER_00
start=324.9s stop=329.7s speaker_SPEAKER_00
start=330.2s stop=340.4s speaker_SPEAKER_00
start=341.2s stop=343.2s speaker_SPEAKER_00
start=343.7s stop=352.4s speaker_SPEAKER_00
start=349.5s stop=349.7s speaker_SPEAKER_02
start=355.1s stop=360.7s speaker_SPEAKER_01
start=359.8s stop=361.9s speaker_SPEAKER_03
start=362.9s stop=363.3s speaker_SPEAKER_03
start=363.8s stop=367.4s speaker_SPEAKER_03
start=368.6s stop=370.7s speaker_SPEAKER_03
start=372.5s stop=380.5s speaker_SPEAKER_00
start=380.6s stop=385.0s speaker_SPEAKER_00
start=385.2s stop=395.4s speaker_SPEAKER_00
start=395.6s stop=396.2s speaker_SPEAKER_00
start=396.6s stop=396.6s speaker_SPEAKER_00
start=396.6s stop=399.5s speaker_SPEAKER_03
start=396.6s stop=397.5s speaker_SPEAKER_00
start=401.1s stop=402.6s speaker_SPEAKER_00
start=403.0s stop=403.7s speaker_SPEAKER_00
start=404.1s stop=415.4s speaker_SPEAKER_00
start=414.7s stop=418.2s speaker_SPEAKER_03
start=419.7s stop=433.6s speaker_SPEAKER_00
start=434.1s stop=437.1s speaker_SPEAKER_00
start=437.5s stop=441.2s speaker_SPEAKER_00
start=441.5s stop=445.3s speaker_SPEAKER_00
start=446.4s stop=446.6s speaker_SPEAKER_00
start=447.2s stop=460.5s speaker_SPEAKER_00
start=460.7s stop=466.4s speaker_SPEAKER_00
start=467.3s stop=467.8s speaker_SPEAKER_00
start=468.6s stop=470.5s speaker_SPEAKER_00
start=471.0s stop=484.3s speaker_SPEAKER_00
start=484.3s stop=484.7s speaker_SPEAKER_03
start=484.7s stop=489.0s speaker_SPEAKER_00
start=487.3s stop=487.6s speaker_SPEAKER_03
start=490.3s stop=490.6s speaker_SPEAKER_00
start=491.4s stop=491.8s speaker_SPEAKER_00
start=493.1s stop=494.1s speaker_SPEAKER_03
start=494.1s stop=496.0s speaker_SPEAKER_00
start=494.2s stop=494.6s speaker_SPEAKER_03
start=496.7s stop=506.1s speaker_SPEAKER_00
start=506.7s stop=517.8s speaker_SPEAKER_00
start=515.1s stop=515.5s speaker_SPEAKER_02
start=519.3s stop=520.3s speaker_SPEAKER_00
start=520.5s stop=529.8s speaker_SPEAKER_00
start=526.5s stop=526.7s speaker_SPEAKER_03
start=531.2s stop=535.1s speaker_SPEAKER_01
start=532.5s stop=532.8s speaker_SPEAKER_00
start=535.1s stop=535.5s speaker_SPEAKER_03
start=535.7s stop=536.6s speaker_SPEAKER_03
start=537.0s stop=537.5s speaker_SPEAKER_03
start=538.3s stop=538.7s speaker_SPEAKER_00
start=539.5s stop=542.2s speaker_SPEAKER_00
start=542.6s stop=543.3s speaker_SPEAKER_00
start=543.5s stop=544.3s speaker_SPEAKER_03
start=544.6s stop=545.5s speaker_SPEAKER_00
start=544.7s stop=544.7s speaker_SPEAKER_03
start=545.7s stop=546.0s speaker_SPEAKER_03""")
        response = model.generate_content(request,
                                    request_options={"timeout": 600})
        return response

class MeetingProfessionalism:
    def __init__(self):
        pass
    def prompt(self, frames, audio):
        prompt = """You have been provided with timestamped image frames and an audio recording of a recent meeting. Rate the meeting and speech professsionalism and eloquence, mostly in terms of speech and ways of talking. Observe the language and tone used by participants throughout the meeting. Note very excessive instances of casual or unprofessional language such as 'like', 'um', or other non-professional thing, but don't be too strict. Keep it general, avoid specific names."""
    # #prompt = "What was the first thing said in the meeting?"
    # # Set the model to Gemini 1.5 Pro.
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    # Make the LLM request.
        request = make_request(prompt, frames)
        request.append(audio)
        response = model.generate_content(request,
                                    request_options={"timeout": 600})
        return response

class MeetingRespect:
    def __init__(self):
        pass
    def prompt(self, frames, audio):
        prompt = """You have been provided with timestamped image frames and an audio file of a recent meeting. Closely monitor interactions among participants to identify clear instances of interruptions or rudeness, or abrupt cutting off. Pay particular attention to tone of voice, how participants handle interruptions, and the nature of disagreements. Highlight significant interactions that demonstrate obvious disrespect or disruption to the flow of conversation.Provide examples of these interactions and suggest how they might be addressed in future meetings."""
    # #prompt = "What was the first thing said in the meeting?"
    # # Set the model to Gemini 1.5 Pro.
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    # Make the LLM request.
        request = make_request(prompt, frames)
        request.append(audio)
        response = model.generate_content(request,
                                    request_options={"timeout": 600})
        return response

class MeetingProductivity:
    def __init__(self):
        pass
    def prompt(self, frames, audio, speaker_frequencies):
        prompt = "You have been provided with timestamped image frames and an audio file of a recent meeting, along with a dictionary detailing speaker frequencies. Analyze the content of the discussion to determine the proportion of time spent on relevant versus unrelated topics. Identify and quantify moments where the discussion veers off-topic to assess overall meeting productivity in percentages."
    # #prompt = "What was the first thing said in the meeting?"
    # # Set the model to Gemini 1.5 Pro.
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    # Make the LLM request.
        request = make_request(prompt, frames)
        request.append(audio)
        request.append(str(speaker_frequencies))
#         request.append("""start=3.6s stop=4.7s speaker_SPEAKER_00
# start=4.9s stop=6.1s speaker_SPEAKER_00
# start=7.3s stop=11.2s speaker_SPEAKER_00
# start=13.1s stop=17.1s speaker_SPEAKER_01
# start=17.5s stop=18.0s speaker_SPEAKER_00
# start=18.0s stop=18.1s speaker_SPEAKER_01
# start=18.9s stop=20.6s speaker_SPEAKER_00
# start=21.4s stop=21.9s speaker_SPEAKER_00
# start=21.5s stop=22.0s speaker_SPEAKER_01
# start=22.5s stop=22.9s speaker_SPEAKER_00
# start=22.6s stop=24.7s speaker_SPEAKER_01
# start=25.2s stop=26.6s speaker_SPEAKER_01
# start=26.6s stop=26.7s speaker_SPEAKER_02
# start=28.2s stop=31.2s speaker_SPEAKER_02
# start=30.1s stop=30.2s speaker_SPEAKER_00
# start=30.3s stop=30.3s speaker_SPEAKER_00
# start=31.2s stop=31.8s speaker_SPEAKER_00
# start=32.3s stop=35.8s speaker_SPEAKER_00
# start=32.4s stop=32.8s speaker_SPEAKER_02
# start=34.6s stop=35.6s speaker_SPEAKER_02
# start=36.4s stop=37.2s speaker_SPEAKER_02
# start=37.3s stop=37.9s speaker_SPEAKER_00
# start=38.5s stop=42.1s speaker_SPEAKER_02
# start=40.5s stop=40.6s speaker_SPEAKER_00
# start=42.7s stop=50.6s speaker_SPEAKER_02
# start=50.6s stop=51.6s speaker_SPEAKER_01
# start=51.8s stop=52.1s speaker_SPEAKER_01
# start=52.6s stop=54.2s speaker_SPEAKER_01
# start=53.0s stop=53.2s speaker_SPEAKER_00
# start=54.6s stop=57.6s speaker_SPEAKER_00
# start=58.7s stop=59.4s speaker_SPEAKER_00
# start=60.5s stop=63.2s speaker_SPEAKER_00
# start=64.0s stop=64.9s speaker_SPEAKER_00
# start=64.0s stop=66.4s speaker_SPEAKER_02
# start=66.8s stop=68.2s speaker_SPEAKER_00
# start=67.5s stop=68.1s speaker_SPEAKER_02
# start=68.2s stop=68.2s speaker_SPEAKER_02
# start=68.2s stop=68.2s speaker_SPEAKER_00
# start=68.6s stop=70.0s speaker_SPEAKER_02
# start=68.8s stop=70.9s speaker_SPEAKER_00
# start=71.2s stop=72.0s speaker_SPEAKER_02
# start=73.1s stop=73.6s speaker_SPEAKER_02
# start=74.2s stop=75.0s speaker_SPEAKER_02
# start=75.0s stop=75.4s speaker_SPEAKER_00
# start=76.6s stop=79.9s speaker_SPEAKER_02
# start=80.7s stop=81.1s speaker_SPEAKER_00
# start=81.4s stop=81.6s speaker_SPEAKER_02
# start=82.4s stop=84.8s speaker_SPEAKER_00
# start=85.2s stop=86.9s speaker_SPEAKER_00
# start=87.5s stop=90.3s speaker_SPEAKER_00
# start=91.0s stop=91.4s speaker_SPEAKER_00
# start=92.0s stop=92.7s speaker_SPEAKER_00
# start=95.0s stop=96.8s speaker_SPEAKER_02
# start=98.9s stop=101.9s speaker_SPEAKER_02
# start=102.4s stop=104.7s speaker_SPEAKER_02
# start=102.9s stop=104.0s speaker_SPEAKER_00
# start=105.2s stop=106.2s speaker_SPEAKER_00
# start=107.5s stop=109.0s speaker_SPEAKER_00
# start=110.0s stop=117.4s speaker_SPEAKER_00
# start=117.6s stop=118.7s speaker_SPEAKER_00
# start=119.0s stop=121.4s speaker_SPEAKER_00
# start=121.6s stop=124.4s speaker_SPEAKER_00
# start=125.1s stop=125.6s speaker_SPEAKER_00
# start=126.1s stop=126.7s speaker_SPEAKER_02
# start=126.8s stop=127.3s speaker_SPEAKER_00
# start=128.2s stop=128.6s speaker_SPEAKER_00
# start=128.2s stop=130.6s speaker_SPEAKER_02
# start=131.4s stop=132.3s speaker_SPEAKER_02
# start=132.9s stop=133.1s speaker_SPEAKER_00
# start=133.9s stop=134.4s speaker_SPEAKER_02
# start=134.9s stop=135.7s speaker_SPEAKER_00
# start=136.1s stop=136.6s speaker_SPEAKER_00
# start=136.8s stop=137.5s speaker_SPEAKER_02
# start=138.0s stop=139.3s speaker_SPEAKER_00
# start=141.1s stop=141.6s speaker_SPEAKER_00
# start=142.2s stop=143.6s speaker_SPEAKER_00
# start=144.4s stop=145.0s speaker_SPEAKER_01
# start=145.9s stop=149.4s speaker_SPEAKER_01
# start=149.8s stop=152.9s speaker_SPEAKER_01
# start=151.5s stop=152.4s speaker_SPEAKER_00
# start=152.9s stop=152.9s speaker_SPEAKER_02
# start=152.9s stop=153.0s speaker_SPEAKER_01
# start=153.0s stop=153.0s speaker_SPEAKER_02
# start=153.0s stop=154.2s speaker_SPEAKER_00
# start=154.6s stop=156.1s speaker_SPEAKER_02
# start=154.8s stop=155.6s speaker_SPEAKER_01
# start=157.5s stop=158.1s speaker_SPEAKER_01
# start=158.3s stop=159.2s speaker_SPEAKER_01
# start=158.6s stop=158.8s speaker_SPEAKER_02
# start=158.8s stop=158.9s speaker_SPEAKER_00
# start=158.9s stop=158.9s speaker_SPEAKER_02
# start=159.9s stop=161.2s speaker_SPEAKER_01
# start=160.2s stop=161.1s speaker_SPEAKER_02
# start=161.4s stop=170.6s speaker_SPEAKER_01
# start=166.0s stop=166.7s speaker_SPEAKER_00
# start=173.3s stop=173.7s speaker_SPEAKER_00
# start=173.3s stop=174.7s speaker_SPEAKER_01
# start=174.7s stop=174.7s speaker_SPEAKER_02
# start=175.3s stop=176.6s speaker_SPEAKER_02
# start=176.8s stop=177.3s speaker_SPEAKER_00
# start=177.1s stop=177.9s speaker_SPEAKER_02
# start=178.5s stop=181.5s speaker_SPEAKER_00
# start=178.9s stop=179.1s speaker_SPEAKER_02
# start=182.1s stop=183.7s speaker_SPEAKER_01
# start=182.6s stop=183.4s speaker_SPEAKER_02
# start=183.7s stop=183.8s speaker_SPEAKER_02
# start=184.3s stop=184.3s speaker_SPEAKER_01
# start=184.3s stop=184.4s speaker_SPEAKER_02
# start=184.4s stop=184.4s speaker_SPEAKER_01
# start=185.2s stop=186.0s speaker_SPEAKER_02
# start=186.0s stop=186.1s speaker_SPEAKER_01
# start=186.7s stop=191.2s speaker_SPEAKER_01
# start=187.0s stop=187.5s speaker_SPEAKER_02
# start=191.4s stop=203.6s speaker_SPEAKER_01
# start=197.6s stop=198.3s speaker_SPEAKER_02
# start=204.3s stop=206.9s speaker_SPEAKER_01
# start=204.7s stop=204.9s speaker_SPEAKER_00
# start=207.0s stop=210.9s speaker_SPEAKER_01
# start=211.9s stop=213.4s speaker_SPEAKER_01
# start=212.3s stop=212.8s speaker_SPEAKER_00
# start=212.8s stop=212.9s speaker_SPEAKER_02
# start=214.2s stop=216.8s speaker_SPEAKER_01
# start=220.5s stop=221.0s speaker_SPEAKER_00
# start=222.1s stop=227.1s speaker_SPEAKER_00
# start=227.6s stop=228.1s speaker_SPEAKER_00
# start=227.7s stop=228.8s speaker_SPEAKER_02
# start=229.0s stop=229.9s speaker_SPEAKER_02
# start=229.1s stop=229.7s speaker_SPEAKER_00
# start=230.1s stop=232.0s speaker_SPEAKER_00
# start=232.0s stop=235.3s speaker_SPEAKER_02
# start=234.0s stop=234.4s speaker_SPEAKER_00
# start=236.2s stop=237.5s speaker_SPEAKER_00
# start=237.6s stop=238.6s speaker_SPEAKER_02
# start=240.1s stop=241.1s speaker_SPEAKER_02
# start=242.2s stop=243.1s speaker_SPEAKER_02
# start=242.3s stop=250.4s speaker_SPEAKER_01
# start=243.2s stop=243.4s speaker_SPEAKER_02
# start=250.9s stop=251.3s speaker_SPEAKER_01
# start=250.9s stop=251.5s speaker_SPEAKER_02""")
        response = model.generate_content(request,
                                    request_options={"timeout": 600})
        return response

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
    request.append(get_timestamp(file.display_name))
    request.append(file)
  return request

def upload_video(prefix, df, do_upload):

    shutil.rmtree(FRAME_EXTRACTION_DIRECTORY)
    os.mkdir(FRAME_EXTRACTION_DIRECTORY)

    video_file_name = prefix + '.mp4'
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

def get_frames_and_audio(test_file):
  df = pd.read_csv('file_manifest.csv')

  df = df[df['origin_name'] == test_file]

  frame_uids = df[df['display_name'].str.contains('jpg')]['uid'].to_list()
  audio_uid = df[df['display_name'].str.contains('mp3')]['uid'].iloc[0]

  frames = []
  for frame in frame_uids:
      frames.append(genai.get_file(frame))

  audio = genai.get_file(audio_uid)

  return frames, audio

def get_speaker_frequencies(audio_file):
  # .wav file is passed in
  pass

def get_frames():

  # Specify the path of your pickle file
  pickle_file_path = 'sample3_frame_handles.pkl'

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



if __name__ == '__main__':
    
    
    # df = pd.DataFrame({'origin_name': [], "display_name": [], "uid": []})
    # prefixes = ['testSample1', 'testSample2', 'testSample3', 'testSample4', 'testSample5']
    # for prefix in prefixes:
    #    df = upload_video(prefix, df, do_upload=genai.upload_file)
    #df.to_csv("file_manifest.csv")


    #frames, audio = get_frames_and_audio("testSample1")
    frames = get_frames()
    audio = get_audio("testSample3")
    print(frames)
    print(audio)

    #meeting_feedback = MeetingProductivity()
    # meeting_feedback = MeetingRespect()
    # meeting_feedback = MeetingProfessionalism()
    meeting_feedback = MeetingParticipation()
    meeting_feedback = MeetingEffort()

    response = meeting_feedback.prompt(frames, audio)
    print(response.text)







