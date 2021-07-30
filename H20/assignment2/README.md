# IN3110-vegardfa Assignment 2

The move function is found in the codefile move.sh. The function is designed to run with the following parameters:
```
# to move all files from src to dst
move src dst        

# to move all files with a .txt ending from src to dst
move src dst txt    # works with all file endings, not just .txt

# to move all files to a directory dst/YYYY-MM-DD-hh-mm, run with the -d flag
move -d src dst [file_ending]
```
The function will leave subdirectories untouched and print error messages if directories do not exist. The src and dst directories are used for testing the function.

The time tracker is found in track.sh. To use the track function, one must first source the file.
```
source track.sh

# now we can track time!
track start The rest of the line is a label

# to see if a task is running, or what task is running
track status

# to stop the current task
track stop

# to view the tracking log
track log
```
