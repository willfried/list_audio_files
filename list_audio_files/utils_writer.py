##################################################################
# How to write a audio file (mp3, flac) collection in a export file?
#
# This file gathers the functions to write the ".col" export file
# * write_collection_line(colFile, collectionNode: CollectionNode)
# * write_volume_line(tFile, vn: VolumeNode)
# * write_folder_line(tFile, cn: FolderNode)
# * write_file_line(tFile, fn: FileNode)
#
# These methods are following the MAC col file description
# see https://mac.sourceforge.net/
##################################################################

import utils_ascii
from math import floor
from node_classes import CollectionNode, VolumeNode, FolderNode, FileNode

# function write_fileTag
# write a file (one line) in a ".col" file as described in https://mac.sourceforge.net/
# param tFile : the stream on the ".col" file
# param fn : the FileNode to write in colFile
def write_file_line(tFile, fn: FileNode):
    iLevel = fn.depth - 1
    for x in range(iLevel):
        tFile.write(utils_ascii.TAB)

    # File name(max. 250 characters)
    tFile.write(fn.name)
    tFile.write(utils_ascii.SOH)
    # Size(kilobytes)
    iSize = floor(fn.size / 1024)
    tFile.write( str(iSize) )
    tFile.write(utils_ascii.STX)
    # Duration(seconds), a negative number means "VBR" - coded with variable bit rate
    iDuration = floor(fn.duration)
    if fn.name.endswith(".mp3"):
        tFile.write( str( floor(iDuration)) )
    elif fn.name.endswith(".flac"):
        tFile.write( "-" + str( floor(iDuration)) )
    else:
        tFile.write( str( floor(iDuration)) )
    tFile.write(utils_ascii.ETX)
    # Sample Rate(without last 0 - e.g. 4410)
    iSampleRate = floor(fn.sampleRate / 10)
    tFile.write( str(iSampleRate))
    tFile.write(utils_ascii.EOT)
    # Kanal mode:
    #     Stereo = 1
    #     Joint Stereo = 2
    #     Dual Channel = 3
    #     Mono = 4

    # stereo else mono
    if fn.channels is not None and fn.channels == 2:
        tFile.write("1")
    else:
        tFile.write("4")

    tFile.write(utils_ascii.ENQ)
    # MPEG Version:
    #     Unknown = 0
    #     V1 = 1
    #     V2 = 2
    #     V2.5 = 3
    #     MPEG + SV4..7 = 4..7
    #     Windows PCM = 9
    #     TwinVQ = 10
    #     Ogg Vorbis = 20
    #     Windows Media Audio = 25
    #     Monkeys Audio = 30
    #     FLAC = 35
    #     OptimFROG = 40
    #     AAC = 45
    #     WavPack = 50
    if fn.name.endswith(".mp3"):
        tFile.write("1")
    elif fn.name.endswith(".flac"):
        tFile.write("35")
    else:
        tFile.write("0")

    tFile.write(utils_ascii.ACK)
    # MPEG Layer:
    #     Unknown = 0
    #     L1..3 = 1..3 or MPEG + SV7 Profile 1..5 = 1..5
    #     Windows PCM, Monkey 's Audio or FLAC = 8, 16 (bit)
    #     TwinVQ = 10
    #     Ogg Vorbis = 20
    #     Windows Media Audio = 25

    if fn.bitdepth is not None:
        if fn.name.endswith(".flac"):
            tFile.write( str(fn.bitdepth) )
        elif fn.name.endswith(".mp3"):
            tFile.write("3")
        else:
            tFile.write("0")
    else:
        tFile.write("0")

    tFile.write(utils_ascii.BEL)
    tFile.write(utils_ascii.NAK)
    # ID3 - tag: Title(can be empty)
    if fn.title is not None:
        tFile.write(fn.title)
    tFile.write(utils_ascii.SYN)
    # ID3 - tag: Artist(can be empty)
    if fn.artist is not None:
        tFile.write(fn.artist)
    tFile.write(utils_ascii.ETB)
    # ID3 - tag: Album(can be empty)
    if fn.album is not None:
        tFile.write(fn.album);
    tFile.write(utils_ascii.CAN)
    # ID3 - tag: Track number(can be empty)
    if fn.track is not None:
        tFile.write(str(fn.track));
    tFile.write(utils_ascii.EM)
    # ID3 - tag: Year(can be empty)
    if fn.year is not None:
        tFile.write(fn.year)
    tFile.write(utils_ascii.SUB)
    # ID3 - tag: Comment(can be empty)
    if fn.comment is not None:
        tFile.write(fn.comment)

    tFile.write(utils_ascii.ESC)
    # ID3 - tag: Genre (can be empty)
    if fn.genre is not None:
        tFile.write(fn.genre)

    tFile.write(utils_ascii.FS)

    # new line
    tFile.write(utils_ascii.NL)

    # end def write_fileTag


