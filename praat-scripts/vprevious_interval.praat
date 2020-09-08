# Written by Rolando Muñoz Aramburú (2020)

include check_error_message.praat

all# = selected#()

tg = selected("TextGrid")
editor: tg
  info$ = Editor info
  selected_tier = extractNumber(info$, "Selected tier: ")
  window_start = extractNumber(info$, "Window start:")
  window_end = extractNumber(info$, "Window end:")
  margin = (window_end - window_start)*0.5
  length = Get selection length
  start_selection = Get start of selection
  end_selection = Get end of selection
  time = if length > 0 then (start_selection + end_selection)*0.5 else start_selection fi
endeditor

# Interval info
selectObject: tg
is_interval_tier = Is interval tier: selected_tier
if is_interval_tier
  interval = Get interval at time: selected_tier, time
  tmin = Get start time of interval: selected_tier, interval

  @previous_interval: selected_tier, tmin
  target_tier = previous_interval.return#[1]
  start_time = previous_interval.return#[2]
  end_time = previous_interval.return#[3]

  editor: tg
    @vmove_to_interval: selected_tier, target_tier, start_time, end_time
    Zoom: start_time - 3, end_time + 3
  endeditor
endif
selectObject: all#

procedure vmove_to_interval: .current_tier, .target_tier, .start_time, .end_time
  .tier_diff = .current_tier - .target_tier

  if .tier_diff > 0
    for .i to .tier_diff
      Select previous tier
    endfor
  elif .tier_diff < 0
    .tier_diff = abs(.tier_diff)
    for .i to .tier_diff
      Select next tier
    endfor
  endif
  Select: .start_time, .end_time
endproc

procedure previous_interval: .tier, .start_time
  .return# = {0, 0, 0}
  @previous_vinterval_at_start: .tier, .start_time
  if previous_vinterval_at_start.return#[1]
    .return# = previous_vinterval_at_start.return#
  else
    @previous_vinterval: .start_time
    .return# = previous_vinterval.return#
  endif
  if .return#[1] == 0
    .total_duration = Get total duration
    @previous_vinterval: .total_duration
    .return# = previous_vinterval.return#
  endif
endproc

#! ~~~ params
#!  Selection:
#!    - Object: TextGrid
#!  in:
#!    - start_time: the start start_time of the interval to be searched
#!  out:
#!    - return#: a vector with the following values {tier, start_time, end_time}. If nothing is found, then it returns {0, 0, 0}
#! ~~~
#! Find the next interval
#!
#!
procedure previous_vinterval: .start_time
  .return# = {0, 0, 0}
  .n_tiers = Get number of tiers
  .minimum_time = 0
  .tmin = .minimum_time
  .tmax = 0
  .tier = 0

  for .i_tier to .n_tiers
    .is_interval_tier = Is interval tier: .i_tier
    if .is_interval_tier
      is_boundary = Get interval boundary from time: .i_tier, .start_time
      if is_boundary
        .interval = Get low interval at time: .i_tier, .start_time
      else
        .interval = Get interval at time: .i_tier, .start_time
      endif
      @previous_non_empty_interval: .i_tier, .interval
      .previous_interval = previous_non_empty_interval.return
      if .previous_interval
        .tmin = Get start time of interval: .i_tier, .previous_interval
        if .tmin >= .minimum_time and not .start_time == .tmin
          .minimum_time = .tmin
          .tier = .i_tier
          .label$ = Get label of interval: .tier, .previous_interval
          .tmax = Get end time of interval: .tier, .previous_interval
        endif
      endif
    endif
  endfor
  .return# = {.tier, .minimum_time, .tmax}
endproc

#! ~~~ params
#!  Selection:
#!    - Object: TextGrid
#!  in:
#!    - tier: tier position from which the search starts
#!    - start_time: the start start_time of the interval to be searched
#!  out:
#!    - return#: a vector with the following values {tier, start_time, end_time}. If nothing is found, then it returns {0, 0, 0}
#! ~~~
#! Find the next interval in the following tiers that starts at a specific start_time.
#! If the that interval does not exist, it returns {0, 0, 0}
#!
procedure previous_vinterval_at_start: .tier, .start_time
  .return# = {0, 0, 0}
  .tier -= 1
  .continue = if .tier > 0 then 1 else 0 fi
  while .continue
    .is_interval_tier = Is interval tier: .tier
    if .is_interval_tier
      .interval = Get interval boundary from time: .tier, .start_time
      if .interval
        .label$ = Get label of interval: .tier, .interval
        .start_time = Get start time of interval: .tier, .interval
        .end_time = Get end time of interval: .tier, .interval

        if not .label$ == ""
          .return# = {.tier, .start_time, .end_time}
          .continue = 0
        endif
      endif
    endif
    .tier -= 1
    .continue = if .continue == 0 or .tier < 1 then 0 else 1 fi
  endwhile
endproc

#! ~~~ params
#!  Selection:
#!    - Object: TextGrid
#!  in:
#!    - tier: a tier position
#!    - interval: an interval position
#!  out:
#!    - return: the next non-empty interval. If there is no non-empty-interval, it returns 0
#! ~~~
#!
#!  Given a interval, find the next non-empty interval in the same tier. If nothing is found, it returns 0
#!
procedure previous_non_empty_interval: .tier, .interval
  .return = 0
  .continue = 1

  while .continue
    if .interval < 1
      .continue = 0
    else
      .label$ = Get label of interval: .tier, .interval
      if not .label$ == ""
        .return = .interval
        .continue = 0
      endif
    endif
    .interval -= 1
  endwhile
endproc
