import vim
from functools import partial

from .utils import *

class FtermLine(object):
    def __init__(self, manager):
        self.manager = manager
        self.bufnr = vimeval("bufadd('')", 1)
        # a : fg = left normal  , bg = right normal
        # b : fg = left normal  , bg = right current
        # c : fg = left current , bg = right normal
        self.sep = ftget("termline_sep", "''")
        #  self.prop_types = ["info", "normal", "current", "sep_a", "sep_b", "sep_c"]
        self.prop_types = ["info", "normal", "current"]
        self.init_highlights()
        self.init_text_prop()

    def init_highlights(self):
        vimcmd("call fterm#colorscheme#set()")

    def init_text_prop(self):
        #  optsions = {"bufnr": self.bufnr}
        optsions = dict()
        for prop_type in self.prop_types:
            optsions["highlight"] = ftget("hl_termline_{}".format(prop_type), "'fterm_hl_termline_{}'".format(prop_type))
            vimcmd("call prop_type_add('fterm_{}', {})".format(prop_type, str(optsions)))

    def set_buffer(self):
        setlocal = partial(vim_win_setlocal, self.winid)
        setlocal("nobuflisted")
        setlocal("buftype=nofile")
        setlocal("bufhidden=hide")
        setlocal("undolevels=-1")
        setlocal("noswapfile")
        setlocal("nolist")
        setlocal("nonumber norelativenumber")
        setlocal("nospell")
        setlocal("nofoldenable")
        setlocal("foldmethod=manual")
        setlocal("shiftwidth=4")
        setlocal("nocursorline")
        setlocal("foldcolumn=0")
        setlocal("signcolumn=no")
        setlocal("colorcolumn=")
        #  setlocal("wincolor=...")
        setlocal("filetype=ftermline")

    def build_line(self):
        self.set_popup()
        self.set_buffer()
        self.set_content()
        self.set_text_prop()

    def get_coor(self):
        pos = get_termline_pos()
        term = self.manager.get_curterm()
        anchor_line = term.anchor_line
        self.col = term.col
        if pos == 'innertop' or pos == 'outertop':
            self.line = anchor_line
        if pos == 'innerbottom':
            self.line = anchor_line + term.height
        if pos == 'outerbottom':
            self.line = anchor_line + term.height + 2 # 2 borders

    def set_popup(self):
        self.get_coor()
        term = self.manager.get_curterm()
        opts = {
                "maxwidth":        term.width,
                "minwidth":        term.width,
                "maxheight":       1,
                "minheight":       1,
                "zindex":          1000,
                "pos":             "topleft",
                "line":            self.line,
                "col":             self.col,
                "scrollbar":       0,
                "mapping":         0,
                }
        opts["borderhighlight"] = ftget("hl_terminal_border", "'fterm_hl_border'")
        opts["border"], opts["borderchars"], opts["padding"] = get_termline_border()
        opts["highlight"] = ftget("hl_terminal_body", "'fterm_hl_terminal_body'")
        self.winid = vimeval("popup_create({}, {})".format(self.bufnr, str(opts)), 1)
        self.bufnr = vimeval("winbufnr({})".format(self.winid), 1)

    def set_content(self):
        termline = []
        curterm = self.manager.get_curterm()
        rest = curterm.width
        for i, term in enumerate(self.manager.term_list):
            #  title = " {} {} ".format(i + 1, term.title)
            termline.append(" {} {} ".format(i + 1, term.title))
            #  termline.append(self.format_title(i + 1, term.title))
        self.titles = termline
        termline = self.sep.join(termline)
        vimcmd("call setbufline({}, 1, '{}')".format(self.bufnr, termline))

    # to be used
    def format_title(self, nr, title):
        max_w = ftget("title_max_width", 1, 1)
        title = title[:5] + "..." if len(title) > max_w else title
        return " {} {} ".format(nr, title)

    def set_text_prop(self):
        optsions = {"bufnr": self.bufnr}
        vimcmd("call prop_clear(1, 1, {})".format(str(optsions)))
        pos = 1
        for term in self.manager.term_list:
            length = len(term.title) + 4
            optsions["length"] = length
            optsions["type"] = "fterm_current" if term is self.manager.get_curterm() else "fterm_normal"
            vimcmd("call prop_add(1, {}, {})".format(pos, str(optsions)))
            pos += length

    def close_popup(self):
        vimcmd("call popup_close({})".format(self.winid))

    def rebuild(self):
        self.close_popup()
        self.build_line()
        self.manager.get_curterm().restore()

    def set_title(self, title):
        manager = self.manager
        term = manager.get_curterm()
        if term is None:
            vimsg("Error", "No terminal exists!")
            return
        if not manager.show:
            vimsg("Error", "please toggle terminal first before setting its title")
            return
        term.title = title
        self.rebuild()

    def move_to(self, term_nr: int):
        manager = self.manager
        term_list = manager.term_list
        cur_termnr = manager.cur_termnr
        if cur_termnr == -1:
            return
        term_nr = term_nr % len(term_list)
        #  term_nr = term_nr if term_nr >=0 else 0
        #  term_nr = term_nr if term_nr < len(term_list) - 1 else len(term_list) - 1
        manager.term_list = change_list(term_list, cur_termnr, term_nr)
        manager.cur_termnr = term_nr
        self.rebuild()

    def move_left(self, n):
        manager = self.manager
        cur_termnr = manager.cur_termnr
        termnr = cur_termnr - n
        self.move_to(termnr)

    def move_right(self, n):
        self.move_left(-n)

    def move_end(self):
        self.move_to(len(self.manager.term_list) - 1)
