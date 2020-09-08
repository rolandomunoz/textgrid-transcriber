import subprocess
import os
import re
import time
import psutil

class SendPraat():
  def __init__(self, sendpraat_dir):
    self.init_variables(sendpraat_dir)

  def init_variables(self, sendpraat_dir):
    # Dir variables
    self._CWD = os.getcwd()
    self.SENDPRAAT_DIR = sendpraat_dir
    self.SCRIPTS_DIR = os.path.join(self._CWD, 'praat-scripts')
    self.LOCAL_DIR = os.path.join(self._CWD, 'temp')
    self.LOGFILE_DIR = os.path.join(self.LOCAL_DIR, 'log.txt')
    self.AUDIOFILE_DIR = os.path.join(self.LOCAL_DIR, 'temp.wav')

    self.IO_PREFERENCES = os.path.join(self.SCRIPTS_DIR, 'io_preferences.praat')

    self.PUSH_TEXT = os.path.join(self.SCRIPTS_DIR, 'push_interval_text.praat')
    self.PULL_TEXT = os.path.join(self.SCRIPTS_DIR, 'pull_interval_text.praat')
    self.NEXT_TIER = os.path.join(self.SCRIPTS_DIR, 'next_tier.praat')
    self.PREVIOUS_TIER = os.path.join(self.SCRIPTS_DIR, 'previous_tier.praat')
    self.VNEXT_INTERVAL = os.path.join(self.SCRIPTS_DIR, 'vnext_interval.praat')
    self.VPREVIOUS_INTERVAL = os.path.join(self.SCRIPTS_DIR, 'vprevious_interval.praat')
    self.NEXT_INTERVAL = os.path.join(self.SCRIPTS_DIR, 'next_interval.praat')
    self.PREVIOUS_INTERVAL = os.path.join(self.SCRIPTS_DIR, 'previous_interval.praat')

    self.ZOOM_ALL = os.path.join(self.SCRIPTS_DIR, 'zoom_all.praat')
    self.ZOOM_BACK = os.path.join(self.SCRIPTS_DIR, 'zoom_back.praat')
    self.ZOOM_IN = os.path.join(self.SCRIPTS_DIR, 'zoom_in.praat')
    self.ZOOM_OUT = os.path.join(self.SCRIPTS_DIR, 'zoom_out.praat')
    self.ZOOM_TO_SELECTION = os.path.join(self.SCRIPTS_DIR, 'zoom_to_selection.praat')
    self.EXTRACT_AUDIOFILE = os.path.join(self.SCRIPTS_DIR, 'extract_selected_audio.praat')
    self.CREATE_NO_WINDOW = 0x08000000

    if psutil.WINDOWS:
      praat_name = 'Praat.exe'
    elif psutil.LINUX:
      praat_name = 'praat'
    elif psutil.MACOS:
      praat_name = 'praat'
    self.PRAAT_NAME = praat_name
    
    # Create local dir
    if not os.path.exists(self.LOCAL_DIR):
      os.mkdir(self.LOCAL_DIR)

    self.SENDPRAAT_CMD = self.get_sendpraat_cmd()

  def get_sendpraat_cmd(self):
    sendpraat_cmd = [self.SENDPRAAT_DIR, '0', 'praat']
    if psutil.WINDOWS:
      sendpraat_cmd.pop(1)
    return sendpraat_cmd

  def check_textgrideditor(self):
    pass

  def update_sendpraat_dir(self, sendpraat_dir):
    self.SENDPRAAT_DIR = sendpraat_dir
    self.get_sendpraat_cmd()

  def remove_log(self):
    if os.path.exists(self.LOGFILE_DIR):
      os.remove(self.LOGFILE_DIR)

  def io_preferences(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.IO_PREFERENCES)], creationflags=self.CREATE_NO_WINDOW)

  def next_tier(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.NEXT_TIER)], creationflags=self.CREATE_NO_WINDOW)

  def previous_tier(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.PREVIOUS_TIER)], creationflags=self.CREATE_NO_WINDOW)

  def next_interval(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.NEXT_INTERVAL)], creationflags=self.CREATE_NO_WINDOW)

  def previous_interval(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.PREVIOUS_INTERVAL)], creationflags=self.CREATE_NO_WINDOW)

  def next_vinterval(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.VNEXT_INTERVAL)], creationflags=self.CREATE_NO_WINDOW)

  def previous_vinterval(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.VPREVIOUS_INTERVAL)], creationflags=self.CREATE_NO_WINDOW)

  def zoom_all(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.ZOOM_ALL)], creationflags=self.CREATE_NO_WINDOW)

  def zoom_in(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.ZOOM_IN)], creationflags=self.CREATE_NO_WINDOW)

  def zoom_out(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.ZOOM_OUT)], creationflags=self.CREATE_NO_WINDOW)

  def zoom_to_selection(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.ZOOM_TO_SELECTION)], creationflags=self.CREATE_NO_WINDOW)

  def zoom_back(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}"'.format(self.ZOOM_BACK)], creationflags=self.CREATE_NO_WINDOW)

  def push_interval_text(self, text):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}", "{}"'.format(self.PUSH_TEXT, text)], creationflags=self.CREATE_NO_WINDOW)

  def pull_interval_text(self):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}", "{}"'.format(self.PULL_TEXT, self.LOGFILE_DIR)], creationflags=self.CREATE_NO_WINDOW)
    with open(self.LOGFILE_DIR, encoding = 'utf-8') as f:
      log = f.readline()
    return log

  def extract_audio_file(self, speed):
    subprocess.run(self.SENDPRAAT_CMD + [r'runScript: "{}", "{}", "{}"'.format(self.EXTRACT_AUDIOFILE, self.AUDIOFILE_DIR, speed)], creationflags=self.CREATE_NO_WINDOW)

if __name__ == '__main__':
  sp = SendPraat(r'C:\Users\rolan\Desktop\python_scripts\textgrid-transcriber\sendpraat.exe')
  #sp.extract_audio_file(2)
  sp.vnext_interval()
