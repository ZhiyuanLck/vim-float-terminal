import vim

from functools import partial
from pathlib import Path

vimcmd = vim.command
vimeval = vim.eval

class InvalidPos(Exception):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return "invalid pos: {}".format(self.pos)

def vimeval(cmd, to_int=0):
    """
    :to_int:
        0 for original
        1 for int
        2 for float
    """
    r = vim.eval(cmd)
    if to_int == 0:
        return r
    if to_int == 1:
        return int(r)
    return float(r)

def vimget(namespace, prefix, var, default, eval_mode=0):
    return vimeval("get({}, '{}_{}', {})".format(namespace, prefix, var, default), eval_mode)

ftget = partial(vimget, 'g:', 'fterm')

def vim_win_setlocal(winid, cmd):
    vimcmd("call win_execute({}, 'setlocal {}')".format(winid, cmd))

def expanduser(path):
    p = Path(path).expanduser().resolve()
    return str(p) if p.exists() else path

def get_cwd():
    cwd = vimeval("fnamemodify(resolve(expand('%:p')), ':p:h')")
    use_root = ftget("use_root", 1) == '1'
    if not use_root:
        return cwd
    is_root = False
    root_marker = ftget("root_marker", ['.root', '.git', '.svn', '.hg', '.project'])
    level = ftget("root_search_level", 5, 1)
    cur = Path(cwd)
    n = 1
    while n <= level and cur != cur.parent:
        if n > 1:
            cur = cur.parent
        for marker in root_marker:
            f = cur / marker
            if not f.is_symlink() and f.exists():
                is_root = True
                break
        if is_root:
            break
        n += 1
    return str(cur) if is_root and cur != Path.home() else cwd

def vimsg(type, msg):
    vimcmd(r"""echohl {} | echom "{}" | echohl None""".format(type, msg))

def get_termline_pos():
    pos = ['innertop', 'outertop', 'innerbottom', 'outerbottom']
    termline_pos = ftget("termline_pos", "'innertop'")
    if termline_pos in pos:
        return termline_pos
    else:
        vimsg('WarningMsg', "invalid pos: '{}', using 'innertop' instead".format(termline_pos))
        return 'innertop'

def get_borderchars() -> list:
    default_borderchars = ['─', '│', '─', '│', '┌', '┐', '┘', '└']
    return ftget("borderchars", default_borderchars)

def get_terminal_border():
    pos = get_termline_pos()
    border = [1, 1, 1, 1]
    borderchars = get_borderchars()
    if pos == 'innertop':
        border[0] = 0
        borderchars[0] = ''
        borderchars[4] = borderchars[3]
        borderchars[5] = borderchars[1]
    if pos == 'innerbottom':
        border[2] = 0
        borderchars[2] = ''
        borderchars[6] = borderchars[1]
        borderchars[7] = borderchars[3]
    return border, borderchars

def get_termline_border():
    pos = get_termline_pos()
    border = [1, 1, 1, 1]
    borderchars = get_borderchars()
    padding = [0, 0, 0, 0]
    if pos == 'outertop' or pos == 'outerbottom':
        border = [0, 0, 0, 0]
        padding = [0, 1, 0, 1]
    if pos == 'innertop':
        border[2] = 0
        borderchars[2] = ''
        borderchars[6] = borderchars[1]
        borderchars[7] = borderchars[3]
    if pos == 'innerbottom':
        border[0] = 0
        borderchars[0] = ''
        borderchars[4] = borderchars[3]
        borderchars[5] = borderchars[1]

    return border, borderchars, padding

def change_list(list, old, to):
    """
    list = [0, 1, 2, 3, 4]
    1. old = 1, to = 3, change to [0, 2, 3, 1, 4]
    1. old = 3, to = 1, change to [0, 3, 1, 2, 4]
    """
    to = to % len(list)
    if to == old:
        return list
    #  to = 0 if to < 0 else to
    #  to = to if to < len(list) else len(list) - 1
    if old < to:
        a = list[0:old]
        b = list[old + 1:to + 1]
        if to < len(list) - 1:
            c = list[to + 1 - len(list):]
        else:
            c = []
        x = list[old]
        return [*a, *b, x, *c]
    else:
        a = list[0:to]
        b = list[to:old]
        if old < len(list) - 1:
            c = list[old + 1:]
        else:
            c = []
        x = list[old]
        return [*a, x, *b, *c]