# function write_folder
# write a folder (one line) in a ".col" file as described in https://mac.sourceforge.net/
# param tFile : the stream on the ".col" file
# param cn : the CollectionNode to write in colFile
def write_folder_line(tFile, cn: FolderNode):
    iLevel = cn.depth - 1
    for x in range(iLevel):
        tFile.write(utils_ascii.TAB)

    # Name(max.  250 characters)
    tFile.write(cn.name)
    tFile.write(utils_ascii.SOH)
    # Size(kilobytes)
    iSize = floor(cn.size / 1024)
    tFile.write( str(iSize) )
    tFile.write(utils_ascii.STX)
    # Duration(seconds)
    iDurationInSeconds = floor(cn.duration)
    tFile.write( str(iDurationInSeconds))
    tFile.write(utils_ascii.ETX)
    # Subfolder count
    tFile.write( str(cn.folderCount) )
    tFile.write(utils_ascii.EOT)
    # File count
    tFile.write( str(cn.fileCount) )
    tFile.write(utils_ascii.ENQ)

    # new line
    tFile.write(utils_ascii.NL)

    # end of def write_folder

# function write_volume
# write a volume (one line) in a ".col" file as described in https://mac.sourceforge.net/
# param tFile : the stream on the ".col" file
# param vn : the VolumeNode to write in colFile
def write_volume_line(tFile, vn: VolumeNode):

    tFile.write(utils_ascii.TAB)
    # Name(CD - Label and Path, if not Root)
    tFile.write(vn.name)
    tFile.write(utils_ascii.SOH)
    # Size(kilobytes)
    iSize = floor(vn.size / 1024)
    tFile.write( str(iSize) )
    tFile.write(utils_ascii.STX)
    iDurationInSeconds = floor(vn.duration)
    tFile.write( str(iDurationInSeconds))
    tFile.write(utils_ascii.ETX)
    #Folder count
    tFile.write(  str(vn.folderCount))
    tFile.write(utils_ascii.EOT)
    # File count
    tFile.write( str(vn.fileCount) )
    tFile.write(utils_ascii.ENQ)
    # TODO handle last change date
    tFile.write("45641")
    tFile.write(utils_ascii.ACK)
    # Serial number of CD / HDD
    # TODO handle serial number
    tFile.write("-1832560112")
    tFile.write(utils_ascii.BEL)
    # Volume Type : \
    #    1 - Removable
    #    2 - Fixed(HDD)
    #    3 - Remote(Network)
    #    4 - CD - ROM
    #    5 - RAM disk
    #    6 - Audio CD
    # TODO volume type
    tFile.write("2")
    tFile.write(utils_ascii.BS)

    # new line
    tFile.write(utils_ascii.NL)

    # end of def write_volume

# function write_collection
# write a collection (one line) in a ".col" file as described in https://mac.sourceforge.net/
# param colFile : the stream on the ".col" file
# param collectionNode : the collectionNode to write in colFile
def write_collection_line(colFile, collectionNode: CollectionNode):
    colFile.write(utils_ascii.SOH)
    iSize = floor(collectionNode.size / 1024)
    colFile.write( str(iSize) )      # Size (kilobytes)
    colFile.write(utils_ascii.STX)
    fDuration = floor(collectionNode.duration)
    colFile.write( str(fDuration) )        # Duration (seconds)
    colFile.write(utils_ascii.ETX)
    colFile.write( str(collectionNode.folderCount) )            # Volume count
    colFile.write(utils_ascii.EOT)
    colFile.write( str(collectionNode.fileCount) )          # File count
    colFile.write(utils_ascii.ENQ)
    # TODO handle last change date
    colFile.write("45641")        # Date (last change)
    colFile.write(utils_ascii.ACK)

    # new line
    colFile.write(utils_ascii.NL)

    # end of def write_col