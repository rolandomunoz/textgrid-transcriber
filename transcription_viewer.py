import wx, wx.media, wx.adv
import sendpraat
import time
import os
import json
import simpleaudio

class MainFrame(wx.Frame):
  
  def __init__(self):
    # Init gui
    super().__init__(None)
    TranscriptionPanel(self)
    self.SetTitle('TextGrid Transcriber')
    self.SetSize((400, 500))
    self.Show()

class TranscriptionPanel(wx.Panel):
  
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    # Init data
    pref = self.read_preferences()
    self.sendpraat = sendpraat.SendPraat(pref['sendpraat_dir'])

    # Init variables
    self.first_play = False
    
    # Menubar
    menuBar = wx.MenuBar()
    
    fileMenu = wx.Menu()
    menuBar.Append(fileMenu, "&File")

    about_item = fileMenu.Append(wx.ID_ANY, 'About...')
    preferences_item = fileMenu.Append(wx.ID_ANY, 'Preferences...')
    quit_item = fileMenu.Append(wx.ID_ANY, 'Quit\tctrl+Q')

    viewMenu = wx.Menu()
    menuBar.Append(viewMenu, "&View")
    zoom_all_item = viewMenu.Append(wx.ID_ANY, 'Show all')
    zoom_in_item = viewMenu.Append(wx.ID_ANY, 'Zoom in\tCtrl+I')
    zoom_out_item = viewMenu.Append(wx.ID_ANY, 'Zoom out\tCtrl+O')
    zoom_to_selection_item = viewMenu.Append(wx.ID_ANY, 'Zoom to selection\tCtrl+N')
    zoom_back_item = viewMenu.Append(wx.ID_ANY, 'Zoom back\tCtrl+B')

    viewMenu.AppendSeparator()
    previous_tier_item = viewMenu.Append(wx.ID_ANY, 'Select previous tier\tAlt+Up')
    next_tier_item = viewMenu.Append(wx.ID_ANY, 'Select next tier\tAlt+Down')
    previous_interval_item = viewMenu.Append(wx.ID_ANY, 'Select previous interval\tAlt+Left')
    next_interval_item = viewMenu.Append(wx.ID_ANY, 'Select next interval\tAlt+Right')

    textMenu = wx.Menu()
    menuBar.Append(textMenu, "&Text")
    pull_text_item = textMenu.Append(wx.ID_ANY, 'Pull\tCtrl+L')
    push_text_item = textMenu.Append(wx.ID_ANY, 'Push\tCtrl+P')
    
    parent.SetMenuBar(menuBar)

    parent.Bind(wx.EVT_MENU, self.quit, quit_item)
    parent.Bind(wx.EVT_MENU, self.preferences, preferences_item)
    parent.Bind(wx.EVT_MENU, self.about, about_item)

    parent.Bind(wx.EVT_MENU, self.zoom_all, zoom_all_item)
    parent.Bind(wx.EVT_MENU, self.zoom_in, zoom_in_item)
    parent.Bind(wx.EVT_MENU, self.zoom_out, zoom_out_item)
    parent.Bind(wx.EVT_MENU, self.zoom_to_selection, zoom_to_selection_item)
    parent.Bind(wx.EVT_MENU, self.zoom_back, zoom_back_item)

    parent.Bind(wx.EVT_MENU, self.previous_tier, previous_tier_item)
    parent.Bind(wx.EVT_MENU, self.next_tier, next_tier_item)
    parent.Bind(wx.EVT_MENU, self.previous_interval, previous_interval_item)
    parent.Bind(wx.EVT_MENU, self.next_interval, next_interval_item)

    parent.Bind(wx.EVT_MENU, self.pull_text, pull_text_item)
    parent.Bind(wx.EVT_MENU, self.push_text, push_text_item)
        
    # Shortcuts
    accel_tbl = wx.AcceleratorTable([
      #(wx.ACCEL_CTRL, ord('a'), zoom_all_item.GetId()),
      (wx.ACCEL_CTRL, ord('i'), zoom_in_item.GetId()),
      (wx.ACCEL_CTRL, ord('o'), zoom_out_item.GetId()),
      (wx.ACCEL_CTRL, ord('n'), zoom_to_selection_item.GetId()),
      (wx.ACCEL_CTRL, ord('b'), zoom_back_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_UP, previous_tier_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_DOWN, next_tier_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_LEFT, previous_interval_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_RIGHT, next_interval_item.GetId()),
      (wx.ACCEL_CTRL, ord('l'), pull_text_item.GetId()),
      (wx.ACCEL_CTRL, ord('q'), quit_item.GetId()),
      (wx.ACCEL_CTRL, ord('p'), push_text_item.GetId())
    ])
    self.SetAcceleratorTable(accel_tbl)
    
    self.sound = wx.media.MediaCtrl(self)
    
    # Text Entry
    self.control = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE)
        
    play_btn = wx.Button(self, label = '&Play')
    pause_btn = wx.Button(self, label = 'P&ause')
    stop_btn = wx.Button(self, label = '&Stop')
    self.sld = wx.Slider(self, value=10, minValue=1, maxValue=20, style=wx.SL_HORIZONTAL)
    self.txt = wx.StaticText(self, label = '1')
    
    play_btn.Bind(wx.EVT_BUTTON, self.play_sound)
    pause_btn.Bind(wx.EVT_BUTTON, self.pause_sound)
    stop_btn.Bind(wx.EVT_BUTTON, self.stop_sound)
    self.sld.Bind(wx.EVT_SCROLL, self.on_slider_scroll)
    
    # Layout
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    
    horizontal_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
    
    horizontal_sizer1.Add(play_btn)
    horizontal_sizer1.Add(pause_btn)
    horizontal_sizer1.Add(stop_btn)
    horizontal_sizer1.Add(self.sld)
    horizontal_sizer1.Add(self.txt)
    
    main_sizer.Add(horizontal_sizer1, proportion = 0)
    main_sizer.Add(self.control, proportion = 1, flag = wx.ALL|wx.EXPAND, border = 5)

    self.SetSizer(main_sizer)
    main_sizer.Fit(parent)
    self.Layout()

  def on_slider_scroll(self, event):
    obj = event.GetEventObject()
    val = obj.GetValue()
    self.txt.SetLabel(str(val/10))
    
  def read_preferences(self):
    with open('preferences.json', mode = 'r') as f:
      return json.load(f)

  def write_preferences(self, dict_preferences):
    with open("preferences.json", mode = "w") as f:
      json.dump(dict_preferences, f)
 
  def preferences(self, event):
    pref = self.read_preferences()

    with wx.TextEntryDialog(self, 'Sendpraat directory', 'Preferences') as dlg:
      dlg.SetValue(pref['sendpraat_dir'])
      if dlg.ShowModal() == wx.ID_OK:
        sendpraat_dir = dlg.GetValue()
        pref['sendpraat_dir'] = sendpraat_dir
        self.write_preferences(pref)
        self.sendpraat.set_sendpraat_dir(sendpraat_dir)
        
  def about(self, event):
    info = wx.adv.AboutDialogInfo()
    info.SetName('TextGrid Transcriber')
    info.SetVersion('0.1')
    info.SetCopyright('(C) 2020 Rolando Muñoz Aramburú')
    info.SetWebSite('https://github.com/rolandomunoz/textgrid-transcriber')
    info.SetLicense('GNU General Public License v3.0')
    wx.adv.AboutBox(info)
  
  def quit(self, event):
    self.parent.Destroy()

  def play_sound(self, event):
    if os.path.exists(self.sendpraat.AUDIOFILE_DIR):
      os.remove(self.sendpraat.AUDIOFILE_DIR)
      
    value = self.sld.GetValue()/10
    self.sendpraat.extract_audio_file(value)

    wave_obj = simpleaudio.WaveObject.from_wave_file(self.sendpraat.AUDIOFILE_DIR)
    self.play_obj = wave_obj.play()
    self.first_play = True
    
  def pause_sound(self, event):
    if self.first_play:
      self.sound.Pause()
        
  def stop_sound(self, event):
    if self.play_obj.is_playing():
      self.play_obj.stop()

  def pull_text(self, event):
    self._pull_text()

  def push_text(self, event):
    self._push_text()

  def _pull_text(self):
    text = self.sendpraat.pull_interval_text()
    text = text.replace(r'\n', '\n')
    text = text.replace('**', 'ININT')

    self.control.SetValue(text)
    
  def _push_text(self):
    text = self.control.GetValue()

    text = text.replace('\n', r'\n')
    text = text.replace('**', 'ININT')

    self.sendpraat.push_interval_text(text)
    time.sleep(0.1)

  def next_tier(self, event):
    self._push_text()
    self.sendpraat.next_tier()
    self._pull_text()
    
  def previous_tier(self, event):
    self._push_text()
    self.sendpraat.previous_tier()
    self._pull_text()

  def next_interval(self, event):
    self._push_text()
    self.sendpraat.next_interval()
    self._pull_text()
    
  def previous_interval(self, event):
    self._push_text()    
    self.sendpraat.previous_interval()
    self._pull_text()

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
