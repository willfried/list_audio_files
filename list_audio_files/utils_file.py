##################################################################
# How to write a audio file (mp3, flac) collection in a export file?
#
# This file gathers the functions handling folders or files counting, and relative path
##################################################################

import os

def __countFoldersInDir(pPath):
    total = sum([len(folder) for r, d, folder in os.walk(path)])
    #print("[debug][countFilesInDir] pPath/countFiles=["+pPath+"]["+str(total)+"]")
    return total
# end def countFoldersInDir

def __countFilesInDir(pPath):
    total = sum([len(files) for r, d, files in os.walk(pPath)])
    #print("[debug][countFilesInDir] pPathcountFolders=["+pPath+"]["+str(total)+"]")
    return total
# end def countFilesInDir

def __countSizeInDir(pPath):
    total = 0
    with os.scandir(pPath) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += countSizeInDir(entry.path)
    #print("[debug][countSizeInDir] Path    =["+pPath+"] has totalSize [" + str(total) + "]")
    return total
# end def countSizeInDir

def relativePath(pPath):
    # Split the path
    # @param pPath : example "G:/dir_a/dir_b/dir_c"
    # @return the relative path, example "dir_c"
    normPath = os.path.normpath(pPath)
    pathArray = normPath.split(os.sep)
    #print("[debug][relativePath] path : '% s:'" % pPath )
    #print("[debug][relativePath] path.length : '% s:'" % pPath, len(pathArray)  )
    returnPath = pathArray[ len(pathArray) - 1 ]
    #print("[debug][relativePath] return '% s:'" % returnPath)
    return returnPath

# end def relativePath