mergetex.py

This is a script for merging a LaTeX project into a single 
monolithic file while stripping out the comments.  The purpose is 
to make it easier to generate a single pared-down .tex file for
submitting manuscripts to ArXiV, which generally wants the raw
.tex.  Sometimes comments are embarassing, so this script removes
them (while checking for excaped \% signs).

The script scans recursively through the main .tex file looking
for \input{} commands and appends them to a target output file.

USAGE:
     python mergetex.py  [input]  [output]

EXAMPLE:
     python mergetex.py  mypaper.tex  mypaperMerged.tex

v0.1 by Anand Sarwate (asarwate@alum.mit.edu) based on a previous
perl version.
