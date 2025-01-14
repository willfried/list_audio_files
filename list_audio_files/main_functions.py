##################################################################
# How to write a audio file (mp3, flac) collection in a export file?
#
# This file gathers the main functions called by the main script
# * buildCollection(collectionPath)
# * write_collection(collection, colFilePath, test)
# and some other private methods dedicated
# to build the complete collection (__build_volume, __build_folder)
# and to write (__write_volume, __write_folder, __write_file)
##################################################################

import utils_file
import utils_writer
import os
import node_classes
from tinytag import TinyTag

# private method build_folder
# Adds the folders (as FolderNode) and files (as FileNode) in sPath to the parent folderNode
# param sPath : the volume path
# param folderNode : the FolderNode to process
def __build_folder(sPath, folderNode ):
    #print("[debug][build_folder] beginning in sPath=" + sPath)

    # let's find the relative path of sPath, example "dir_c" if sPath = "G:/dir_a/dir_b/dir_c"
    rPath = utils_file.relativePath(sPath)

    childrenList = os.listdir(sPath)

    #print("[debug][build_folder] adding the childs in sPath : " + sPath + ", len=" + str(len(childrenList)))
    for i in childrenList:

        iPath = os.path.join(sPath, i)

        if os.path.isfile(iPath):
            # TODO : only flac and mp3 are handled
            if i.endswith(".flac") or i.endswith(".mp3"):
                #print("[debug][build_folder] adding fileNode : " + i)
                # loading the audio tags with TinyTag
                tag = TinyTag.get(iPath)
                fileNode = node_classes.FileNode(i, tag.filesize, tag.duration, tag.samplerate, tag.title, tag.artist, tag.album, tag.track, tag.year, tag.comment, tag.genre, tag.bitdepth, tag.channels, parent=folderNode)
                #build_file(fileNode, iPath)
        elif os.path.isdir(iPath):
            #print("[debug][build_folder] adding folder [" + i +"]")
            subFolderNode = node_classes.FolderNode(i, parent=folderNode)
            __build_folder(iPath, subFolderNode)
        else:
            # unexpected case, then raise an exception
            print("[ERROR][build_folder] Unexpected item in [" + i + "]")
            raise Exception("[ERROR][build_folder] Unexpected item in [" + i + "]")


# private method build_volume
# Builds the volume in sPath as a VolumeNode and add it to collectionNode
# a VolumeNode is like a FolderNode but at the 1st level (under the root)
# param sPath : the volume path
# param collectionNode : the processed CollectionNode parent of the VolumeNode
def __build_volume(sPath :str, collectionNode):
    #print("[debug][build_volume] beginning in sPath=" + sPath)

    # let's find the relative path of sPath, example "dir_c" if sPath = "G:/dir_a/dir_b/dir_c"
    rPath = utils_file.relativePath(sPath)

    # at first level under collectionNode only volumes
    volumeNode = node_classes.VolumeNode(rPath, parent=collectionNode)
    #print("[debug][build_volume] creating volumeNode [" + rPath + "]")

    childrenList = os.listdir(sPath)

    #print("[debug][build_volume] adding the childs in sPath : " + sPath + ", len=" + str(len(childrenList)))
    for i in childrenList:
        iPath = os.path.join(sPath, i)
        if os.path.isfile(iPath):
            # TODO : only flac and mp3 are handled
            if i.endswith(".flac") or i.endswith(".mp3"):
                #print("[debug][build_volume] adding fileNode : " + i )
                tag = TinyTag.get(iPath)
                fileNode = node_classes.FileNode(i, tag.filesize, tag.duration, tag.samplerate, tag.title, tag.artist, tag.album, tag.track, tag.year, tag.comment, tag.genre, tag.bitdepth, tag.channels, parent=volumeNode)
        elif os.path.isdir(iPath):
            #print("[debug][build_volume] adding folderNode [" + i +"]")
            folderNode = node_classes.FolderNode(i, parent=volumeNode)
            __build_folder(iPath, folderNode)
        else:
            # unexpected case, then raise an exception
            print("[ERROR][build_volume] Unexpected item in [" + i + "]")
            raise Exception("[ERROR][build_volume] Unexpected item in [" + i + "]")


