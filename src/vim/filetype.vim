if exists("did_load_filetypes")
    finish
endif
augroup filetypedetect
    au! BufEnter,BufNewFile SConstruct,SConscript,Sconcript,Sconstruct,sconscript,sconstruct set filetype=python
    au! BufEnter,BufNewFile *.sv set filetype=verilog
    au! BufRead,BufNewFile *.tpp set filetype=cpp
augroup END
