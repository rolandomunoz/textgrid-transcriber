form Extract audio file
  sentence soundfile
  real speed
endform

objects# = selected#()
tg = selected("TextGrid")
editor: tg
sd = Extract selected sound (time from 0)
endeditor

new_sd = Lengthen (overlap-add): 75, 600, speed
Scale peak: 0.99
Save as WAV file: soundfile$

removeObject: new_sd, sd
selectObject: objects#