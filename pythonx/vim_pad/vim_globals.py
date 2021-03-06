# coding=utf-8
import vim
from os.path import join
from vim_pad.utils import get_save_dir

def set_vim_globals():
    """ Sets global vim preferences and commands.
    """
    # To update the date when files are modified
    if get_save_dir() == "":
        vim.command('echom "vim-pad: IMPORTANT: please set g:pad#dir to a valid path in your vimrc."')
        vim.command("redraw")
    else:
        vim.command('execute "au! BufEnter" printf("%s*", g:pad#dir) ":let b:pad_modified = 0"')
        vim.command('execute "au! BufWritePre" printf("%s*", g:pad#dir) ":let b:pad_modified = eval(&modified)"')
        vim.command('execute "au! BufLeave" printf("%s*", g:pad#dir) ":call pad#UpdatePad()"')

    # vim-pad pollutes the MRU.vim list quite a lot, if let alone.
    # This should fix that.
    if vim.eval('exists(":MRU")') == "2":
        mru_exclude_files = vim.eval("MRU_Exclude_Files")
        if mru_exclude_files != '':
            tail = "\|" + mru_exclude_files
        else:
            tail = ''
        vim.command("let MRU_Exclude_Files = '^" +
                join(get_save_dir(), ".*") + tail + "'")

    # we forbid writing backups of the notes
    orig_backupskip = vim.eval("&backupskip")
    vim.command("let &backupskip='" +
            ",".join([orig_backupskip, join(get_save_dir(), "*")]) + "'")

