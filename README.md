# MP3 Spider

A small script to download MP3 albums in their proper directories from a website with hotlink protection. The script recursively crawls directories until it finds mp3/zip/rar files and downloads them in the same path structure locally.  

Supports downloading item ranges for easier resuming if the amount of songs is large, or picking exactly which albums to download from a large list.


<b>Base</b> (url):<br>
-<u>Album</u> (dirPattern match)<br>
--> Song.mp3 (urlBase + songHref)<br>
--> Song.mp3 (urlBase + songHref)<br>
--> Song.mp3 (urlBase + songHref)<br>
-<u>Album</u> (dirPattern match)<br>
-- <u>CD1</u>(dirPattern match)<br>
---> Song1.zip (urlBase + songHref)<br>
---> Song2.zip (urlBase + songHref)<br>
-- <u>CD2</u> (dirPattern match)<br>
---> Song1.zip (urlBase + songHref)<br>
---> Song2.zip (urlBase + songHref)<br>
---> SOng3.zip (urlBase + songHref)<br>
