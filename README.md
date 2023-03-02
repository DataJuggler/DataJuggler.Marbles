# Data Juggler Marbles Creator

This project reads a directory and loads all .png images.

Then 100 marbles at a time and 100 OmniPBR Materials are created and the image at the matching index is applied. You can run this extension more than once (in a session) and create hundreds of marbles. I tried creating many hundreds at a time and Code would lock up, but 100 at a time seems to work in about 30 seconds then it gets slower the
more times you create 100.

I create the images to apply using this project
https://github.com/DataJuggler/SubImageCreator - This is a C# WinForms project, but there is a release version you can 
install. Look for Releases in the bottom right of the above link.



