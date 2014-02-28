Scheme_Compiler
===============

A shallow scheme compiler using gcc

this project is part of the Compiler Principles course given at Ben-Gurion University

Running the project:

tha main file is Compiler.py
the file has a global method: compile_scheme_file(source,target)
which must be invoked inorder to compile a scheme file into a gcc assembly file.
the source file must contain valid schcme expression, and the target is a C file containing assembly instructions.
compile the target file and run it.
you will see a valid scheme output that describe the user input. :)

Steps:
======

1. run the project under python 3.0 - 3.2:

python3 -i compiler.py

2. call the main method - keep in mind that the target file must end with asm suffix :

compile_schcme_file (source.scm,target.asm)

3.after compiling a scheme file, a C code will be created. just use make with target name to compile it to binary code using gcc

Make target

4. run the compiled gcc code:

./target

the output should be a vaild scheme result.

================================================================
this compiler is assuming input correctnes, if input is not valid result are not certain.


This project was built using Mayer Goldberg Assembly Architecture.

=================================================================
this project is copyright. you may use it for personal use only, and you must give credit to the Autor.
