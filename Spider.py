import urllib2
import bs4
import time
import re
import logging
import os
import random

#TO-DO: Nested CD Dirs in Album
#TO-DO: Album Count on Page

#url = "http://www.folkoteka.org:7080/NOVO-2012-2013DLNOV0ollllIllIlhdweruuuuuuuuuu/"
url = "http://www.folkoteka.org:7080/NOVO-2012-2013DLNOV0ollllIllIlhdweruuuuuuuuuu/index.php?order=mod&direction=0"

downloadBaseLocation = '/Users/sgloutnikov/Downloads/Folkoteka/'
mp3Pattern = re.compile('.*action=downloadfile.*mp3&.*', re.UNICODE)
zipPattern = re.compile('.*action=downloadfile.*zip&.*', re.UNICODE)
dirPattern = re.compile('.*&directory.*', re.UNICODE)
downloadCurrent = 0
# Inclusive Range
downloadStart = 0
downloadEnd = 10

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


def createAlbumDirectory(basePath, title):
    fullPath = basePath + title
    try:
        os.makedirs(fullPath)
    except OSError:
        if not os.path.isdir(fullPath):
            logging.exception(fullPath)
            raise

# Start
request = urllib2.Request(url)
response = urllib2.urlopen(request)
soup = bs4.BeautifulSoup(response)
# All Links
for link in soup.find_all('a'):
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
        createAlbumDirectory(downloadBaseLocation, albumTitle)
        print('+++ STARTING ALBUM (' + str(downloadCurrent) + '): ' + albumTitle)
        logging.info('+++ STARTING ALBUM (' + str(downloadCurrent) + '): ' + albumTitle + ' FROM: ' + folderUrl)
        downloadCurrent += 1
        request2 = urllib2.Request(folderUrl)
        response2 = urllib2.urlopen(request2)
        soup2 = bs4.BeautifulSoup(response2)
        # Song Links
        for link2 in soup2.find_all('a'):
            songHref = str(link2.get('href'))
            if (mp3Pattern.search(songHref) or zipPattern.search(songHref)):
                time.sleep(random.randint(1,2))
                songUrl = url + str(link2.get('href')).replace(' ', '%20')
                logging.info('++ STARTING SONG FROM: ' + songUrl)
                download(songUrl, downloadBaseLocation + albumTitle + '/')

logging.info('=== Finished Download for Range: ' + str(downloadStart) + ' - ' + str(downloadEnd))
print('=== Finished Download for Range: ' + str(downloadStart) + ' - ' + str(downloadEnd))




#if 'national-park' in a['href']:
#    print 'found a url with national-park in the  link'