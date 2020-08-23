import subprocess
import os
import re
import time
import platform
import codecs

class SendPraat():
  def __init__(self, sendpraat_dir):

    # Dir variables
    self._cwd = os.getcwd()
    self._sendpraat_dir = sendpraat_dir
    self._transcriber_dir = os.path.join(self._cwd, 'transcriber-local')
    self._logfile = os.path.join(self._transcriber_dir, 'log.txt')
    self._audiofile = os.path.join(self._transcriber_dir, 'temp.wav')

    # Create local dir
    if not os.path.exists(self._transcriber_dir):
      os.mkdir(self._transcriber_dir)

    # Praat script pieces

    self.sp_start = [self._sendpraat_dir, '0', 'praat']
    if platform.system() == 'Windows':
      self.sp_start.pop(1)

    self.sp_textgrideditor = self.sp_start + [
      'tg = selected("TextGrid")',
      'editor: tg'
    ]

    self.sp_write2log = [
      'info$ = Editor info',
      'text$ = nocheck Get label of interval',
      'writeFile: "{}", info$ + "Text: " + text$'.format(self._logfile)
    ]

  def set_dir(self, sendpraat_dir):
    self._sendpraat_dir = sendpraat_dir

  def remove_log(self):
    if os.path.exists(self._logfile):
      os.remove(self._logfile)

  def remove_tempaudio(self):
    if os.path.exists(self._audiofile):
      os.remove(self._audiofile)

  def play_sound(self, tmin, tmax):
    subprocess.run(self.sp_start + ['Play: {}, {}'.format(tmin, tmax)])

  def pause_sound(self):
    subprocess.run(self.sp_textgrideditor + ['Play or stop'])

  def stop_sound(self):
    subprocess.run(self.sp_textgrideditor + ['Interrupt playing'])

  def next_tier():
    self.remove_log()
    subprocess.run(self.sp_textgrideditor + ['Select next tier'] + self.sp_write2log)

  def previous_tier(self):
    self.remove_log()
    subprocess.run(self.sp_textgrideditor + ['Select previous tier'] + self.sp_write2log)

  def next_interval(self):
    self.remove_log()
    subprocess.run(self.sp_textgrideditor + ['Select next interval'] + self.sp_write2log)

  def previous_interval(self):
    self.remove_log()
    subprocess.run(self.sp_textgrideditor + ['Select previous interval'] + self.sp_write2log)

  def zoom_all(self):
    subprocess.run(self.sp_textgrideditor + ['Show all'])

  def zoom_in(self):
    subprocess.run(self.sp_textgrideditor + ['Zoom in'])

  def zoom_out(self):
    subprocess.run(self.sp_textgrideditor + ['Zoom out'])

  def zoom_selection(self):
    subprocess.run(self.sp_textgrideditor + ['Zoom to selection'])

  def zoom_back(self):
    subprocess.run(self.sp_textgrideditor + ['Zoom back'])

  def push_interval_text(self, text):
    subprocess.run(self.sp_textgrideditor + [
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

  def pull_interval_text(self):
    self.write_editor2log()
    while True:
      if os.path.exists(self._logfile):
        editor = self.load_editor_info()
        break
      time.sleep(0.1)
    return editor['Text']
    
  def extract_audio_file(self):
    self.remove_tempaudio()
    subprocess.run(self.sp_textgrideditor + [
    'info$ = Editor info',
    'tmin = extractNumber(info$, "Selection start: ")',
    'tmax = extractNumber(info$, "Selection end: ")',
    'Save selected sound as WAV file: "{}"'.format(self._audiofile)
    ])

    while True:
      if os.path.exists(self._audiofile):
        break
      time.sleep(0.1)

  def write_editor2log(self):
    self.remove_log()
    subprocess.run(self.sp_textgrideditor + self.sp_write2log)

  def load_editor_info(self):
    editor_info = dict()
    encoding = self.detect_encoding(self._logfile)
    with open(self._logfile, mode = 'r', encoding = encoding) as log:
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

  def detect_encoding(self, f):
    """
    * This function was taken from https://github.com/kylebgorman/textgrid/blob/master/textgrid/textgrid.py
    All credits correspond to his respective author.
    This helper method returns the file encoding corresponding to path f.
    This handles UTF-8, which is itself an ASCII extension, so also ASCII.
    """
    encoding = 'ascii'
    try:
      with codecs.open(f, 'r', encoding='utf-16') as source:
        source.readline()  # Read one line to ensure correct encoding
    except UnicodeError:
      try:
        with codecs.open(f, 'r', encoding='utf-8-sig') as source: #revised utf-8 to utf-8-sig for utf-8 with byte order mark (BOM)  
          source.readline()  # Read one line to ensure correct encoding
      except UnicodeError:
        with codecs.open(f, 'r', encoding='ascii') as source:
          source.readline()  # Read one line to ensure correct encoding
      else:
        encoding = 'utf-8-sig' #revised utf-8 to utf-8-sig for utf-8 with byte order mark (BOM) 
    else:
      encoding = 'utf-16'
    return encoding
  
if __name__ == '__main__':
  sp = SendPraat(r'C:\Users\lab\Desktop\textgrid-transcriber\sendpraat.exe')
