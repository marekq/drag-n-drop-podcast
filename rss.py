#!/usr/bin/env python
# marek kuczynski
# www.marek.asia
# sudo apt-get install python-eyed3

import eyeD3, sys, os, hashlib, time
from SimpleXMLWriter import XMLWriter
# import configuration file
from cfg import *

###
# define the output of the program (either stdout or file)
xml = XMLWriter('rss.xml')

# head of the file
output = xml.start('rss', version='2.0')

# channel part of the file
xml.start('channel')
xml.element('title', title)
xml.element('link', url)
xml.element('language', 'en-us')
xml.element('description', description)
xml.element('author', author)
xml.element('category', category)

xml.start('image')
xml.element('url', image)
xml.end('image')

# channel owner information
xml.start('owner')
xml.element('name', author)
xml.element('email', email)
xml.end('owner')

# check of the dirpath for music has been defined, else set to current dir
if musicpath == "":
	musicpath = '.'

# calculate the amount of chars in the defined webroot
rootchars = int(musicpath.count('')) - 1

# crawl the current directory recursively
for dirname, dirnames, filenames in os.walk(musicpath):
    for filename in filenames:
	if 'mp3' in filename or 'm4a' in filename:
		# define the path of the fime
		path = os.path.join(dirname, filename)
		# get the dir structure from the webroot
		webpath = path[rootchars:]
		# create a new item for every file
		xml.start('item')
		tag = eyeD3.Tag()
		tag.link(path)
		fileinfo = eyeD3.Mp3AudioFile(path)

		# retrieve several required fields
		xml.element('title', filename.split('.')[0])
                xml.element('enclosure', url=str(url + '/' + webpath), length=str(fileinfo.getSize()), type='audio/mpeg')
		xml.element('pubDate', time.ctime(os.path.getctime(path)))
		xml.element('category', webpath.split('/')[0])
		xml.element('description', str(webpath.split('/')[0]))
		
		# the following attributes are optional, uncomment if needed
		xml.element('duration', fileinfo.getPlayTimeString())
		xml.element('keywords', tag.getComment())
                xml.element('album', tag.getAlbum())
		xml.element('bpm', tag.getBPM())
                xml.element('author', tag.getArtist())
		xml.element('link', link)
		
		# calculate the guid by making an md5 hash
		guid = hashlib.md5()
		guid.update(tag.getTitle() + tag.getArtist() + path)
		xml.element('guid', guid.hexdigest())
		xml.end('item')

# close tags and write file
#xml.end('channel')
xml.close(output)
