form Push text
  sentence Text
endform

objects# = selected#()

tg = selected("TextGrid")
editor: tg

editor_info$ = Editor info
selected_tier = extractNumber( editor_info$, "Selected tier: ")

tmin = Get start of selection
tmax = Get end of selection

endeditor
selectObject: tg

interval_left = Get interval boundary from time: selected_tier, tmin
interval_right= Get interval boundary from time: selected_tier, tmax

if interval_left != 0 and interval_right != 0
  interval_diff = interval_right - interval_left
  if interval_diff == 1
    Set interval text: selected_tier, interval_left, text$
  endif
endif

selectObject: objects#
