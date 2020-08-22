import subprocess
import os
import re
import time
import socket
import threading

CWD = os.getcwd()
TRANSCRIBER_DIRECTORY = os.path.join(CWD, 'transcriber')
TEMP_AUDIO = os.path.join(TRANSCRIBER_DIRECTORY,'extracted_audio.wav')
LOGFILE = os.path.join(TRANSCRIBER_DIRECTORY, 'log.txt')

if not os.path.exists(TRANSCRIBER_DIRECTORY):
  os.mkdir('transcriber')

SENDPRAAT = ['sendpraat', '0', 'praat',
 'tg = selected("TextGrid")',
 'editor: tg'
]

WRITE_TO_LOG = [
  'info$ = Editor info',
  'text$ = Get label of interval',
  'writeFile: "{}", info$ + "Text: " + text$'.format(LOGFILE)
]

def remove_log():
  if os.path.exists(LOGFILE):
    os.remove(LOGFILE)

def remove_extracted_audio():
  if os.path.exists(TEMP_AUDIO):
    os.remove(TEMP_AUDIO)
    
def play_sound(tmin, tmax):
  subprocess.run(SENDPRAAT + ['Play: {}, {}'.format(tmin, tmax)])

def pause_sound():
  subprocess.run(SENDPRAAT + ['editor: tg', 'Play or stop'])

def stop_sound():
  subprocess.run(SENDPRAAT + ['Interrupt playing'])

def next_tier():
  remove_log()
  subprocess.run(SENDPRAAT + ['Select next tier'] + WRITE_TO_LOG)

def previous_tier():
  remove_log()
  subprocess.run(SENDPRAAT + ['Select previous tier'] + WRITE_TO_LOG)

def next_interval():
  remove_log()
  subprocess.run(SENDPRAAT + ['Select next interval'] + WRITE_TO_LOG)

def previous_interval():
  remove_log()
  subprocess.run(SENDPRAAT + ['Select previous interval'] + WRITE_TO_LOG)

def zoom_all():
  subprocess.run(SENDPRAAT + ['Show all'])

def zoom_in():
  subprocess.run(SENDPRAAT + ['Zoom in'])

def zoom_out():
  subprocess.run(SENDPRAAT + ['Zoom out'])

def zoom_selection():
  subprocess.run(SENDPRAAT + ['Zoom to selection'])

def zoom_back():
  subprocess.run(SENDPRAAT + ['Zoom back'])

def push_interval_text(text):
  subprocess.run(SENDPRAAT + [
  'info$ = Editor info',
  'tmin = extractNumber(info$, "Selection start: ")',
  'tmax = extractNumber(info$, "Selection end: ")',
  'selected_tier = extractNumber(info$, "Selected tier:")',
  'tmid = (tmin + tmax)*0.5',
  'endeditor',
  'selectObject: tg',
  'interval = Get interval at time: selected_tier, tmid',
  'Set interval text: selected_tier, interval, "{}"'.format(text),
  'editor: tg'
  ])

def extract_audio_file():
  remove_extracted_audio()    
  subprocess.run(SENDPRAAT + [
  'info$ = Editor info',
  'tmin = extractNumber(info$, "Selection start: ")',
  'tmax = extractNumber(info$, "Selection end: ")',
  'Save selected sound as WAV file: "{}"'.format(TEMP_AUDIO)
  ])
  
  while True:
    if os.path.exists(TEMP_AUDIO):
      break
    time.sleep(0.1)

def get_text():
  write_editor_to_log()
  while True:
    if os.path.exists(LOGFILE):
      editor = pull_editor_info()
      break
    time.sleep(0.1)
  return editor['Text']
  
def write_editor_to_log():
  remove_log()
  subprocess.run(SENDPRAAT + WRITE_TO_LOG)

def pull_editor_info():
  editor_info = dict()
  with open(LOGFILE, mode = 'r') as log:
    lines = log.readlines()
    
    for line in lines:
      line = line.rstrip()
      if line == '':
        continue

      key, value = line.split(':', 1)
      value = value.strip()
      
      if re.match('^[0-9]', value):
        value = value.split(' ')[0]
        if value.isnumeric():
          value = float(value)

      editor_info[key] = value
  return editor_info
  
if __name__ == '__main__':
  next_interval()
  text = get_text()
  print(text)
