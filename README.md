# MP3 Spider

A small script I wrote to download MP3 albums in their proper directories from a website with hotlink protection. The script recursively crawls directories until it finds mp3/zip/rar files and downloads them in the same path structure locally.  

Supports downloading item ranges for easier resuming if the amount of songs is large, or picking exactly which albums to download from a large list.


Base (url):
-Album (dirPattern)
--> Song.mp3 (urlBase + songHref)
--> Song.mp3 (urlBase + songHref)
--> Song.mp3 (urlBase + songHref)
-Album2 (dirPattern)
-- CD1 (dirPattern)
---> Song1.zip (urlBase + songHref)
---> Song2.zip (urlBase + songHref)
-- CD2 (dirPattern)
---> Song1.zip (urlBase + songHref)
---> Song2.zip (urlBase + songHref)
---> SOng3.zip (urlBase + songHref)
