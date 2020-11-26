# Fterm

Simple vim terminal in popup window with a **termline**.

## Screenshots

![buffer][1]

## Overview

- Create/toggle/kill terminal in popup window handily.
- Termline support just like tabline.
- Blocked mapping only for fterm.

## Installation

- Requirement: `+python3`, `+popup`, `+terminal`
- Best experience: include patch >= 8.2.1997
- Support for nvim: **not yet**

For vim-plug:

```vim
Plug 'ZhiyuanLck/vim-float-terminal'
```

## Usage

All commands are derived from command `:Fterm`

```
usage: Fterm [-h] {new,toggle,kill,select,settitle,move,quit} ...

positional arguments:
  {new,toggle,kill,select,settitle,move}
  new        create a new terminal
  toggle     toggle a terminal to show or hidden
  kill       kill a terminal
  settitle   set the title of current terminal
  move       move the place of terminal on termline
```

All subcommands have separate options, see more details via `:h fterm-commands`.

## Global Variables

- Check normal global options by `:h fterm-options`.
- Check mapping options by `:h fterm-mappings`.

## Mappings

Fterm sets the default mappings for you. You can change them by mapping
variables like `g:fterm_map_xxx`. There is a little difference when you change
the mapping of selecting terminal, see more details by `:h g:fterm_map_select`.

You can also disable all default mappings by `let g:fterm_disable_map = 1`,
and then customize your own mapping through `g:fterm_custom_map`, which make
it possible to define **blocked mapping** that takes effect only in fterm. See
more details by `:h g:fterm_custom_map`.

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

## Highlights

You can customize highlights by `g:fterm_highlights`. See all default
highlights by `:h g:fterm_highlights`.

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
