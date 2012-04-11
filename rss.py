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
output = xml.start('xml', version='1.0')
xml.element('podcast')
#output = xml.declaration()
xml.rssdecl()

# channel part of the file
xml.start('channel')
xml.element('title', title)
xml.element('link', url)
xml.element('language', 'en-us')
xml.element('description', description)
xml.element('itunes:author', author)
xml.element('itunes:category', category)
xml.start('itunes:owner')
xml.element('itunes:name', author)
xml.element('itunes:email', email)
xml.end('itunes:owner')

# check of the dirpath for music has been defined, else set to current dir
if musicpath == "":
	musicpath = '.'

# crawl the current directory recursively
for dirname, dirnames, filenames in os.walk(musicpath):
    for filename in filenames:
	if 'mp3' in filename or 'm4a' in filename:
		# define the path of the fime
		path = os.path.join(dirname, filename)
		
		# create a new item for every file
		xml.start('item')
		tag = eyeD3.Tag()
		tag.link(path)
		fileinfo = eyeD3.Mp3AudioFile(path)
		# retrieve several required fields
		# not having a title sucks, so replacing it if blank
		title = tag.getTitle()
		if title == '':
			title = filename
		xml.element('title', title)
		xml.element('enclosure', url=str(url + '/' + path[2:]), length=str(fileinfo.getSize()), type='type/' + os.path.splitext(filename)[1][1:])
		xml.element('pubDate', time.ctime(os.path.getctime(path)))
		
		# the following attributes are optional, comment if needed
		xml.element('itunes:duration', fileinfo.getPlayTimeString())
		xml.element('duration', fileinfo.getPlayTimeString())
		xml.element('itunes:keywords', tag.getComment())
                xml.element('album', tag.getAlbum())
		xml.element('bpm', tag.getBPM())
                xml.element('itunes:author', tag.getArtist())
		xml.element('author', tag.getArtist())
		xml.element('link', link)
		
		# calculate the guid by making an md5 hash
		guid = hashlib.md5()
		guid.update(tag.getTitle() + tag.getArtist() + path)
		xml.element('guid', guid.hexdigest())
		xml.end('item')

# close tags and write file
xml.end('channel')
xml.rssdeclclose()
xml.close(output)
