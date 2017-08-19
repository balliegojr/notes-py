# Notes Py #

A simple console program to note managing

## Configuration ##
Upon the first use, a .notesrc will be created in the home folder with the defaults config  

```
[NOTES]
# Path to store the notes
path = "~/.notes"
# File extension
extension = ".note"
# Editor to be used to change the notes
editor = $EDITOR
```

## Usage ##

### Show help ###
```
notes.py -h
notes.py --help
```

### Insert new note ###
Notes are stored in the path specified into the .notesrc. Upon the creation of a note, the default editor will be used to edit the note.

```
notes.py insert note_one
notes.py new note two
```

It is possible to use sub folders
```
notes.py insert folder/note
```

### Editing a note ###
```
notes.py edit note_one
```

### Removing a note ###
```
notes.py remove note_one
notes.py del note_one
```

### Showing the contents ###
```
notes.py show note_one
```

### Moving a note ###
```
notes.py rename old_name new_name
notes.py move old_name new_name
notes.py move "path/old name" "new path/new name"
```

### Listing notes ###
```
notes.py list
notes.py
```

### Overriding the editor ###
Upon the creation or edition of a note, it is possible to override the editor to be used with the option --editor

```
notes.py insert --editor=subl new note
```
