import vim
import argparse

from .utils import *
from .terminal import Fterm
from .ftermline import FtermLine

class ExtendAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)

class Manager(object):
    def __init__(self):
        self.term_list = []
        self.termline = FtermLine(self)
        self.cur_termnr = -1
        self.show = False
        self.init_parser()

    def issue(self):
        return vimeval("fterm#issue#patch_821990()", 1)

    def init_parser(self):
        parser = argparse.ArgumentParser(prog='Fterm')
        subparsers = parser.add_subparsers(dest='mode', help='Fterm sub-command help')
        default_width = ftget("width", 0.75, 2)
        default_height = ftget("height", 0.75, 2)
        default_title = ftget("title", "'fterm'")
        # new command
        parser_new = subparsers.add_parser('new')
        parser_new.register('action', 'extend', ExtendAction)
        parser_new.add_argument('--cwd', help='cwd of terminal')
        parser_new.add_argument('--cmd', nargs="+", type=str, action="extend",
                help='run command in new terminal')
        parser_new.add_argument('--width', metavar='width', type=float,
                default=default_width, help='width of the popup window')
        parser_new.add_argument('--height', metavar='height', type=float,
                default=default_height, help='height of the popup window')
        parser_new.add_argument('--title', metavar='title', type=str,
                dest='init_title', default=default_title,
                help='set the title of terminal')
        # toggle command
        parser_toggle = subparsers.add_parser('toggle')
        # kill command
        parser_kill = subparsers.add_parser('kill')
        parser_kill.add_argument('--all', default=False, dest="kill_all", action='store_true', help='kill all terminals')
        # select command
        parser_select = subparsers.add_parser('select')
        parser_select.add_argument('termnr', type=int, metavar='terminal_number', help='open the terminal by terminal number')
        # settitle command
        parser_set_title = subparsers.add_parser('settitle')
        parser_set_title.add_argument('title', metavar='title', type=str, help='set the title of current open terminal')
        # move command
        parser_move = subparsers.add_parser('move')
        parser_move.add_argument('--left', dest='move_left', metavar='N', type=int, help='move current tab to right')
        parser_move.add_argument('--right', dest='move_right', metavar='N', type=int, help='move current tab to right')
        parser_move.add_argument('--to', dest='move_to', metavar='N', type=int, help='move current tab to specified position')
        parser_move.add_argument('--end', default=False, dest="move_end", action='store_true', help='move current tab to end')
        # quit command
        parser_quit = subparsers.add_parser('quit')
        self.parser = parser

    def start(self, arglist):
        if self.issue():
            return
        try:
            args = self.parser.parse_args(arglist)
            self.args = args
        except SystemExit:
            return
        try:
            mode = self.args.mode
            if mode == 'new':
                self.create_term()
            elif mode == 'toggle':
                self.toggle_term()
            elif mode == 'kill':
                if self.args.kill_all:
                    self.kill_all_term()
                else:
                    self.kill_single_term()
            elif mode == 'select':
                self.select_term(self.args.termnr)
            elif mode == 'settitle':
                self.termline.set_title(self.args.title)
            elif mode == 'move':
                self.move()
            elif mode == 'quit':
                self.quit()
        except AttributeError:
            pass

    def empty(self):
        return len(self.term_list) == 0

    def get_curterm(self):
        return None if self.empty() else self.term_list[self.cur_termnr]

    def create_term(self):
        """
        1. create from empty
        2. create when fterm is hidden
        3. create when fterm is show
        """
        curterm = self.get_curterm()
        if curterm is not None:
            curterm.close_popup()
        term = Fterm(self.termline, self.args)
        self.cur_termnr += 1
        self.term_list.insert(self.cur_termnr, term)
        term.create_popup()
        self.show = True

    def toggle_term(self):
        if self.empty():
            default = ftget("toggle_default", "'FtermNew'")
            vimcmd(default)
        elif self.show:
            self.get_curterm().close_popup()
            self.show = False
        else:
            self.get_curterm().create_popup()
            return_to_terminal()
            self.show = True

    def kill_single_term(self):
        if self.empty():
            vimcmd("echom 'there is no terminal to kill'")
            return
        if self.show:
            self.get_curterm().close_popup()
        term = self.term_list.pop(self.cur_termnr)
        term.kill_term()
        if self.empty():
            self.show = False
        if self.cur_termnr >= len(self.term_list): # no terminal on the right
            self.cur_termnr -= 1
        if self.show and not self.empty():
            self.get_curterm().create_popup()
            return_to_terminal()

    def quit(self):
        if not self.show or self.empty():
            return
        term = self.term_list.pop(self.cur_termnr)
        term.close_popup()
        term.kill_term()
        if self.cur_termnr >= len(self.term_list): # no terminal on the right
            self.cur_termnr -= 1
        self.show = False

    def kill_all_term(self):
        if self.empty():
            vimcmd("echom 'there is no terminal to kill'")
            return
        if self.show:
            self.get_curterm().close_popup()
            self.show = False
        for term in self.term_list:
            term.kill_term()
        self.cur_termnr = -1
        self.term_list.clear()

    def select_term(self, termnr):
        if termnr > len(self.term_list):
            vimsg("Error", "invalid argument: {}".format(termnr))
            return_to_terminal()
            return
        if self.show:
            self.get_curterm().close_popup()
        else:
            self.show = True
        self.cur_termnr = termnr - 1
        self.get_curterm().create_popup()
        return_to_terminal()

    def move(self):
        left = self.args.move_left
        right = self.args.move_right
        to = self.args.move_to
        end = self.args.move_end
        #  print(left, right, to)
        termline = self.termline
        if end:
            termline.move_end()
            return
        if to is not None:
            termline.move_to(to - 1)
            return
        if left is not None:
            termline.move_left(left)
            return
        if right is not None:
            termline.move_right(right)

    def edit_in_vim(self, path):
        print(path)
        if self.show:
            self.toggle_term()
        cmd = ftget("open_cmd", "'tabedit'")
        vimcmd("{} {}".format(cmd, path))

    def async_run(self):
        cmd = []
        cwd = vimeval("shellescape(getcwd())")
        cmd.append('cd {}'.format(cwd))
        cmd.append(vimeval("a:opts.cmd"))
        cmd = '; '.join(cmd).replace('"', r'\"')
        need_return = False if self.empty() else True
        if self.empty():
            vimcmd("FtermNew")
        if not self.show:
            self.get_curterm().create_popup()
            self.show = True
        bufnr = self.get_curterm().bufnr
        #  cmd = 'ls'
        vimcmd(r"""call term_sendkeys({}, "{}\<cr>")""".format(bufnr, cmd))
        if need_return:
            return_to_terminal()
        #  vimcmd(r"""call feedkeys("{}\<cr>")""".format(cmd))

manager = Manager()

__all__ = ['manager']
