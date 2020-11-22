import vim
import re

from pathlib import Path
from .utils import *
from .ftermline import FtermLine

class Fterm(object):
    def __init__(self, termline, args):
        self.termline = termline
        self.args = vars(args)
        self.lastbuf = vimeval("bufnr('%')", 1)
        self.set_cwd()
        self.title = ftget("title", "'fterm'")
        self.set_exclude()
        self.set_geometry()
        self.init_term()

    def set_cwd(self):
        cwd = self.args["cwd"]
        if cwd is None:
            self.cwd = get_cwd()
        else:
            self.cwd = str(Path(cwd).expanduser().resolve())

    def set_exclude(self):
        self.exclude_cmdline = ftget("fterm_exclude_cmdline", 1) == '1'
        self.exclude_statusline = vimeval("&laststatus") != '0' and ftget("exclude_statusline", 1) == '1'
        self.exclude_tabline = vimeval("&showtabline") != '0' and ftget("exclude_tabline", 1) == '1'
        self.exclude_signcolumn = vimeval("&signcolumn") == 'yes' and ftget("exclude_signcolumn", 0) == '1'

    def set_geometry(self):
        self.get_max()
        self.width = self.get_size(width=True)
        self.height = self.get_size(width=False)
        self.get_coor()

    def get_max(self):
        self.max_w = vimeval("&columns", 1)
        self.max_h = vimeval("&lines", 1)
        if self.exclude_cmdline:
            self.max_h -= vimeval("&cmdheight", 1)
        if self.exclude_statusline:
            self.max_h -= 1
        if self.exclude_tabline:
            self.max_h -= 1
        if self.exclude_signcolumn:
            self.max_w -= 2

    def get_size(self, width=True):
        max_n = vimeval("&{}".format("columns" if width else "lines"), 1)
        max_n = self.max_w if width else self.max_h
        key = 'width' if width else 'height'
        n = self.args[key]
        n = n if n > 0 else 0.8 # n must > 0
        n = int(n) if n > 1 else int(max_n * n)
        n = max(n, 10) # at least 10 cols or lines
        n = min(n, max_n) # at most max_n
        return n - 2 if width else n - 3 # exclude border and temrline

    def get_anchor(self):
        """
        Get the coordinates of topleft anchor.
        Note that calculation of anchor involves borders while setting the size the popup not.
        """
        delta_w = self.max_w - self.width - 2 # 2 for border
        if delta_w & 1:
            self.anchor_col = (delta_w + 1) // 2 + 1
            self.width -= 1
        else:
            self.anchor_col = delta_w // 2 + 1
        delta_h = self.max_h - self.height - 3 # 3 for border and termline
        if delta_h & 1:
            self.anchor_line = (delta_h + 1) // 2 + 1
            self.height -= 1
        else:
            self.anchor_line = delta_h // 2 + 1
        if self.exclude_tabline:
            self.anchor_line += 1
        if self.exclude_signcolumn:
            self.anchor_col += 2

    def get_coor(self):
        self.get_anchor()
        pos = get_termline_pos()
        self.col = self.anchor_col + 1
        if pos == 'innertop':
            self.line = self.anchor_line + 2
        if pos == 'outertop':
            self.line = self.anchor_line + 1
        if pos == 'innerbottom' or pos == 'outerbottom':
            self.line = self.anchor_line

    def init_term(self):
        cmd = self.get_cmd()
        opts = {"hidden": 1, "norestore": 1, "term_finish": "open"}
        opts["term_cols"] = self.width
        opts["term_rows"] = self.height
        opts["cwd"] = self.cwd
        opts["term_api"] = "fterm#edit"
        self.bufnr = vimeval(r"""term_start("{}", {})""".format(cmd, opts), 1)
        if ftget("autoquit", 0) == '1':
            vimcmd("call term_setkill({}, 'kill')".format(self.bufnr))

    def get_cmd(self):
        shell = ftget("shell", "&shell")
        cmd_parts = self.args["cmd"]
        if cmd_parts is None:
            cmd = shell
        else:
            if ftget("expanduser", 1) == '1':
                cmd_parts = [expanduser(p) for p in cmd_parts]
            cmd = ' '.join(cmd_parts)
        return cmd

    def map_quit(self):
        cmd = self.get_cmd()
        noquit = ftget("noquit", [r'\v(\w|/)*bash$', r'\v(\w|/)*zsh$', r'\v(\w|/)*ksh$', r'\v(\w|/)*csh$', r'\v(\w|/)*tcsh$'])
        map = True
        for pattern in noquit:
            if vimeval("match('{}', '{}')".format(cmd, pattern)) != '-1':
                map = False
                break
        if map:
            quit = ftget("map_quit", "'q'")
            vimcmd(r"tnoremap <silent><buffer>{} <c-\><c-n>:FtermQuit<cr>".format(quit))
            vimcmd(r"noremap <silent><buffer>{} <c-\><c-n>:FtermQuit<cr>".format(quit))

    def create_popup(self):
        opts = {
                "maxwidth":  self.width,
                "minwidth":  self.width,
                "maxheight": self.height,
                "minheight": self.height,
                "padding":   [0, 1, 0, 1],
                "zindex":    1000,
                "pos":       "topleft",
                "line":      self.line,
                "col":       self.col,
                "scrollbar": 0,
                "mapping":   0,
                }
        opts["borderhighlight"] = ftget("hl_terminal_border", "'fterm_hl_border'")
        opts["border"], opts["borderchars"] = get_terminal_border()
        opts["highlight"] = ftget("hl_terminal_body", "'fterm_hl_terminal_body'")
        self.winid = vimeval("popup_create({}, {})".format(self.bufnr, str(opts)), 1)
        self.map_quit()
        self.termline.build_line()

    def close_popup(self):
        vimcmd("call popup_close({})".format(self.winid))
        self.termline.close_popup()

    def kill_term(self):
        vimcmd("call fterm#terminal#kill({})".format(self.bufnr))
