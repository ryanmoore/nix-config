""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => My Commands 
""""""""""""""""""""""""""""""""""""""""""""""""""""""


""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General
""""""""""""""""""""""""""""""""""""""""""""""""""""""

vmap  - :diffget<cr>

"make it easier to jump to specific mark locations
nnoremap ' `
nnoremap ` '
"keep longer history log
set history=700
"change terminal title(hopefully)

filetype plugin on
filetype indent on

"auto read when a file is changed from the outside
set autoread

let mapleader = ","
let g:mapleader = ","

"fast saving
nmap <leader>w :w!<cr>

"when vimrc is edited, reload it
autocmd! bufwritepost vimrc source ~/.vimrc

"Save and restore things like folds
au BufWinLeave * silent! mkview
au BufWinEnter * silent! loadview

""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM userinterface 
""""""""""""""""""""""""""""""""""""""""""""""""""""""

"center page on cursor a bit better
set scrolloff=7

"show menu with possible tab completions
set wildmenu

"always show current position
set ruler

set cmdheight=1

"Set backspace confi
set backspace=eol,start,indent
set whichwrap+=<,>

"search casing
set ignorecase
set smartcase

set hlsearch "Highlight search things

"set incsearch "make search act like search in modern browser
set nolazyredraw "don't redraw while executing macros

set magic "Set magic on, for regex

set showmatch "Show batching brackets when text indicator is over them
set mat=2 "how many tenths of a second to blink

"No sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
""""""""""""""""""""""""""""""""""""""""""""""""""""""

syntax enable "enable syntax hl

set gfn=Monospace\ 10
set shell=/bin/bash

colorscheme ron
set background=dark

set encoding=utf8

try
	lang en_US
catch
endtry

"highlight Pmenu ctermfg=0 ctermbg=3
"highlight PmenuSel ctermfg=0 ctermbg=7
"if &bg == "dark"
"	highlight MatchParen ctermbg=darkblue guibg=blue
"endif


""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Files, backups, and undo
""""""""""""""""""""""""""""""""""""""""""""""""""""""

"Turn backup off, since most stuff is rev control anyways
set nobackup
set nowb
set noswapfile

"Persistent undo
try
	set undodir=~/.vim/undodir
	set undofile
catch
endtry

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Text, tab and indent related
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set expandtab
set shiftwidth=4
set tabstop=4
set smarttab

"turn off expandnig tabs for makefiles
autocmd BufEnter ?akefile*,*.mk set noexpandtab ts=8 sw=8
autocmd BufLeave ?akefile*,*.mk set expandtab   ts=4 sw=4
"autocmd BufEnter ?.mk set noet ts=8 sw=8

set lbr
set tw=500

set ai "Auto indent
set si "Smart indet
"set wrap "Wrap lines

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Moving around, tabs and buffers
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Map space to / (search) and c-space to ? (backgwards search)
map <space> /
map <c-space> ?
map <silent> <leader><cr> :noh<cr>

" Smart way to move btw. windows
map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" Close the current buffer
map <leader>bd :Bclose<cr>

" Close all the buffers
map <leader>ba :1,300 bd!<cr>

" Use the arrows to something usefull
map <right> :tabn<cr>
map <left> :tabp<cr>

" Tab configuration
map <leader>tn :tabnew<cr>
map <leader>te :tabedit
map <leader>tc :tabclose<cr>
map <leader>tm :tabmove

" When pressing <leader>cd switch to the directory of the open buffer
map <leader>cd :cd %:p:h<cr>


command! Bclose call <SID>BufcloseCloseIt()
function! <SID>BufcloseCloseIt()
	let l:currentBufNum = bufnr("%")
	let l:alternateBufNum = bufnr("#")

	if buflisted(l:alternateBufNum)
		buffer #
	else
		bnext
	endif

	if bufnr("%") == l:currentBufNum
		new
	endif

	if buflisted(l:currentBufNum)
		execute("bdelete! ".l:currentBufNum)
	endif
endfunction

" Specify the behavior when switching between buffers 
try
	set switchbuf=usetab
	set stal=2
catch
endtry

""""""""""""""""""""""""""""""
" => Statusline
""""""""""""""""""""""""""""""
" Always hide the statusline
set laststatus=2

" Format the statusline
set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CWD:\ %r%{CurDir()}%h\ \ \ Line:\ %l/%L:%c


function! CurDir()
	let curdir = substitute(getcwd(), '/Users/ryancm/', "~/", "g")
	return curdir
endfunction

function! HasPaste()
	if &paste
		return 'PASTE MODE  '
	else
		return ''
	endif
endfunction

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Parenthesis/bracket expanding
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
vnoremap $1 <esc>`>a)<esc>`<i(<esc>
vnoremap $2 <esc>`>a]<esc>`<i[<esc>
vnoremap $3 <esc>`>a}<esc>`<i{<esc>
vnoremap $$ <esc>`>a"<esc>`<i"<esc>
vnoremap $q <esc>`>a'<esc>`<i'<esc>
vnoremap $e <esc>`>a"<esc>`<i"<esc>

