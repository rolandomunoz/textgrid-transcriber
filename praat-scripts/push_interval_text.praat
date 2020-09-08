form Push text
  sentence Text
endform

include check_error_message.praat

objects# = selected#()

tg = selected("TextGrid")
editor: tg

editor_info$ = Editor info
selected_tier = extractNumber( editor_info$, "Selected tier: ")

tmin = Get start of selection
tmax = Get end of selection

endeditor
selectObject: tg

interval_left = Get interval at time: selected_tier, tmin

Set interval text: selected_tier, interval_left, text$

selectObject: objects#
