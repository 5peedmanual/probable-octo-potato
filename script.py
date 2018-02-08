import my_module as mm
import json
import sys
import requests
from bs4 import BeautifulSoup
import argparse

headers = {
	'User-Agent': 'Not a bot',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Host': 'www.onlinevideoconverter.com',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
}

headers2 = {
	'Host': 'www.onlinevideoconverter.com',
	'User-Agent': 'Not a bot',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Referer': 'https://www2.onlinevideoconverter.com/video-converter',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'X-Requested-With': 'XMLHttpRequest',
	'Connection': 'keep-alive'
}

def goto_convert(link):
	global session
	global convert_url

	convert_url = 'https://www2.onlinevideoconverter.com/webservice'
	session = requests.session() # create a session to onlinevideoconverter.com

	payloadjson = {
		'function':	'validate',
		'args[dummy]': '1',
		'args[urlEntryUser]': str(link),
		'args[fromConvert]': 'urlconverter',
		'args[requestExt]': str(args.format),
		'args[nbRetry]': '0',
		'args[videoResolution]': '-1',
		'args[audioBitrate]': str(args.bitrate),
		'args[audioFrequency]': '0',
		'args[channel]': 'stereo',
		'args[volume]': '0',
		'args[startFrom]': '-1',
		'args[endTo]': '-1',
		'args[custom_resx]': '-1',
		'args[custom_resy]': '-1',
		'args[advSettings]': 'true',
		'args[aspectRatio]': '-1'
	}

	print('[i] Link: '+ link)
	print('[+] sending POST request...')
	post = session.post(convert_url, data=payloadjson, headers=headers2)
	print('[+] success.')
	json = str(post.json())
	print(str(post.json()))

	getcheck_id(json, link)

# filter the id and check if it's zero. this happens when the json response status is ok or failed
def getcheck_id(json, link):
	id = json.split('dPageId')[1].split('\': ')[1].split(',')[0]
	status = json.split('status')[1].split('\': u\'')[1].split('\',')[0]

	# happens on some videos
	if(status == 'failed'):
		print('[!!] Failed to convert link!')
		return -1

	# filter 'u' from id
	# not found
	if(id.find('u') == -1):
		print('Id: ' + id + '\n')
		if(id == '0'):
			send_payload_ok(json, link)
		else:
			send_payload_default(id)

	# found
	elif(id.find('u') == 0):
		id = id.split('u')[1].split('\'')[1]
		print('[i] Id: ' + id)
		if(id == '0'):
			send_payload_ok(json, link)
		else:
			send_payload_default(id)
	else:
		print('[!!] Something bad happened!')
		return -1;


# usually the first json response status will be default and send the id with it
# but after the first the rest will be will be status ok which means that you need to extract the server id
# the server url and the id process and then send a new post with that info. Afterwards you will receive the id
def send_payload_ok(json, link):

	serverId = json.split('serverId')[1].split(': u\'')[1].split('\'')[0]
	print('[i] serverId: '+ serverId)
	serverUrl = json.split('serverUrl')[1].split(': u\'')[1].split('\'')[0]
	print('[i] serverUrl: '+ serverUrl)
	id_process = json.split('id_process')[1].split(': u\'')[1].split('\'')[0]
	print('[i] id_process: '+ id_process)

	payloadjson_processVideo = {
		'function':	'processVideo',
		'args[dummy]': '1',
		'args[urlEntryUser]': str(link),
		'args[fromConvert]': 'urlconverter',
		'args[requestExt]': str(args.format),
		'args[serverId]': str(serverId),
		'args[nbRetry]': '0',
		# 'args[title]': '0',
		'args[serverUrl]': str(serverUrl),
		'args[id_process]': str(id_process),
		'args[videoResolution]': '-1',
		'args[audioBitrate]': str(args.bitrate),
		'args[audioFrequency]': '0',
		'args[channel]': 'stereo',
		'args[volume]': '0',
		'args[startFrom]': '-1',
		'args[endTo]': '-1',
		'args[custom_resx]': '-1',
		'args[custom_resy]': '-1',
		'args[advSettings]': 'true',
		'args[aspectRatio]': '-1'
	}

	print(payloadjson_processVideo)

	print('\n[+] sending POST request OK...')
	post = session.post(convert_url, data=payloadjson_processVideo, headers=headers2)
	print('[+] success.')
	print('[+] checking id...')
	jsonpostok = str(post.json())
	print('\n\n' + jsonpostok + '\n\n')
	getcheck_id(jsonpostok, link)
	# get_download_link()

def send_payload_default(id):
	success_url = 'https://www.onlinevideoconverter.com/success?id='+id
	print('[+] idurl: ' + success_url)
	print('[+] sending GET request... ')
	get_with_id = requests.get(success_url, headers=headers)
	print('[+] success.')
	# mm.write_to_file("idget.html", get_with_id.text, 1)
	get_download_link(get_with_id.text)

# parse the download link and the song name
default_count = 1
def get_download_link(response):
        global default_count
	get_with_id_download_soup = BeautifulSoup(response, 'html.parser')
	#get the name of the song
	b = get_with_id_download_soup.find("b")
	# print(b)

        #song_name = str("'u'OBES\xd8N - Drugs").encode('utf-8')
        try:
            song_name = b.a['title'].encode('utf-8')
            song_name = str(song_name)
	    print('[i] Song name: ' + song_name + '\n')
        except IOError as error:
            print('[!!] Error writing song name ' + str(error))
            song_name = 'default' + default_count
            default_count += 1
	# get the url of the download
	a_download = get_with_id_download_soup.find(id="downloadq")
	a_download_href = a_download.get('href')
	#print(a_download_href)
	# print(parse_js.find_all('dPageId'))
	download(a_download_href, song_name)
	print('[+] Complete.\n')

# download the song
def download(url, name):
	print('\n[+] Downloading...')
	rdownload = requests.get(url, stream=True)
	downloads = 'Downloads/' ### create this folder
	with open((downloads+name), 'wb') as f:
		for chunk in rdownload.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	return name

# get the links of the songs on the playlist
def parse_youtube(link):
	get_yt_html = requests.get(link) # get the playlist yt page
	yt_html_soup = BeautifulSoup(get_yt_html.text, "html.parser") # create a soup with it
	td = yt_html_soup.find_all("td", {"class": "pl-video-title"})
	td_soup = BeautifulSoup(str(td), "html.parser")
	a = td_soup.find_all("a", {"class": "pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link "})
	a_soup = BeautifulSoup(str(a), "html.parser")

	links = []
	ls = a_soup.find_all('a')
	youtube = 'https://www.youtube.com'
	for link in ls:
		link = (youtube+link.get('href'))
		print(link)
		goto_convert(link)
		#links.append(youtube+str(link.get('href')))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download your playlist')
	parser.add_argument('link', help='Link to playlist')
	parser.add_argument('--bitrate', type=str, default='192',
	 metavar='320 kbps, 256 kbps, 192 kbps, 128 kbps, 96 kbps, 64 kbps',
	 help='Audio bit rate (default 192 kbps)')
	parser.add_argument('--format', default='mp3',
	 metavar='.mp3, .aac, .ogg, .m4a, .wma, .fkac, .wav',
	 help='Audio formats (default mp3)' )
	args = parser.parse_args()
	playlist_link = args.link
	# print(playlist_link)
	parse_youtube(playlist_link)
        
