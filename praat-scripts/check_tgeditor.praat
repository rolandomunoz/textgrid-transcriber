form Log destiny
  sentence log_file
endform

include check_error_message.praat

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

writeFile: log_file$, label$
selectObject: objects#
