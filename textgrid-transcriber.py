import wx, wx.adv
import sendpraat
import os
import configparser
import audioplayer
import psutil

class MainFrame(wx.Frame):

  def __init__(self):
    # Init gui
    super().__init__(None)
    TranscriptionPanel(self)
    self.SetTitle('TextGrid Transcriber')
    self.SetSize((400, 500))
    self.SetIcon(wx.Icon(os.path.join('img', 'logo.ico')))
    self.Show()

class TranscriptionPanel(wx.Panel):

  def __init__(self, parent):
    super().__init__(parent)

    # Init variables
    self.CONFIG_FILE_DIR = 'settings.ini'
    self.parent = parent
    sendpraat_dir = self.get_setting('Settings', 'sendpraat_dir')
    self.skip_back = float(self.get_setting('Playback', 'jump_back'))
    self.sendpraat = sendpraat.SendPraat(sendpraat_dir)
    
    # INIT GUI
    self.add_MenuBar()
    self.statusbar = parent.CreateStatusBar(1)
    self.add_Panel()
    self.shortcuts(False)
    self.init_app(None)

#    self.parent.ToggleWindowStyle(wx.STAY_ON_TOP)

  def add_MenuBar(self):
    # Menubar
    menuBar = wx.MenuBar()

    fileMenu = wx.Menu()
    tgMenu = wx.Menu()
    playbackMenu = wx.Menu()

    menuBar.Append(fileMenu, "&Transcriber")
    menuBar.Append(tgMenu, "Text&Grid")
    menuBar.Append(playbackMenu, "&Playback")

    # Menubar > transcriber
    about_item = fileMenu.Append(wx.ID_ANY, '&About...')
    fileMenu.AppendSeparator()
    self.init_app_item = fileMenu.Append(wx.ID_ANY, '&Connect to TextGridEditor', kind= wx.ITEM_CHECK)
    self.on_top_item = fileMenu.Append(wx.ID_ANY, 'Show on &top\tF12', kind= wx.ITEM_CHECK)
    preferences_item = fileMenu.Append(wx.ID_ANY, '&Preferences...')
    fileMenu.AppendSeparator()
    quit_item = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl+Q')

    # Menubar > TextGrid
    zoom_all_item = tgMenu.Append(wx.ID_ANY, 'Show &all\tCtrl+E')
    zoom_in_item = tgMenu.Append(wx.ID_ANY, 'Zoom &in\tCtrl+I')
    zoom_out_item = tgMenu.Append(wx.ID_ANY, 'Zoom &out\tCtrl+O')
    zoom_to_selection_item = tgMenu.Append(wx.ID_ANY, 'Zoom to s&election\tCtrl+N')
    zoom_back_item = tgMenu.Append(wx.ID_ANY, 'Zoom &back\tCtrl+B')
    tgMenu.AppendSeparator()
    previous_tier_item = tgMenu.Append(wx.ID_ANY, 'Select &previous tier\tAlt+Up')
    next_tier_item = tgMenu.Append(wx.ID_ANY, 'Select &next tier\tAlt+Down')
    previous_interval_item = tgMenu.Append(wx.ID_ANY, 'Select p&revious interval\tAlt+Left')
    next_interval_item = tgMenu.Append(wx.ID_ANY, 'Select ne&xt interval\tAlt+Right')
    tgMenu.AppendSeparator()
    previous_vinterval_item = tgMenu.Append(wx.ID_ANY, 'Sele&ct previous vinterval\tCtrl+Y')
    next_vinterval_item = tgMenu.Append(wx.ID_ANY, 'Selec&t next vinterval\tCtrl+U')

    tgMenu.AppendSeparator()
    pull_text_item = tgMenu.Append(wx.ID_ANY, 'Pu&ll\tCtrl+L', 'Pull text to the Text editor')
    push_text_item = tgMenu.Append(wx.ID_ANY, 'Pu&sh\tCtrl+S', 'Push text to interval')

    # Menubar > Playback
    play_item = playbackMenu.Append(wx.ID_ANY,'&Play\tCtrl+G')
    stop_item = playbackMenu.Append(wx.ID_ANY,'&Stop\tCtrl+H')
    jump_back_item = playbackMenu.Append(wx.ID_ANY,'&Jump back\tCtrl+J')
    skip_forward_item = playbackMenu.Append(wx.ID_ANY,'&Skip forward\tCtrl+K')
    playbackMenu.AppendSeparator()
    playback_settings_item = playbackMenu.Append(wx.ID_ANY,'&Settings...')

    self.parent.SetMenuBar(menuBar)

    self.menu_items = (
      about_item, self.init_app_item, self.on_top_item, preferences_item, quit_item,
      zoom_all_item, zoom_in_item, zoom_out_item, zoom_to_selection_item, zoom_back_item,
      previous_tier_item, next_tier_item, previous_interval_item, next_interval_item, previous_vinterval_item, next_vinterval_item,
      pull_text_item, push_text_item,
      play_item, stop_item, jump_back_item, skip_forward_item, playback_settings_item
      )

    self.menu_methods = (
      self.about, self.init_app, self.on_top, self.preferences, self.close,
      self.zoom_all, self.zoom_in, self.zoom_out, self.zoom_to_selection, self.zoom_back,
      self.previous_tier, self.next_tier, self.previous_interval, self.next_interval, self.previous_vinterval, self.next_vinterval,
      self.pull_text, self.push_text,
      self.play_sound, self.stop_sound, self.jump_back_sound, self.skip_forward_sound, self.playback_settings
      )

     # Bind events
    for item, method in zip(self.menu_items, self.menu_methods):
      self.parent.Bind(wx.EVT_MENU, method, item)

    self.table = [
      (wx.ACCEL_CTRL, ord('E'), zoom_all_item.GetId()),
      (wx.ACCEL_CTRL, ord('I'), zoom_in_item.GetId()),
      (wx.ACCEL_CTRL, ord('O'), zoom_out_item.GetId()),
      (wx.ACCEL_CTRL, ord('N'), zoom_to_selection_item.GetId()),
      (wx.ACCEL_CTRL, ord('B'), zoom_back_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_UP, previous_tier_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_DOWN, next_tier_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_LEFT, previous_interval_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_RIGHT, next_interval_item.GetId()),
      (wx.ACCEL_CTRL, ord('L'), pull_text_item.GetId()),
      (wx.ACCEL_CTRL, ord('S'), push_text_item.GetId()),
      (wx.ACCEL_CTRL, ord('U'), next_vinterval_item.GetId()),
      (wx.ACCEL_CTRL, ord('Y'), previous_vinterval_item.GetId()),
      (wx.ACCEL_CTRL, ord('G'), play_item.GetId()),
      (wx.ACCEL_CTRL, ord('H'), stop_item.GetId()),
      (wx.ACCEL_CTRL, ord('J'), jump_back_item.GetId()),
      (wx.ACCEL_CTRL, ord('K'), skip_forward_item.GetId())
    ]

  def add_Panel(self):

    # Playback controls
    PLAY_IMG = os.path.join('img', 'play.png')
    PAUSE_IMG = os.path.join('img', 'pause.png')
    STOP_IMG = os.path.join('img','stop.png')
    JUMP_BACK_IMG = os.path.join('img','jump_back.png')
    SKIP_FORWARD_IMG = os.path.join('img\skip_forward.png')

    main_box = wx.BoxSizer(wx.VERTICAL)
    hbox1 = wx.BoxSizer(wx.HORIZONTAL)

    #Playback menu
    # Audio player
    bmp_play = wx.Bitmap(PLAY_IMG)
    play_btn = wx.BitmapButton(self, wx.ID_ANY, bitmap = bmp_play)
    hbox1.Add(play_btn)

    bmp_stop = wx.Bitmap(STOP_IMG)
    stop_btn = wx.BitmapButton(self, wx.ID_ANY, bitmap = bmp_stop)
    hbox1.Add(stop_btn)

    bmp_jumpback = wx.Bitmap(JUMP_BACK_IMG)
    jumpback_btn = wx.BitmapButton(self, wx.ID_ANY, bitmap = bmp_jumpback)
    hbox1.Add(jumpback_btn)

    bmp_skip = wx.Bitmap(SKIP_FORWARD_IMG)
    skip_btn = wx.BitmapButton(self, wx.ID_ANY, bitmap = bmp_skip)
    hbox1.Add(skip_btn)

    self.sld_speed = wx.Slider(self, value=5, minValue=1, maxValue=9, style=wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SL_SELRANGE)
    hbox1.Add(self.sld_speed)

    # Text Entry
    self.text = wx.TextCtrl(self, wx.ID_ANY, style = wx.TE_MULTILINE)
    font1 = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL, False)
    self.text.SetFont(font1)

    # Layout
    main_box.Add(hbox1)
    main_box.Add(self.text, 1, wx.ALL|wx.EXPAND, border = 5)
    self.SetSizer(main_box)
    main_box.Fit(self.parent)
    self.Layout()

    self.panel_items = (
      play_btn, stop_btn, jumpback_btn, skip_btn, self.sld_speed
      )

    self.panel_methods = (
      self.play_sound, self.stop_sound, self.jump_back_sound, self.skip_forward_sound
      )

    # Bind events
    for item, method in zip(self.panel_items, self.panel_methods):
      self.Bind(wx.EVT_BUTTON, method, item)

  def on_top(self, event):
    if self.on_top_item.IsChecked():
      self.parent.SetWindowStyle(wx.STAY_ON_TOP)
    else:
      self.parent.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)
      
  def shortcuts(self, activate = True):
    # Shortcuts
    if activate:
      self.accel_tbl = wx.AcceleratorTable(self.table)
    else:
      self.accel_tbl = wx.AcceleratorTable([])

  def is_praat_running(self):
    for proc in psutil.process_iter():
        try:
          if proc.name() == self.sendpraat.PRAAT_NAME:
            return True
        except:
          pass
    return False

  def init_app(self, event):

    if self.init_app_item.IsChecked():

      if self.is_praat_running():
        self.shortcuts(True)
        self.sendpraat.io_preferences()

        for item in self.menu_items:
          item.Enable(True)

        for item in self.panel_items:
          item.Enable(True)
        
        self.pull_text(event = None)
        self.parent.Bind(wx.EVT_ACTIVATE, self.pull_text)
        self.sld_speed.Bind(wx.EVT_SCROLL, self.speed_mod)
        self.statusbar.SetStatusText('Status: Connected')
      else:
        self.init_app_item.Check(False)
    else:
      self.shortcuts(False)

      for item in self.menu_items:
        item.Enable(False)

      for item in self.panel_items:
        item.Enable(False)

      for index in range(0, 5):
        self.menu_items[index].Enable(True)

      self.parent.Bind(wx.EVT_ACTIVATE, None)
      self.statusbar.SetStatusText('Status: Disconnected')

  def get_config(self):
    config = configparser.ConfigParser()
    config.read(self.CONFIG_FILE_DIR)
    return config

  def get_setting(self, section, setting):
    config = self.get_config()
    return config.get(section, setting)

  def update_settings(self, section, setting, value):
    config = self.get_config()
    config.set(section, setting, value)
    with open(self.CONFIG_FILE_DIR, "w") as config_file:
      config.write(config_file)

  def preferences(self, event):
    sendpraat_dir = self.get_setting('Settings', 'sendpraat_dir')

    with wx.TextEntryDialog(self, 'Sendpraat directory', 'Preferences') as dlg:
      dlg.SetValue(sendpraat_dir)
      if dlg.ShowModal() == wx.ID_OK:
        sendpraat_dir = dlg.GetValue()
        self.update_settings('Settings', 'SENDPRAAT_DIR', sendpraat_dir)
        self.sendpraat.update_sendpraat_dir(sendpraat_dir)

  def about(self, event):
    info = wx.adv.AboutDialogInfo()
    icon = wx.Icon(os.path.join('img','logo.png'), wx.BITMAP_TYPE_PNG)
    info.SetIcon(icon)
    info.SetName('TextGrid Transcriber')
    info.SetVersion('0.1')
    info.SetCopyright('(C) 2020 Rolando Muñoz Aramburú')
    info.SetWebSite('https://github.com/rolandomunoz/textgrid-transcriber')
    info.AddArtist('Aaron Torres Castillo')
    info.SetLicense('GNU General Public License v3.0')
    wx.adv.AboutBox(info)

  def close(self, event):
    self.parent.Destroy()
      
  def speed_mod(self, event):
    try:
      if self.audio.state.name == 'PLAYING':
        current_position = self.audio.position
        self.load_audio()
        self.audio.play()
        self.audio.position = current_position - 0.1
    except:
      pass
    
  def load_audio(self):
    if os.path.exists(self.sendpraat.AUDIOFILE_DIR):
      os.remove(self.sendpraat.AUDIOFILE_DIR)

    value = self.sld_speed.GetValue()

    midpoint = 5

    if value > midpoint:
      speed = 1 - (value - midpoint)*0.05
    elif value < midpoint:
      speed = (midpoint - value)*0.25 + 1
    elif value == midpoint:
      speed = 1
    self.sendpraat.extract_audio_file(speed)

    try:
      self.audio = audioplayer.AudioPlayer(self.sendpraat.AUDIOFILE_DIR)
    except:
      pass

  def close_audio(self):
    try:
      self.audio.close()
    except:
      pass

  def play_sound(self, event):
    try:
      if self.audio.duration == self.audio.position:
        self.audio.state.name = 'STOPPED'

      if self.audio.state.name == 'PAUSED':
        self.audio.resume()
      elif self.audio.state.name == 'PLAYING':
        self.audio.pause()
      else:
        self.load_audio()
        try:
          self.audio.play(mode = 0)
        except:
          pass
    except AttributeError:
      self.load_audio()
      try:
        self.audio.play(mode = 0)
      except:
        pass
        
  def stop_sound(self, event):
    try:
      self.audio.stop()
    except AttributeError:
      pass

  def jump_back_sound(self, event):
    try:
      current_position = self.audio.position
      self.audio.position = current_position - self.skip_back
      self.audio.resume()
    except AttributeError:
      pass

  def skip_forward_sound(self, event):
    try:
      current_position = self.audio.position
      self.audio.position = current_position + self.skip_back
      self.audio.resume()
    except AttributeError:
      pass

  def playback_settings(self, event):
    jump_back = self.get_setting('Playback', 'jump_back')

    with wx.TextEntryDialog(self, 'Playback', 'jump_back') as dlg:
      dlg.SetValue(jump_back)
      if dlg.ShowModal() == wx.ID_OK:
        jump_back = dlg.GetValue()
        self.update_settings('Playback', 'jump_back', jump_back)
        self.sendpraat.update_sendpraat_dir(jump_back)

  def check_textgrideditor(self, event):
    self.sendpraat.check_textgrideditor()

  def pull_text(self, event):
    text = self.sendpraat.pull_interval_text()
    text = text.replace(r'\n', '\n')
    text = text.replace('**', 'ININT')
    try:
      self.text.SetValue(text)
    except:
      pass

  def push_text(self, event):
    text = self.text.GetValue()
    text = text.replace('"', '""')
    text = text.replace('\n', r'\n')
    text = text.replace('**', 'ININT')
    self.sendpraat.push_interval_text(text)

  def next_tier(self, event):
    self.close_audio()
    self.push_text(event = None)
    self.sendpraat.next_tier()
    self.pull_text(event = None)

  def previous_tier(self, event):
    self.close_audio()
    self.push_text(event = None)
    self.sendpraat.previous_tier()
    self.pull_text(event = None)

  def next_interval(self, event):
    self.close_audio()
    self.push_text(event = None)
    self.sendpraat.next_interval()
    self.pull_text(event = None)

  def previous_interval(self, event):
    self.close_audio()
    self.push_text(event = None)
    self.sendpraat.previous_interval()
    self.pull_text(event = None)

  def next_vinterval(self, event):
    self.close_audio()
    self.push_text(event = None)
    self.sendpraat.next_vinterval()
    self.pull_text(event = None)

  def previous_vinterval(self, event):
    self.close_audio()
    self.push_text(event = None)
    self.sendpraat.previous_vinterval()
    self.pull_text(event = None)

  def zoom_all(self, event):
    self.sendpraat.zoom_all()

  def zoom_in(self, event):
    self.sendpraat.zoom_in()

  def zoom_out(self, event):
    self.sendpraat.zoom_out()

  def zoom_to_selection(self, event):
    self.sendpraat.zoom_to_selection()

  def zoom_back(self, event):
    self.sendpraat.zoom_back()

if __name__ == '__main__':
  app = wx.App(redirect = False)
  frame = MainFrame()
  app.MainLoop()