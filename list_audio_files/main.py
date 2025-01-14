##################################################################
# How to write a audio file (mp3, flac) collection in a export file?
# Let's export the audio files list having tags (in a base path) in a export file...
#
# The structure of folders and files is loaded in a CollectionNode
# a CollectionNode is a kind of tree using bigtree
# bigtree is a python library, see https://github.com/kayjan/bigtree
# a Collection Node contains one or many VolumeNode
# a VolumeNode is a folder under the root (1st level)
# a VolumeNode contains folders handled as FolderNode and audio files handled as FileNode
# a FolderNode contains folders and files
# the audio files as FileNode have tags retrieved with TinyTag
# TinyTag is a audio file tag python library, see https://github.com/tinytag/tinytag
#
# 14/01/2025 : the collection is written in a col file following the MAC standards
# MAC Mpeg Audio Collection is a audio file collection manager, see https://mac.sourceforge.net/
##################################################################

import main_functions
import node_classes

if __name__ == '__main__':
    print("[main][debug] begin")

    # TODO change the base path of the audio files collection
    basePath = "G:/00 collection/00 best of"
    # TODO change the path of the file to write in
    colFilePath = "G:/00 collection/20250111.col"

    collectionNode :node_classes.CollectionNode = main_functions.build_collection(basePath)

    print("[main][debug] build_collection done : collection " + collectionNode.name + " has " + str(collectionNode.fileCount) + " files")

    main_functions.write_collection(collectionNode, colFilePath, False)
    print("[debug][main] end")



# end main
