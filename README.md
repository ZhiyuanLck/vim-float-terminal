# Fterm

<!--ts-->
   - [Fterm](#fterm)
      - [Screenshots](#screenshots)
      - [Installation](#installation)
      - [Usage](#usage)
      - [Global Variables](#global-variables)
      - [Command](#command)
      - [Default Mappings](#default-mappings)
      - [Default Highlights](#default-highlights)
      - [Support for <a href="https://github.com/skywind3000/asyncrun.vim">asyncrun.vim</a>](#support-for-asyncrunvim)
      - [Known issues](#known-issues)

<!-- Added by: zhiyuan, at: 2020年 11月 15日 星期日 18:58:51 CST -->

<!--te-->

Simple vim terminal in popup window with a termline.

## Screenshots

![buffer][1]

## Installation

Python3 support and vim-features `+popup`, `+terminal` are required.

```vim
Plug 'ZhiyuanLck/vim-float-terminal'
```

## Usage

```
usage: Fterm [-h] {new,toggle,kill,select,settitle,move} ...

positional arguments:
  {new,toggle,kill,select,settitle,move}
                        Fterm sub-command help

optional arguments:
  -h, --help            show this help message and exit

------------------------------------------------------------------------------

usage: Fterm new [-h] [--cmd CMD [CMD ...]] [--width width] [--height height]

optional arguments:
  -h, --help           show this help message and exit
  --cmd CMD [CMD ...]  run command in new terminal
  --width width        width of the popup window
  --height height      height of the popup window

------------------------------------------------------------------------------

usage: Fterm toggle [-h] [--cmd CMD [CMD ...]] [--width width]
                    [--height height]

optional arguments:
  -h, --help           show this help message and exit
  --cmd CMD [CMD ...]  run command in new terminal (only in creation mode)
  --width width        width of the popup window (only in creation mode)
  --height height      height of the popup window (only in creation mode)

------------------------------------------------------------------------------

usage: Fterm kill [-h] [--all]

optional arguments:
  -h, --help  show this help message and exit
  --all       kill all terminals

------------------------------------------------------------------------------

usage: Fterm select [-h] terminal_number

positional arguments:
  terminal_number  open the terminal by terminal number

optional arguments:
  -h, --help       show this help message and exit

------------------------------------------------------------------------------

usage: Fterm settitle [-h] title

positional arguments:
  title       set the title of current open terminal

optional arguments:
  -h, --help  show this help message and exit

------------------------------------------------------------------------------

usage: Fterm move [-h] [--left N] [--right N] [--to N] [--end]

optional arguments:
  -h, --help  show this help message and exit
  --left N    move current tab to right
  --right N   move current tab to right
  --to N      move current tab to specified position
  --end       move current tab to end
```

## Global Variables

| Variables                     | Default Value                              | Description
| ---------                     | ------------                               | -----------
| `g:fterm_shell`               | `&shell`                                   | shell to be used when using terminal
| `g:fterm_width`               | `0.75`                                     | width of the terminal
| `g:fterm_height`              | `0.75`                                     | height of the terminal
| `g:fterm_autoquit`            | `0`                                        | kill the terminal automatically when leaving vim
| `g:fterm_exclude_cmdline`     | `1`                                        | exclude the cmdline when calculating the height of terminal
| `g:fterm_exclude_statusline`  | `1`                                        | exclude the statusline when calculating the height of terminal
| `g:fterm_exclude_tabline`     | `1`                                        | exclude the tabline when calculating the height of terminal
| `g:fterm_exclude_signcolumns` | `0`                                        | exclude the signcolumn when calculating the width of terminal
| `g:fterm_borderchars`         | `['─', '│', '─', '│', '┌', '┐', '┘', '└']` | characters of the window border
| `g:fterm_termline_pos`        | `outertop`                                 | pos of termline, value must be one of `outertop, innertop, outerbottom, innerbottom`
| `g:fterm_title`               | `fterm`                                    | default title
| `g:fterm_highlights`          |                                            | highlight setting

## Command

```vim
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
```

## Default Mappings

```vim
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
```

## Default Highlights

```vim
let g:fterm_highlights = {
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
      \ "fterm_hl_terminal_body": {
      \   "ctermfg": "fg",
      \   "ctermbg": "bg",
      \   },
      \ "fterm_hl_termline_body": {
      \   "ctermfg": "fg",
      \   "ctermbg": "bg",
      \   },
      \ }
```

## Support for [asyncrun.vim](https://github.com/skywind3000/asyncrun.vim)

```vim
let g:asyncrun_runner = get(g:, 'asyncrun_runner', {})
let g:asyncrun_runner.fterm = function('fterm#async_runner')
```

## Known issues

1. Cursor position wrong in terminal popup with finished job. Fixed in [patch 8.2.1990](https://github.com/vim/vim/commit/6a07644db30cb5f3d0c6dc5eb2c348b6289da553).

2. Patch 8.2.1990 cause new problem: window changes when using bufload() while in a terminal popup. Fixed in [patch 8.2.1997](https://github.com/vim/vim/commit/8adc8d9b73121b647476a33d91d31d25e1c2d987). This issue will **cause the plugin to not work properly**.

  [1]: https://github.com/ZhiyuanLck/images/blob/master/fterm/fterm.gif
