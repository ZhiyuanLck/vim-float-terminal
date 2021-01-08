let s:cterm_fg = synIDattr(hlID("Normal"), "fg", "cterm") ? "fg" : 251
let s:cterm_bg = synIDattr(hlID("Normal"), "bg", "cterm") ? "bg" : 235
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
      \   "ctermfg": s:cterm_fg,
      \   "ctermbg": s:cterm_bg,
      \   },
      \ "fterm_hl_termline_body": {
      \   "ctermfg": s:cterm_fg,
      \   "ctermbg": s:cterm_fg,
      \   },
      \ }

function! s:get_cmd(name, hl) abort
  let cmd = map(a:hl, v:key.'='.v:val)
  let cmd = join(cmd, ' ')
  return 'highlight! '.a:name.' '.cmd
endfunction

function! fterm#colorscheme#set() abort
  let hl_list = s:default_highlights
  let extra_list = get(g:, "fterm_highlights", {})
  call extend(hl_list, extra_list)
  for [name, hl] in items(hl_list)
    let cmd = "highlight! ".name
    for [k, v] in items(hl)
      let cmd .= printf(" %s=%s", k, v)
    endfor
    exec cmd
  endfor
endfunction
