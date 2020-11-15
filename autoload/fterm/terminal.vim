function! fterm#terminal#kill(bufnr) abort
  let job = term_getjob(a:bufnr)
  if job == v:null
    return
  endif
  if job_status(job) !=# 'dead'
    call job_stop(job)
  endif
  if bufexists(a:bufnr)
    execute a:bufnr . 'bwipeout!'
  endif
endfunction
