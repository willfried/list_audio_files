##################################################################
# How to write a audio file (mp3, flac) collection in a export file?
#
# This file gathers the classes allowing to build the collection
# These classes are implementing bigtree
# bigtree is a python library, see https://github.com/kayjan/bigtree
# * class CollectionNode(Node)
#   a Collection Node contains one or many VolumeNode
# * class VolumeNode(Node)
#   a VolumeNode is a folder under the root (1st level)
#   a VolumeNode contains folders handled as FolderNode and audio files handled as FileNode
# * class FolderNode(Node)
#   a FolderNode contains folders and files
# * class FileNode
#   the audio files are handled as FileNode
##################################################################

from bigtree import Node

"""
@attribute name : File name (max. 250 characters)
@attribute size : Size (kilobytes)
@attribute duration : Duration (seconds), a negative number means "VBR" - coded with variable bit rate
@attribute sampleRate : Sample Rate (without last 0 - e.g. 4410)
Kanal mode : 
    Stereo = 1
    Joint Stereo = 2
    Dual Channel = 3
    Mono = 4
MPEG Version:
    Unknown = 0
    V1 = 1
    V2 = 2
    V2.5 = 3
    MPEG+ SV4..7 = 4..7
    Windows PCM = 9
    TwinVQ = 10
    Ogg Vorbis = 20
    Windows Media Audio = 25
    Monkey's Audio = 30
    FLAC = 35
    OptimFROG = 40
    AAC = 45
    WavPack = 50
MPEG Layer:
    Unknown = 0
    L1..3 = 1..3 or MPEG+ SV7 Profile 1..5 = 1..5
    Windows PCM, Monkey's Audio or FLAC = 8, 16 (bit)
    TwinVQ = 10
    Ogg Vorbis = 20
    Windows Media Audio = 25
@attribute title : ID3-tag : Title (can be empty)
@attribute artist : ID3-tag : Artist (can be empty)
@attribute album : ID3-tag : Album (can be empty)
@attribute track : ID3-tag : Track number (can be empty)
@attribute year : ID3-tag : Year (can be empty)
@attribute comment : ID3-tag : Comment (can be empty)
@attribute genre : ID3-tag : Genre (can be empty)
"""
class FileNode(Node):

    def __init__(self, name: str, iSize: int, iDuration :int, iSampleRate :int,
                 title :str, artist :str, album :str, track :str, year :str, comment :str, genre :str,
                 bitdepth :int, channels :int, **kwargs):
        super().__init__(name, **kwargs)
        self._size = iSize
        self._duration = iDuration
        self._sampleRate = iSampleRate
        self._title = title
        self._artist = artist
        self._album = album
        self._track = track
        self._year = year
        self._comment = comment
        self._genre = genre
        self._bitdepth = bitdepth
        self._channels = channels

    @property
    def size(self):
        return self._size

#    @size.setter
#    def size(self, value):
#        self._size = value

    @property
    def duration(self):
        return self._duration

#    @duration.setter
#    def duration(self, value):
#        self._duration = value

    @property
    def sampleRate(self):
        return self._sampleRate

#    @sampleRate.setter
#    def sampleRate(self, value):
#        self._sampleRate = value

#
    @property
    def title(self):
        return self._title

#    @title.setter
#    def title(self, value):
#        self._title = value

    @property
    def artist(self):
        return self._artist

#    @artist.setter
#    def artist(self, value):
#        self._artist = value

    @property
    def album(self):
        return self._album

#   @album.setter
#    def album(self, value):
#        self._album = value

    @property
    def track(self):
        return self._track

#    @track.setter
#    def track(self, value):
#        self._track = value

    @property
    def year(self):
        return self._year

#    @year.setter
#    def year(self, value):
#        self._year = value

    @property
    def comment(self):
        return self._comment

#    @comment.setter
#    def comment(self, value):
#        self._comment = value

    @property
    def genre(self):
        return self._genre

    @property
    def bitdepth(self):
        return self._bitdepth

    @property
    def channels(self):
        return self._channels


#    @genre.setter
#    def genre(self, value):
#        self._genre = value

    @property
    def folderCount(self):
        return 0

    @property
    def fileCount(self):
        return 1

# end class FileNode(Node)

"""
Name (max. 250 characters)
Size (kilobytes)
Duration (seconds)
Subfolder count
File count
"""
class FolderNode(Node):

    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    @property
    def size(self):
        return sum([child.size for child in self.children])

    @property
    def duration(self):
        return sum([child.duration for child in self.children])

    """
    the folder amount is the amount of folder of the current folder added to the children folder amount
    """
    @property
    def folderCount(self):
        folderCount = 0
        itemList = self.children
        for i in itemList:
            if isinstance(i, FolderNode):
                folderCount += 1
        folderCount += sum([child.folderCount for child in self.children])
        return folderCount

    @property
    def fileCount(self):
        return sum([child.fileCount for child in self.children])

# end class FolderNode(Node)

"""
FolderNode : Name (CD-Label and Path, if not Root)
Size (kilobytes)
Duration (seconds)
Folder count
File count
# Date (adding to collection), see "last change date"
# Serial number of CD/HDD
# Volume Type: 1 - Removable | 2 - Fixed (HDD) | 3 - Remote (Network) | 4 - CD-ROM | 5 - RAM disk | 6 - Audio CD
"""
class VolumeNode(Node):

    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    @property
    def size(self):
        return sum([child.size for child in self.children])

    @property
    def duration(self):
        return sum([child.duration for child in self.children])
    """
    the folder amount is the amount of folder of the current folder added to the children folder amount
    """
    @property
    def folderCount(self):
        folderCount = 0
        itemList = self.children
        for i in itemList:
            if isinstance(i, FolderNode):
                folderCount += 1
        folderCount += sum([child.folderCount for child in self.children])
        return folderCount

    @property
    def fileCount(self):
        return sum([child.fileCount for child in self.children])

"""
Size (kilobytes)
Duration (seconds)
Volume count
File count
TODO Date (last change), the number of days that have passed since 12/30/1899
"""
class CollectionNode(Node):

    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        print("CollectionNode.init : name"+name)

    @property
    def size(self):
        return sum([child.size for child in self.children])

    @property
    def duration(self):
        return sum([child.duration for child in self.children])

    @property
    def folderCount(self):
        return sum([child.folderCount for child in self.children])

    @property
    def fileCount(self):
        return sum([child.fileCount for child in self.children])