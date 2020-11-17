function! fterm#issue#patch_821990() abort
  if has('patch-8.2.1990') && !has('patch-8.2.1997')
    echohl Error
    echom "You're using vim with patch-8.2.1990 which has serious issue of terminal popup that was fixed in patch-8.2.1997. Please update to latest vim to ensure that vim has patch-8.2.1997."
    echohl None
    return 1
  endif
endfunction
