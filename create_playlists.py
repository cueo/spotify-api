from __future__ import print_function
from data import *
from tracks import tracks
import sys
import pprint

import spotipy
import spotipy.util as util

query_list = []
music_list_raw = tracks.split('\n\n')
for item in music_list_raw:
	music_list_clean = item.split('\n')
	query_list.append([music_list_clean[0]])
	for music in music_list_clean[1:]:
		query_list[-1].append(music_list_clean[0] + ' ' + music)

username = sys.argv[0]
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

if token:
	sp = spotipy.Spotify(auth=token)
	sp.trace = False
	for query in query_list:
		track_ids = []
		playlist_name = query[0]
		print('Creating playlist:', playlist_name)
		playlist = sp.user_playlist_create(username, playlist_name)
		playlist_id = playlist['id']
		# pprint.pprint(playlists)
		for track in query[1:]:
			results = sp.search(q=track, limit=1)
			try:
				item = results['tracks']['items'][0]
			except:
				print("Couldn't find track:", track)
			# print(item['name'], item['uri'])
			track_ids.append(item['uri'])
		results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
		print(results)

else:
	print("Can't get token for", username)