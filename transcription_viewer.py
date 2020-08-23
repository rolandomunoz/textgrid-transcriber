import wx, wx.media, wx.adv
import poll_praat
import time
import os

class MainFrame(wx.Frame):
  
  def __init__(self):
    super().__init__(None, title = 'Transcription Viewer')
    TranscriptionPanel(self)
    self.Show()

class TranscriptionPanel(wx.Panel):
  
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent

    # Menubar
    menuBar = wx.MenuBar()
    
    fileMenu = wx.Menu()
    menuBar.Append(fileMenu, "&File")

    about_item = fileMenu.Append(wx.ID_ANY, 'About...')
    preferences_item = fileMenu.Append(wx.ID_ANY, 'Preferences')
    quit_item = fileMenu.Append(wx.ID_ANY, 'Quit\tctrl+Q')

    viewMenu = wx.Menu()
    menuBar.Append(viewMenu, "&View")
    zoom_all_item = viewMenu.Append(wx.ID_ANY, 'Show all')
    zoom_in_item = viewMenu.Append(wx.ID_ANY, 'Zoom in\tCtrl+I')
    zoom_out_item = viewMenu.Append(wx.ID_ANY, 'Zoom out\tCtrl+O')
    zoom_selection_item = viewMenu.Append(wx.ID_ANY, 'Zoom to selection\tCtrl+N')
    zoom_back_item = viewMenu.Append(wx.ID_ANY, 'Zoom back\tCtrl+B')

    viewMenu.AppendSeparator()
    previous_tier_item = viewMenu.Append(wx.ID_ANY, 'Select previous tier\tAlt+Up')
    next_tier_item = viewMenu.Append(wx.ID_ANY, 'Select next tier\tAlt+Down')
    previous_interval_item = viewMenu.Append(wx.ID_ANY, 'Select previous interval\tAlt+Left')
    next_interval_item = viewMenu.Append(wx.ID_ANY, 'Select next interval\tAlt+Right')

    textMenu = wx.Menu()
    menuBar.Append(textMenu, "&Text")
    pull_text_item = textMenu.Append(wx.ID_ANY, 'Refresh\tCtrl+R')
    push_text_item = textMenu.Append(wx.ID_ANY, 'Push\tCtrl+P')
    
    parent.SetMenuBar(menuBar)

    parent.Bind(wx.EVT_MENU, self.quit, quit_item)
    parent.Bind(wx.EVT_MENU, self.preferences, preferences_item)
    parent.Bind(wx.EVT_MENU, self.about, about_item)

    parent.Bind(wx.EVT_MENU, self.zoom_all, zoom_all_item)
    parent.Bind(wx.EVT_MENU, self.zoom_in, zoom_in_item)
    parent.Bind(wx.EVT_MENU, self.zoom_out, zoom_out_item)
    parent.Bind(wx.EVT_MENU, self.zoom_selection, zoom_selection_item)
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
      (wx.ACCEL_CTRL, ord('n'), zoom_selection_item.GetId()),
      (wx.ACCEL_CTRL, ord('b'), zoom_back_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_UP, previous_tier_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_DOWN, next_tier_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_LEFT, previous_interval_item.GetId()),
      (wx.ACCEL_ALT, wx.WXK_RIGHT, next_interval_item.GetId()),
      (wx.ACCEL_CTRL, ord('r'), pull_text_item.GetId()),
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

    play_btn.Bind(wx.EVT_BUTTON, self.play_sound)
    pause_btn.Bind(wx.EVT_BUTTON, self.pause_sound)
    stop_btn.Bind(wx.EVT_BUTTON, self.stop_sound)
    
    # Layout
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    
    horizontal_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
    
    horizontal_sizer1.Add(play_btn)
    horizontal_sizer1.Add(pause_btn)
    horizontal_sizer1.Add(stop_btn)
    
    main_sizer.Add(horizontal_sizer1, proportion = 0)
    main_sizer.Add(self.control, proportion = 1, flag = wx.ALL|wx.EXPAND, border = 5)

    self.SetSizer(main_sizer)
    main_sizer.Fit(parent)
    self.Layout()

  def preferences(self, event):
    with wx.TextEntryDialog(self, 'Sendpraat directory', 'Text Entry') as dlg:
      dlg.SetValue('sendpraat.exe')
      if dlg.ShowModal() == wx.ID_OK:
        print('hello')
  
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
    poll_praat.extract_audio_file()
    #self.sound.SetPlaybackRate(2.0)
    
    self.sound.Load(poll_praat.TEMP_AUDIO)
    
#    print(self.sound.GetPlaybackRate())
    self.sound.Play()

  def pause_sound(self, event):
    self.sound.Pause()
        
  def stop_sound(self, event):
    self.sound.Stop()
  
  def pull_text(self, event):
    self._pull_text()
  
  def _pull_text(self):
    text = poll_praat.get_text()
    text = text.replace(r'\n', '\n')
    text = text.replace('**', 'ININT')

    self.control.SetValue(text)
    
  def _push_text(self):
    text = self.control.GetValue()

    text = text.replace('\n', r'\n')
    text = text.replace('**', 'ININT')

    poll_praat.push_interval_text(text)
    time.sleep(0.1)

  def push_text(self, event):
    self._push_text()
        
  def next_tier(self, event):
    self._push_text()
    poll_praat.next_tier()
    self._pull_text()
    
  def previous_tier(self, event):
    self._push_text()    
    poll_praat.previous_tier()
    self._pull_text()

  def next_interval(self, event):
    self._push_text()
    poll_praat.next_interval()
    self._pull_text()
    
  def previous_interval(self, event):
    self._push_text()    
    poll_praat.previous_interval()
    self._pull_text()

  def zoom_all(self, event):
    poll_praat.zoom_all()

  def zoom_in(self, event):
    poll_praat.zoom_in()

  def zoom_out(self, event):
    poll_praat.zoom_out()

  def zoom_selection(self, event):
    poll_praat.zoom_selection()

  def zoom_back(self, event):
    poll_praat.zoom_back()

if __name__ == '__main__':  
  app = wx.App(redirect = False)
  frame = MainFrame()
  app.MainLoop()
