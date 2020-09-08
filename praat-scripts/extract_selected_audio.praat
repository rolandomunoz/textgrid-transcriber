form Extract audio file
  sentence soundfile
  real speed
endform

include check_error_message.praat

objects# = selected#()
tg = selected("TextGrid")
editor: tg
sd = nocheck noprogress Extract selected sound (time from 0)
if sd == undefined
  exitScript()
endif
endeditor

new_sd = noprogress Lengthen (overlap-add): 75, 600, speed
noprogress Scale peak: 0.99
noprogress Save as WAV file: soundfile$

removeObject: new_sd, sd
selectObject: objects#