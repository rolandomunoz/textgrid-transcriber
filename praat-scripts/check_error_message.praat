selected_objects# = selected#()

tg_exists = 0
size = size(selected_objects#)
for i to size
  selectObject: selected_objects#[i]
  id = nocheck selected("TextGrid")
  if not id == undefined
    tg_exists = 1
    i = size
  endif
endfor

if not tg_exists
  writeInfoLine: "Warning: No TextGrid selected"
  exitScript()
endif

tg = selected("TextGrid")
selectObject: tg
editor_exists = nocheck editor: tg
if editor_exists == undefined
  writeInfoLine: "Warning: No TextGridEditor with ID 'tg'"
  exitScript()
endif

selectObject: selected_objects#