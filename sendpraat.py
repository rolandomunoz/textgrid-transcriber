import subprocess
import os
import re
import time
import platform

class SendPraat():
  def __init__(self, sendpraat_dir):
    self.init_variables(sendpraat_dir)
    
  def init_variables(self, sendpraat_dir):
    # Dir variables
    self._CWD = os.getcwd()
    self.SENDPRAAT_DIR = sendpraat_dir
    self.SCRIPTS_DIR = os.path.join(self._CWD, 'praat-scripts')
    self.LOCAL_DIR = os.path.join(self._CWD, 'transcriber-local')
    self.LOGFILE_DIR = os.path.join(self.LOCAL_DIR, 'log.txt')
    self.AUDIOFILE_DIR = os.path.join(self.LOCAL_DIR, 'temp.wav')

    self.PUSH_TEXT = os.path.join(self.SCRIPTS_DIR, 'push_interval_text.praat')
    self.PULL_TEXT = os.path.join(self.SCRIPTS_DIR, 'pull_interval_text.praat')
    self.NEXT_TIER = os.path.join(self.SCRIPTS_DIR, 'next_tier.praat')
    self.PREVIOUS_TIER = os.path.join(self.SCRIPTS_DIR, 'previous_tier.praat')
    self.NEXT_INTERVAL = os.path.join(self.SCRIPTS_DIR, 'next_interval.praat')
    self.PREVIOUS_INTERVAL = os.path.join(self.SCRIPTS_DIR, 'previous_interval.praat')
    self.ZOOM_ALL = os.path.join(self.SCRIPTS_DIR, 'zoom_all.praat')
    self.ZOOM_BACK = os.path.join(self.SCRIPTS_DIR, 'zoom_back.praat')
    self.ZOOM_IN = os.path.join(self.SCRIPTS_DIR, 'zoom_in.praat')
    self.ZOOM_OUT = os.path.join(self.SCRIPTS_DIR, 'zoom_out.praat')
    self.ZOOM_TO_SELECTION = os.path.join(self.SCRIPTS_DIR, 'zoom_to_selection.praat')
    self.EXTRACT_AUDIOFILE = os.path.join(self.SCRIPTS_DIR, 'extract_selected_audio.praat')
    # Create local dir
    if not os.path.exists(self.LOCAL_DIR):
      os.mkdir(self.LOCAL_DIR)
  
    self.SENDPRAAT_CMD = [self.SENDPRAAT_DIR, '0', 'praat']
    if platform.system() == 'Windows':
      self.SENDPRAAT_CMD.pop(1)

  def set_sendpraat_dir(self, sendpraat_dir):
    self.SENDPRAAT_DIR = sendpraat_dir
    
  def remove_log(self):
    if os.path.exists(self.LOGFILE_DIR):
      os.remove(self.LOGFILE_DIR)

  def next_tier(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.NEXT_TIER)])
    
  def previous_tier(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.PREVIOUS_TIER)])
    
  def next_interval(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.NEXT_INTERVAL)])
    
  def previous_interval(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.PREVIOUS_INTERVAL)])
    
  def zoom_all(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.ZOOM_ALL)])

  def zoom_in(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.ZOOM_IN)])

  def zoom_out(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.ZOOM_OUT)])

  def zoom_to_selection(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.ZOOM_TO_SELECTION)])

  def zoom_back(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {}'.format(self.ZOOM_BACK)])

  def push_interval_text(self, text):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {} {}'.format(self.PUSH_TEXT, text)])

  def pull_interval_text(self):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {} {}'.format(self.PULL_TEXT, self.LOGFILE_DIR)])
    with open(self.LOGFILE_DIR, encoding = 'utf-8') as f:
      log = f.readline()
    return log
 
  def extract_audio_file(self, speed):
    subprocess.run(self.SENDPRAAT_CMD + ['execute {} {} {}'.format(self.EXTRACT_AUDIOFILE, self.AUDIOFILE_DIR, speed)])
  
if __name__ == '__main__':
  sp = SendPraat(r'C:\Users\lab\Desktop\textgrid-transcriber\sendpraat.exe')
  sp.extract_audio_file()