if !has('python3')
    echo "Error: Required vim compiled with +python3"
    finish
endif
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
from vim_arg_wrap import wrap_args
EOF
function! WrapArgs()
    python3 wrap_args()
endfunction

command! -nargs=0 WrapArgs call WrapArgs()
