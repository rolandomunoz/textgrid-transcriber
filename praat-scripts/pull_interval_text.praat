form Log destiny
  sentence log_file
endform

objects# = selected#()

tg = selected("TextGrid")
editor: tg

editor_info$ = Editor info
selected_tier = extractNumber( editor_info$, "Selected tier: ")

label$ = Get label of interval
tmin = Get start of selection
tmax = Get end of selection

endeditor
selectObject: tg

interval_left = Get interval boundary from time: selected_tier, tmin
interval_right= Get interval boundary from time: selected_tier, tmax

if interval_left == 0 and interval_right == 0
  interval_diff = interval_right - interval_left
  if interval_diff != 1
    label$ = ""
  endif
endif

writeFile: log_file$, label$
selectObject: objects#
