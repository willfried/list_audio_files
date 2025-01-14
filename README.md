# list_audio_files
How to write a audio file (mp3, flac) collection in a export file, in python.<br>
Let's export the audio files list having tags (in a base path) in a export file...

The structure of folders and files is loaded in a CollectionNode<br>
a CollectionNode is a kind of tree using bigtree<br>
bigtree is a python library, see https://github.com/kayjan/bigtree<br>
a Collection Node contains one or many VolumeNode<br>
a VolumeNode is a folder under the root (1st level)<br>
a VolumeNode contains folders handled as FolderNode and audio files handled as FileNode<br>
a FolderNode contains folders and files<br>
the audio files as FileNode have tags retrieved with TinyTag<br>
TinyTag is a audio file tag python library, see https://github.com/tinytag/tinytag<br>

14/01/2025 : the collection is written in a col file following the MAC standards<br>
MAC Mpeg Audio Collection is a audio file collection manager, see https://mac.sourceforge.net/<br>
It means you can use the col file generated with this project with MAC
to display the collection as a tree in the MAC software
14/01/2025 : Only mp3 and flac are managed
