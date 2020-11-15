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

noremap <silent><leader>c :<c-u>FtermNew<cr>
tnoremap <silent><leader>c <c-\><c-n>:<c-u>FtermNew<cr>
noremap <silent><leader>s :<c-u>FtermToggle<cr>
tnoremap <silent><leader>s <c-\><c-n>:<c-u>FtermToggle<cr>
noremap <silent><leader>k :<c-u>FtermKill<cr>
tnoremap <silent><leader>k <c-\><c-n>:<c-u>FtermKill<cr>
noremap <silent><leader>a :<c-u>FtermKillAll<cr>
tnoremap <silent><leader>a <c-\><c-n>:<c-u>FtermKillAll<cr>
tnoremap <silent><leader>, <c-\><c-n>:<c-u>call fterm#set_title()<cr>
tnoremap <silent><leader>tl <c-\><c-n>:<c-u>FtermMoveRight 1<cr>
tnoremap <silent><leader>th <c-\><c-n>:<c-u>FtermMoveLeft 1<cr>
tnoremap <silent><leader>ta <c-\><c-n>:<c-u>FtermMoveStart<cr>
tnoremap <silent><leader>te <c-\><c-n>:<c-u>FtermMoveEnd<cr>
for i in range(1, 9)
  exec printf('tnoremap <silent><m-%d> <c-\><c-n>:<c-u>FtermSelect %d<cr>', i, i)
endfor

" 异步关闭窗口
