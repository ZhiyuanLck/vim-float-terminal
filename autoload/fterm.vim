let g:ft_py = "py3 "
exec g:ft_py "<< END"
import vim, sys
from pathlib import Path
cwd = vim.eval('expand("<sfile>:p:h")')
cwd = Path(cwd) / '..' / 'python'
cwd = cwd.resolve()
sys.path.insert(0, str(cwd))
from fterm.utils import *
from fterm.manager import *
END

let s:home = fnamemodify(resolve(expand('<sfile>:p')), ':h')
let s:script = fnamemodify(s:home . '/../bin', ':p')

if stridx($PATH, s:script) < 0
  let $PATH .= ':' . s:script
endif

function! fterm#py(cmd) abort
  exec g:ft_py "".cmd
endfunction

function! fterm#cmd(...) abort
  exec g:ft_py "fterm_manager.start(vimeval('a:000'))"
endfunction

function! fterm#complete(A, L, P) abort
  return ['new', 'toggle', 'kill', 'select', 'settitle', 'move']
endfunction

function! fterm#set_title() abort
  echohl WarningMsg
  let title = input('title: ')
  echohl None
  exec "FtermSetTitle ".title
endfunction

function! fterm#async_runner(opts) abort
  exec g:ft_py "fterm_manager.async_run()"
endfunction

function! fterm#edit(bufnr, path) abort
  exec g:ft_py printf("fterm_manager.edit_in_vim('%s')", a:path)
endfunction

function! fterm#map(modes, nore, args, lhs, rhs, block) abort
  let all_modes = 'nvxsoilct'
  for mode in split(a:modes == '' ? 'nvo' : a:modes, '\zs')
    if stridx(all_modes, mode) != -1
      if a:block
        let old_map = maparg(a:lhs, mode, 0, 1)
      endif
      exec printf("%s%smap %s %s %s",
            \ mode, a:nore ? 'nore' : '', a:args, a:lhs, a:rhs
            \ )
      if a:block
        let g:fterm_blocked_mapping = get(g:, "fterm_blocked_mapping", [])
        call add(g:fterm_blocked_mapping, {'map': maparg(a:lhs, mode, 0, 1), 'mode': mode, 'old_map': old_map})
        if old_map == {}
          exec mode."unmap ".a:lhs
        else
          call mapset(mode, 0, old_map)
        endif
      endif
    endif
  endfor
endfunction

function! s:set_map(map_dict) abort
endfunction

function! fterm#block_map() abort
  for map_dict in g:fterm_blocked_mapping
    call mapset(map_dict.mode, 0, map_dict.map)
  endfor
endfunction

function! fterm#restore_map() abort
  for map_dict in g:fterm_blocked_mapping
    let old_map = map_dict.old_map
    let map = map_dict.map
    let mode = map_dict.mode
    try
      if old_map == {}
        exec mode."unmap ".map.lhsraw
      else
        call mapset(mode, 0, old_map)
      endif
    catch /^Vim\%((\a\+)\)\=:E31:/
    endtry
  endfor
endfunction

function! fterm#custom_map() abort
  try
    for m in g:fterm_custom_mapping
      call fterm#map(m[0], m[1], m[2], m[3], m[4], m[5])
    endfor
  catch
    echohl Error
    echom "wrong cumstom mapping in 'g:fterm_custom_mapping'!"
    echohl None
  endtry
endfunction

augroup FtermWinLeave
  autocmd!
  autocmd WinLeave * exec g:ft_py "fterm_manager.winleave_cb()"
augroup END
