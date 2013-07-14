import urllib2
import bs4
import time
import re
import logging
import os
import random

# URL & Paths, include traling '/'
# Base Url
urlBase = "http://www.folkoteka.org:7080/downloadstariiiIIIIIIIIIIIlllfdtgzjhzhftuuuuuu/"
# Main Url for different sort methods (ex. Sorted Url for Newest Album Listing 1st)
url = "http://www.folkoteka.org:7080/downloadstariiiIIIIIIIIIIIlllfdtgzjhzhftuuuuuu/index.php?direction=0&order=nom/"

downloadBaseLocation = 'F:/+Folkoteka+/'
downloadAlbumLocation = ''
# Identify entities in link by these patterns
mp3Pattern = re.compile('.*action=downloadfile.*mp3&.*', re.UNICODE)
zipPattern = re.compile('.*action=downloadfile.*zip&.*', re.UNICODE)
rarPattern = re.compile('.*action=downloadfile.*rar&.*', re.UNICODE)
dirPattern = re.compile('.*&direction.*&directory.*', re.UNICODE)
downloadCurrent = 0
totalAlbums = 0
# Inclusive Range
downloadStart = 109
downloadEnd = 125

logging.basicConfig(filename='./log/fs-'+str(downloadStart)+'-'+str(downloadEnd)+'.log', format='%(asctime)s: %(message)s', \
                    datefmt='%m-%d-%Y %H:%M', level=logging.DEBUG)


def createAlbumDirectory(fullPath):
    try:
        os.makedirs(fullPath)
    except OSError:
        if not os.path.isdir(fullPath):
            logging.exception(fullPath)
            raise


def getSoup(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    soup = bs4.BeautifulSoup(response)
    return soup


def countDirs(url):
    soup = getSoup(url)
    count = 0
    for link in soup.find_all('a'):
        if dirPattern.search(str(link.get('href'))) and str(link.get('title')) != 'None':
            count += 1
    return count


def download(url, albumDestination):
    s = urllib2.urlopen(url)
    # Get filename and strip "...";
    filename = s.info()['Content-Disposition'].split('filename=')[1]
    if filename[0] == '"' or filename[0] == "'":
        filename = filename[1:-2]
    logging.info('+ STARTING DOWNLOAD FOR: ' + filename)
    content = s.read()
    s.close()
    file = open(albumDestination + filename, 'wb')
    file.write(content)
    file.close()
    print('= DOWNLOADED: ' + filename)
    logging.info('= FINISHED DOWNLOAD FOR: ' + filename)


def processDir(songSoup, baseDirTitle, albumLocation):
    # Song Links
    for songLink in songSoup.find_all('a'):
        songHref = urllib2.quote(songLink.get('href').encode('iso-8859-1'), safe='/?=&')
        # Song Found
        if (mp3Pattern.search(songHref) or zipPattern.search(songHref) or rarPattern.search(songHref)):
            time.sleep(random.randint(1,2))
            songUrl = urlBase + songHref
            logging.info('+ STARTING SONG FROM: ' + songUrl)
            download(songUrl, albumLocation)
        # CD/Dir Found
        if (dirPattern.search(songHref)) and str(songLink.get('title')) != 'None':
            time.sleep(random.randint(1,2))
            newDirTitle = str(songLink.get('title'))
            newAlbumLocation = albumLocation + newDirTitle + '/'
            createAlbumDirectory(newAlbumLocation)
            dirUrl = url + songHref
            print ('++ FOUND DIRECTORY ' + newDirTitle + ' AT: ' + baseDirTitle)
            logging.info('++ FOUND DIRECTORY ' + newDirTitle + ' AT: ' + baseDirTitle)
            newSongSoup = getSoup(dirUrl)
            processDir(newSongSoup, newDirTitle, newAlbumLocation)


# Start
totalAlbums = countDirs(url)
albumSoup = getSoup(url)
# All Links
for link in albumSoup.find_all('a'):
    folderUrl = url + urllib2.quote(link.get('href').encode('iso-8859-1'), safe='/?=&')
    # Album Links
    if dirPattern.search(folderUrl) and str(link.get('title')) != 'None':
        # Album Range Download
        if not downloadStart <= downloadCurrent <= downloadEnd:
            downloadCurrent += 1
            continue
        # Finish Check
        if downloadCurrent > downloadEnd:
            break
        # Prepare Album Download
        time.sleep(random.randint(1, 3))
        albumTitle = str(link.get('title'))
        downloadAlbumLocation = downloadBaseLocation + albumTitle + '/'
        createAlbumDirectory(downloadAlbumLocation)
        print('+++ STARTING ALBUM (' + str(downloadCurrent) + ' of total ' + str(totalAlbums) + '): ' + albumTitle)
        logging.info('+++ STARTING ALBUM (' + str(downloadCurrent) + ' of total ' + str(totalAlbums) + '): ' + albumTitle + ' FROM: ' + folderUrl)
        downloadCurrent += 1
        # Process Dirs/Albums
        songSoup = getSoup(folderUrl)
        processDir(songSoup, albumTitle, downloadAlbumLocation)


logging.info('=== Finished Download for Range: ' + str(downloadStart) + ' - ' + str(downloadEnd))
print('=== Finished Download for Range: ' + str(downloadStart) + ' - ' + str(downloadEnd))
