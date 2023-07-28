# vim-arg-wrap
Function arguments wrapper, suitable for languages which use parentheses and commas to represent arguments/parameters lists.
![image](https://raw.githubusercontent.com/EugeneSqr/vim-arg-wrap/assets/python-demo.gif)
![image](https://raw.githubusercontent.com/EugeneSqr/vim-arg-wrap/assets/js-demo.gif)

Suppose you have a function invocation with several arguments:
```javascript
long_function_name(first_argument, second_argument, third_argument)
```
The line happens to be too long and you want to wrap it. The most common ways to do it:
```javascript
long_function_name( // let it be type A wrapping
    first_argument, second_argument, third_argument)
```
```javascript
long_function_name( // type B
    first_argument,
    second_argument,
    third_argument)
```
```javascript
long_function_name(first_argument, // type C
                   second_argument,
                   third_argument)
```
```javascript
long_function_name(
    first_argument, // type D
    second_argument,
    third_argument,
)
```
The choice depends on numerous factors, but it's a good idea to have means to quickly apply all of them in your general-purpose text editor.

The plugin exposes two commands to cycle through wrapping types:

* `WrapArgs` to cycle forwards, i.e. `nowrap -> A -> B -> C -> D -> nowrap`
* `WrapArgsBack` to cycle backwards `nowrap -> D -> C -> B -> A -> nowrap`

With proper key bindings it becomes extremely easy to apply any type of wrapping.
```viml
nnoremap <leader>j :WrapArgs<cr>
nnoremap <leader>J :WrapArgsBack<cr>
```

## Installation
Follow your vim package manager's instuctions for installing plugins from github. For [Vundle.vim](https://github.com/VundleVim/Vundle.vim) place these lines into your `vimrc`
```viml
call vundle#begin()
Plugin 'eugenesqr/vim-arg-wrap'
call vundle#end()
```
then launch `vim` and run `:PluginInstall`

## Dependencies
Python 3.8

## Dev environment setup
Navigate to the directory where the plugin is installed for example: `~/.vim/bundle/vim-arg-wrap`. Find the `python` subfolder there, `cd` to it. Initialize virtual environment (if needed) and work with the code as usual:
```bash
python3.8 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Linting the code
```bash
./run_lint
./run_lint --no-typing
```

### Running the tests
```bash
pytest
```
