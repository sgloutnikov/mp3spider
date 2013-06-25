import urllib2
import bs4
import time
import re
import logging
import os
import random

#TO-DO: Nested CD Dirs in Album

url = "http://www.folkoteka.org:7080/NOVO-2012-2013DLNOV0ollllIllIlhdweruuuuuuuuuu/"
#url = "http://www.folkoteka.org:7080/NOVO-2012-2013DLNOV0ollllIllIlhdweruuuuuuuuuu/index.php?order=mod&direction=0/"

downloadBaseLocation = '/Users/sgloutnikov/Downloads/Folkoteka/'
downloadAlbumLocation = downloadBaseLocation
mp3Pattern = re.compile('.*action=downloadfile.*mp3&.*', re.UNICODE)
zipPattern = re.compile('.*action=downloadfile.*zip&.*', re.UNICODE)
dirPattern = re.compile('.*&directory.*', re.UNICODE)
downloadCurrent = 0
totalAlbums = 0
# Inclusive Range
downloadStart = 0
downloadEnd = 0

logging.basicConfig(filename='./log/fs-'+str(downloadStart)+'-'+str(downloadEnd)+'.log', format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', \
                    datefmt='%m-%d %H:%M', level=logging.DEBUG)


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
        if dirPattern.search(str(link.get('href'))):
            count += 1
    return count


# Start
totalAlbums = countDirs(url)
albumSoup = getSoup(url)
# All Links
for link in albumSoup.find_all('a'):
    folderUrl = url + str(link.get('href')).replace(' ', '%20')
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
        downloadAlbumLocation = downloadAlbumLocation + albumTitle + '/'
        createAlbumDirectory(downloadAlbumLocation)
        print('+++ STARTING ALBUM (' + str(downloadCurrent) + ' of total ' + str(totalAlbums) + '): ' + albumTitle)
        logging.info('+++ STARTING ALBUM (' + str(downloadCurrent) + '): ' + albumTitle + ' FROM: ' + folderUrl)
        downloadCurrent += 1
        songSoup = getSoup(folderUrl)
        # Song Links
        for link2 in songSoup.find_all('a'):
            songHref = str(link2.get('href'))
            # Song Found
            if (mp3Pattern.search(songHref) or zipPattern.search(songHref)):
                time.sleep(random.randint(1,2))
                songUrl = url + str(link2.get('href')).replace(' ', '%20')
                logging.info('++ STARTING SONG FROM: ' + songUrl)
                download(songUrl, downloadAlbumLocation)

logging.info('=== Finished Download for Range: ' + str(downloadStart) + ' - ' + str(downloadEnd))
print('=== Finished Download for Range: ' + str(downloadStart) + ' - ' + str(downloadEnd))
