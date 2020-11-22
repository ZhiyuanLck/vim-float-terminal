function! s:init_var(name, default) abort
  let var = get(g:, 'fterm_'.a:name, a:default)
  exec "let g:fterm_".a:name." = var"
endfunction

" attributes
call s:init_var('shell', &shell)
call s:init_var('width', 0.75)
call s:init_var('height', 0.75)
call s:init_var('autoquit', 0)
call s:init_var('exclude_cmdline', 1)
call s:init_var('exclude_statusline', 1)
call s:init_var('exclude_tabline', 1)
call s:init_var('exclude_signcolumn', 0)
call s:init_var('open_cmd', 'tabedit')
call s:init_var('noquit', ['\v(\w|/)*bash$', '\v(\w|/)*zsh$', '\v(\w|/)*ksh$', '\v(\w|/)*csh$', '\v(\w|/)*tcsh$'])
call s:init_var('use_root', 1)
call s:init_var('root_marker', ['.root', '.git', '.svn', '.hg', '.project'])
call s:init_var('root_search_level', 5)
call s:init_var('expanduser', 1)
" termline
call s:init_var('borderchars',
      \ ['─', '│', '─', '│', '┌', '┐', '┘', '└'])
call s:init_var('termline_pos', 'outertop')
call s:init_var('title', 'fterm')
call s:init_var('title_max_width', 8)
call s:init_var('termline_sep', '')
" highlights
call s:init_var('hl_terminal_border', ['fterm_hl_terminal_border'])
call s:init_var('hl_termline_border', ['fterm_hl_termline_border'])
call s:init_var('hl_terminal_body', 'fterm_hl_terminal_body')
call s:init_var('hl_termline_body', 'fterm_hl_termline_body')
" key map
call s:init_var('disable_map', 0)
call s:init_var('map_select', 'm*')
call s:init_var('map_quit', 'q')

" 0 for tmap, 1 for tmap and map
function! s:init_map(map, lhs, rhs, mode=1) abort
  call s:init_var('map_'.a:map, a:lhs)
  exec "let l:lhs = g:fterm_map_".a:map
  if a:mode >= 0
    exec printf('tnoremap <silent>%s <c-\><c-n>:<c-u>%s<cr>', l:lhs, a:rhs)
  endif
  if a:mode >= 1
    exec printf("noremap <silent>%s :<c-u>%s<cr>", l:lhs, a:rhs)
  endif
endfunction

function! s:get_pattern() abort
  let mode = g:fterm_map_select
  if mode == 'm*'
    return {k -> '<m-'.k.'>'}
  elseif mode == 'c*'
    return {k -> '<c-'.k.'>'}
  else
    return {k -> mode.k}
  endif
endfunction

command! -bar -complete=customlist,fterm#complete -nargs=+ Fterm call fterm#cmd(<f-args>)
command! -bar -nargs=* FtermNew Fterm new <args>
command! -bar -nargs=* FtermToggle Fterm toggle <args>
command! -bar -nargs=? FtermKill Fterm kill <args>
command! -bar -nargs=0 FtermKillAll Fterm kill --all
command! -bar -nargs=1 FtermSelect Fterm select <args>
command! -bar -nargs=1 FtermSetTitle Fterm settitle <args>
command! -bar -nargs=1 FtermMoveTo Fterm move --to <args>
command! -bar -nargs=0 FtermMoveStart Fterm move --to 1
command! -bar -nargs=0 FtermMoveEnd Fterm move --end
command! -bar -nargs=1 FtermMoveLeft Fterm move --left <args>
command! -bar -nargs=1 FtermMoveRight Fterm move --right <args>
command! -bar -nargs=0 FtermQuit Fterm quit

if g:fterm_disable_map < 1
  call s:init_map('new',       '<leader>c',  'FtermNew')
  call s:init_map('toggle',    '<leader>s',  'FtermToggle')
  call s:init_map('kill',      '<leader>k',  'FtermKill')
  call s:init_map('killall',   '<leader>a',  'FtermKillAll')
  call s:init_map('settitle',  '<leader>,',  'call fterm#set_title()', 0)
  call s:init_map('moveright', '<leader>tl', 'FtermMoveRight 1',       0)
  call s:init_map('moveleft',  '<leader>th', 'FtermMoveLeft 1',        0)
  call s:init_map('movestart', '<leader>ta', 'FtermMoveStart 1',       0)
  call s:init_map('moveend',   '<leader>te', 'FtermMoveEnd',           0)
  for i in range(1, 10)
    let Pattern = s:get_pattern()
    let num = i % 10
    call s:init_map('select'.num, Pattern(num), 'FtermSelect '.num, 0)
  endfor
endif

" 异步关闭窗口