# function build_collection
# Builds a audio file collection in a CollectionNode processed with Volume nodes, Folder nodes and File nodes
# param sBasePath : the root folder path
# returns : a processed CollectionNode
def build_collection(sBasePath :str):
    print("[debug][build_collection] beginning in [" + sBasePath + "]")
    # let's create a new CollectionNode
    collection = node_classes.CollectionNode("AudioCollection")
    # and we add the volumes
    __build_volume(sBasePath, collection)
    print("[debug][build_collection] returns collection [" + collection.name + "]")
    return collection

# end def build_collection(sBasePath)

# private method write_file
# Writes audio file as a FileNode in a colFile ".col" file
# param fileNode : the fileNode to write
# param colFile : the col file to write in, as a stream
def __write_file(fileNode: node_classes.FileNode, colFile):
    utils_writer.write_file_line(colFile, fileNode)
# end def write_file

# private method write_folder
# Writes folder as a FolderNode in a colFile ".col" file
# param folderNode : the folderNode to write
# param colFile : the col file to write in, as a stream
def __write_folder(folderNode: node_classes.FolderNode, colFile):
    #write the folder in colFile
    utils_writer.write_folder_line(colFile, folderNode)
    # itemList contains Folders and files
    itemList = folderNode.children
    # for every folder childs
    for i in itemList :
        if isinstance(i, node_classes.FolderNode):
            # write the folderNode in colFile
            __write_folder(i, colFile)
        elif isinstance(i, node_classes.FileNode):
            # write the fileNode in colFile
            __write_file(i, colFile)
        else:
            print("[ERROR][write_collection] unknow [" + i.name + "]")
            raise Exception("[ERROR][write_collection] unknow [" + i.name + "]")

#end def write_folder

# private method write_volume
# Writes volume as a VolumeNode in a colFile ".col" file
# param volumeNode : the volumeNode to write
# param colFile : the col file to write in, as a stream
def __write_volume(volumeNode: node_classes.VolumeNode, colFile):
    # write the volume in colFile
    utils_writer.write_volume_line(colFile, volumeNode)
    # itemList contains Folders and files
    itemList = volumeNode.children
    # for every volume childs
    for i in itemList :
        if isinstance(i, node_classes.FolderNode):
            #write the folderNode in colFile
            __write_folder(i, colFile)
        elif isinstance(i, node_classes.FileNode):
            # write the fileNode in colFile
            __write_file(i, colFile)
        else:
            print("[ERROR][write_collection] unknow [" + i.name + "]")
            raise Exception("[ERROR][write_collection] unknow [" + i.name + "]")

# end def write_volume(sBasePath)

# function write_collection
# Writes a audio file collection as a CollectionNode in a ".col" file whose path is sColFilePath
# param collectionNode : the collectionNode to write
# param sColFilePath : the col file path to write in
# param test : if test mode, we only display the collection structure
# see https://bigtree.readthedocs.io/en/stable/gettingstarted/demo/tree/
def write_collection(collectionNode : node_classes.CollectionNode, sColFilePath :str, test :bool):

    if test:
        # if test mode, we only display the collection structure
        collectionNode.show()
    else:
        # we open the file for writing
        colFile = open(sColFilePath, "x")
        # we write the collection line in the colFile
        utils_writer.write_collection_line(colFile, collectionNode)
        volumeList = collectionNode.children
        #print("[debug][write_collection] writing the volume children, len = [" + str(len(volumeList)))
        for v in volumeList :
            __write_volume(v, colFile)

        # we close the file
        colFile.close()

# end def write_collection