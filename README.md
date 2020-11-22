# Fterm

<!--ts-->
   - [Fterm](#fterm)
      - [Screenshots](#screenshots)
      - [Installation](#installation)
      - [Usage](#usage)
      - [Global Variables](#global-variables)
      - [Command](#command)
      - [Default Mappings](#default-mappings)
      - [Quick quit](#quick-quit)
      - [Default Highlights](#default-highlights)
      - [Edit file from terminal](#edit-file-from-terminal)
      - [Support for <a href="https://github.com/skywind3000/asyncrun.vim">asyncrun.vim</a>](#support-for-asyncrunvim)
      - [Known issues](#known-issues)
      - [Reference](#reference)

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
usage: Fterm [-h] {new,toggle,kill,select,settitle,move,quit} ...

positional arguments:
  {new,toggle,kill,select,settitle,move}
                        Fterm sub-command help

optional arguments:
  -h, --help            show this help message and exit

------------------------------------------------------------------------------

usage: Fterm new [-h] [--cwd CWD] [--cmd CMD [CMD ...]] [--width width] [--height height]

optional arguments:
  -h, --help           show this help message and exit
  --cwd CWD            cwd of terminal
  --cmd CMD [CMD ...]  run command in new terminal
  --width width        width of the popup window
  --height height      height of the popup window

------------------------------------------------------------------------------

usage: Fterm toggle [-h] [--cwd CWD] [--cmd CMD [CMD ...]] [--width width] [--height height]

optional arguments:
  -h, --help           show this help message and exit
  --cwd CWD            cwd of terminal
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

------------------------------------------------------------------------------

usage: Fterm quit [-h]

optional arguments:
  -h, --help  show this help message and exit
```

## Global Variables

| Variables                     | Default Value                                  | Description
| ---------                     | ------------                                   | -----------
| `g:fterm_shell`               | `&shell`                                       | shell to be used when using terminal
| `g:fterm_width`               | `0.75`                                         | width of the terminal
| `g:fterm_height`              | `0.75`                                         | height of the terminal
| `g:fterm_autoquit`            | `0`                                            | kill the terminal automatically when leaving vim
| `g:fterm_open_cmd`            | `tabedit`                                      | command to edit file from terminal
| `g:fterm_use_root`            | `1`                                            | try to use the root directory of the project as cwd
| `g:fterm_root_marker`         | `['.root', '.git', '.svn', '.hg', '.project']` | markers that mark current directory as root directory
| `g:fterm_root_search_level`   | `5`                                            | max level when searching root directory
| `g:fterm_expanduser`          | `1`                                            | try to expand '~' in command string
| `g:fterm_exclude_cmdline`     | `1`                                            | exclude the cmdline when calculating the height of terminal
| `g:fterm_exclude_statusline`  | `1`                                            | exclude the statusline when calculating the height of terminal
| `g:fterm_exclude_tabline`     | `1`                                            | exclude the tabline when calculating the height of terminal
| `g:fterm_exclude_signcolumns` | `0`                                            | exclude the signcolumn when calculating the width of terminal
| `g:fterm_borderchars`         | `['─', '│', '─', '│', '┌', '┐', '┘', '└']`     | characters of the window border
| `g:fterm_termline_pos`        | `outertop`                                     | pos of termline, value must be one of `outertop, innertop, outerbottom, innerbottom`
| `g:fterm_title`               | `fterm`                                        | default title
| `g:fterm_highlights`          |                                                | highlight setting
| `g:fterm_disable_map`         | `0`                                            | disable default map

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

If you set `g:fterm_disable_map=0`, default mappings are set, but you can change them by following variables.

| Variables               | Default Value | Description
| ---------               | ------------  | -----------
| `g:fterm_map_new`       | `<leader>c`   | create new terminal
| `g:fterm_map_toggle`    | `<leader>t`   | toggle current terminal if not exist, create a new one
| `g:fterm_map_kill`      | `<leader>k`   | kill current terminal and show next one
| `g:fterm_map_killall`   | `<leader>a`   | kill all terminals
| `g:fterm_map_settitle`  | `<leader>,`   | set the title of current terminal
| `g:fterm_map_moveright` | `<leader>l`   | move current termtab to right 1
| `g:fterm_map_moveleft`  | `<leader>h`   | move current termtab to left 1
| `g:fterm_map_movestart` | `<leader>a`   | move current termtab to the start of the termline
| `g:fterm_map_moveend`   | `<leader>e`   | move current termtab to the end of the termline
| `g:fterm_map_select`    | `m*`          | prefix of mappings to select a termtab, `m*` is for meta key, `<m-1>, <m-2>...`, others are normal prefix

If you set `g:fterm_disable_map=1`, then you need to define mappings by yourself. Here is the example code.

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

## Quick quit

You can quit the terminal quickly by command `FtermQuit` which is mapped to the key specified by `g:fterm_map_quit` (by default `q`). The keymap is disabled when certain pattern is matched in command to start the terminal. This work is done by vim built-in function `match()`. The default pattern list is

```vim
let g:fterm_noquit=[
      \ '\v(\w|/)*bash$',
      \ '\v(\w|/)*zsh$',
      \ '\v(\w|/)*ksh$',
      \ '\v(\w|/)*csh$',
      \ '\v(\w|/)*tcsh$'
      \ ]
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

## Edit file from terminal

When in float terminal, you can use `fterm` to open a file in vim.

## Support for [asyncrun.vim](https://github.com/skywind3000/asyncrun.vim)

```vim
let g:asyncrun_runner = get(g:, 'asyncrun_runner', {})
let g:asyncrun_runner.fterm = function('fterm#async_runner')
```

## Known issues

1. Cursor position wrong in terminal popup with finished job. Fixed in [patch 8.2.1990](https://github.com/vim/vim/commit/6a07644db30cb5f3d0c6dc5eb2c348b6289da553).

2. Patch 8.2.1990 cause new problem: window changes when using bufload() while in a terminal popup. Fixed in [patch 8.2.1997](https://github.com/vim/vim/commit/8adc8d9b73121b647476a33d91d31d25e1c2d987). This issue will **cause the plugin to not work properly**.

## Reference
[vim-floaterm](https://github.com/voldikss/vim-floaterm)

  [1]: https://github.com/ZhiyuanLck/images/blob/master/fterm/fterm.gif
