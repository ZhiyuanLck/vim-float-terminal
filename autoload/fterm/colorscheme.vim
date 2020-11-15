let s:default_highlights = {
      \ "fterm_hl_border": {
      \   "ctermfg": 10,
      \   },
      \ "fterm_hl_termline_info": {
      \   "ctermfg": 255,
      \   "ctermbg": 245,
      \   },
      \ "fterm_hl_termline_normal": {
      \   "ctermfg": 252,
      \   "ctermbg": 240,
      \   },
      \ "fterm_hl_termline_current": {
      \   "ctermfg": 0,
      \   "ctermbg": 84,
      \   },
      \ "fterm_hl_termline_sep_a": {
      \   "ctermfg": 255,
      \   "ctermbg": 245,
      \   },
      \ "fterm_hl_termline_sep_b": {
      \   "ctermfg": 255,
      \   "ctermbg": 245,
      \   },
      \ "fterm_hl_termline_sep_c": {
      \   "ctermfg": 255,
      \   "ctermbg": 245,
      \   },
      \ "fterm_hl_terminal_body": {
      \   "ctermfg": "fg",
      \   "ctermbg": "bg",
      \   },
      \ "fterm_hl_termline_body": {
      \   "ctermfg": "fg",
      \   "ctermbg": "bg",
      \   },
      \ }

function! s:get_cmd(name, hl) abort
  let cmd = map(a:hl, v:key.'='.v:val)
  let cmd = join(cmd, ' ')
  return 'highlight! '.a:name.' '.cmd
endfunction

function! fterm#colorscheme#set() abort
  let hl_list = get(g:, "fterm_highlights", s:default_highlights)
  for [name, hl] in items(hl_list)
    let cmd = "highlight! ".name
    for [k, v] in items(hl)
      let cmd .= printf(" %s=%s", k, v)
    endfor
    exec cmd
  endfor
endfunction
