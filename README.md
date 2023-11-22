# Python File Picker

This is a toy project I used to refresh my Python knowledge.

It selects random files from a source directory and copies them to a destination directory.

You can provide a list of extensions to filter the files.

For instance to select 25 random image files from source directory ~/Desktop/local_test_photos and copy them to destination directory ~/Desktop/pictures you can use the following command.

``` Python
python main.py -n 25 -e jpg JPG jpeg png tif gif TIF -- ~/Desktop/local_test_photos ~/Desktop/pictures