" Map auto complete of (, ", ', [
" if not a perl document
inoremap $1 ()<esc>i
inoremap $2 []<esc>i
inoremap $3 {}<esc>i
inoremap $4 {<esc>o}<esc>O
inoremap $5 {<esc>o};<esc>O
inoremap $q ''<esc>i
inoremap $e ""<esc>i
inoremap $t <><esc>i

" in verilog, replace {} with beginend
autocmd BufEnter *.v inoremap $4 <esc>^"py$obegin<esc>oend // <esc>"ppO

"Delete trailing white space, useful for Python ;)
func! DeleteTrailingWS()
	exe "normal mz"
	%s/\s\+$//ge
	exe "normal `z"
endfunc
autocmd BufWrite *.py :call DeleteTrailingWS()

set guitablabel=%t

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Cope
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Do :help cope if you are unsure what cope is. It's super useful!
map <leader>cc :botright cope<cr>
map <leader>n :cn<cr>
map <leader>p :cp<cr>

""""""""""""""""""""""""""""""
" => Python section
""""""""""""""""""""""""""""""
let python_highlight_all = 1
au FileType python syn keyword pythonDecorator True None False self

au BufNewFile,BufRead *.jinja set syntax=htmljinja
au BufNewFile,BufRead *.mako set ft=mako

au FileType python inoremap <buffer> $r return
au FileType python inoremap <buffer> $i import
au FileType python inoremap <buffer> $p print
au FileType python inoremap <buffer> $f #--- PH ----------------------------------------------<esc>FP2xi
au FileType python map <buffer> <leader>1 /class
au FileType python map <buffer> <leader>2 /def
au FileType python map <buffer> <leader>C ?class
au FileType python map <buffer> <leader>D ?def

""""""""""
" => MIST
"""""""""
" Remove the Windows ^M - when the encodings gets messed up
noremap <Leader>m mmHmt:%s/<C-V><cr>//ge<cr>'tzt'm

"Quickly open a buffer for scripbble
map <leader>q :e ~/buffer<cr>
au BufRead,BufNewFile ~/buffer iab <buffer> xh1 ===========================================

map <leader>pp :setlocal paste!<cr>

map <leader>bb :cd ..<cr>



""""""""""""MY STUFF
"make tags search up
set tags=tags;/

set nowrap
"ignore case unless capitals are present
"ignore these file endings when completing names
set wildignore=.svn,CVS,.git,*.o,*.a,*.swp,*.obj,*.jpg,*.png,*.gif,*.bmp

"display line numbers
set number

"If a tmp1.* exists matching our extension pattern,
"read the tmp1.% into our buffer and substitude a time string if we can
autocmd! BufNewFile * silent! 0r ~/.vim/templates/tmp1.%:e| silent! %s/VIM_TIME_REGEX/\=strftime("%c")/

nmap <F1> :echo<CR>
imap <F1> <C-o>:echo<CR>

inoremap jk <ESC>l

nnoremap <F9> :s/\(\s\+\)\(\w\+\),/\1.\2(\2),/


set diffopt+=iwhite

"Automatic comment/uncomment
au FileType haskell,vhdl,ada let b:comment_leader = '--'
au FileType vim let b:comment_leader = '"'
au FileType c,cpp,java let b:comment_leader = '//'
au FileType sh,make,python let b:comment_leader = '#'
au FileType matlab,tex let b:comment_leader = '%'
noremap <silent> ,c :<C-B>sil <C-E>s/^\(\s*\)/\1<C-R>=escape(b:comment_leader,'\/')<CR>/<CR>:noh<CR>
noremap <silent> ,u :<C-B>sil <C-E>s/^\(\s*\)\V<C-R>=escape(b:comment_leader,'\/')<CR>/\1/e<CR>:noh<CR>


"screen
set titlestring=%t%(\ %M%)%(\ (%{expand(\"%:p:h\")})%)%(\ %a%)\ -\ %{v:servername}
set title
if $TERM=='screen'
    exe "set title titlestring=vim:%f"
    exe "set title t_ts=\<ESC>k t_fs=\<ESC>\\"
endif
