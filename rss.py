#!/usr/bin/env python
# marek kuczynski
# www.marek.asia
# sudo apt-get install python-eyed3

import eyeD3, sys, os, hashlib, time
from SimpleXMLWriter import XMLWriter

###REQUIRED PART###
# define several variables for display in your podcast player
url = 'http://marek.asia/music'
name = 'marek'
title = 'podcast directory marekq'
description = 'mixtapes i share with friends'
author = 'marek'
category = 'music'
email = 'marek@marek.asia'
###REQUIRED PART###

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

# crawl the current directory recursively
for dirname, dirnames, filenames in os.walk('.'):
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
		xml.element('title', tag.getTitle())
		xml.element('enclosure', url=str(url + '/' + path[2:]), length=str(fileinfo.getSize()), type='type/' + os.path.splitext(filename)[1][1:])
		xml.element('pubDate', time.ctime(os.path.getmtime(path)))
		
		# the following attributes are optional, comment if needed
		xml.element('itunes:duration', fileinfo.getPlayTimeString())
		xml.element('itunes:keywords', tag.getComment())
                xml.element('album', tag.getAlbum())
		xml.element('bpm', tag.getBPM())
                xml.element('itunes:author', tag.getArtist())
		
		# calculate the guid by making an md5 hash
		guid = hashlib.md5()
		guid.update(tag.getTitle() + tag.getArtist() + path)
		xml.element('guid', guid.hexdigest())
		xml.end('item')

# close tags and write file
xml.end('channel')
xml.rssdeclclose()
xml.close(output)
