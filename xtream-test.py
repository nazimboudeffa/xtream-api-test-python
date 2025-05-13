import requests
import datetime
import xtream
import json
import os

import config

delimiter = "=====================================================\n"

x = xtream

# login details
x.server   = config.provider['server']
x.username = config.provider['username']
x.password = config.provider['password']

r = x.authenticate()

data = r.json()

#writeJSON (providername + '-auth.json', data)

user_username = data['user_info']['username']
user_status = data['user_info']['status']
user_is_trial = data['user_info']['is_trial']
user_created_at = str(data['user_info']['created_at'])
if (user_created_at != 'None'):
  user_created_at = datetime.datetime.fromtimestamp(float(data['user_info']['created_at'].encode('ascii','ignore'))).isoformat()
user_auth = data['user_info']['auth']
user_allowed_output_formats = data['user_info']['allowed_output_formats']
user_exp_date = str(data['user_info']['exp_date'])
if (user_exp_date != 'None'):
  user_exp_date = datetime.datetime.fromtimestamp(float(data['user_info']['exp_date'].encode('ascii','ignore'))).isoformat()
user_active_cons = data['user_info']['active_cons']
user_message = data['user_info']['message']
user_password = data['user_info']['password']
user_max_connections = data['user_info']['max_connections']

server_https_port = data['server_info']['https_port']
server_url = data['server_info']['url']
server_time_now = data['server_info']['time_now']
server_server_protocol = data['server_info']['server_protocol']
server_timestamp_now = str(data['server_info']['timestamp_now'])
if (server_timestamp_now != 'None'):
  server_timestamp_now = datetime.datetime.fromtimestamp(float(data['server_info']['timestamp_now'])).isoformat()
server_timezone = data['server_info']['timezone']
server_rtmp_port = data['server_info']['rtmp_port']
server_port = data['server_info']['port']


# printing the output 
print("Account information:\n")

print('Username:               {}'.format(user_username))
print('Password:               {}'.format(user_password))
print('Message:                {}'.format(user_message))
print('Status:                 {}'.format(user_status))
print('Authorized:             {}'.format(user_auth))
print('Trial:                  {}'.format(user_is_trial))
print('Created:                {}'.format(user_created_at))
print('Expiration:             {}'.format(user_exp_date))
print('Allowed output formats: {}'.format(user_allowed_output_formats))
print('Max Connections:        {}'.format(user_max_connections))
print('Active connections:     {}'.format(user_active_cons))
      
print("\nServer information:\n")

print('Server address:         {}'.format(server_url))
print('Protocol:               {}'.format(server_server_protocol))
print('Port:                   {}'.format(server_port))
print('HTTPS port:             {}'.format(server_https_port))
print('RTMP port:              {}'.format(server_rtmp_port))
print('Timezone:               {}'.format(server_timezone))
print('Time now:               {}'.format(server_time_now))
print('Timestamp now:          {}'.format(server_timestamp_now))

total_streams = 0

print("\n\nCategory information:\n")

r = x.categories(x.liveType)

try:
  live_category_data = r.json() 
  
  #writeJSON (providername + '-live-categories.json', live_category_data)

  s = x.streams(x.liveType)
  live_stream_data = s.json() 

  #writeJSON (providername + '-live-streams.json', live_stream_data)

  # live_category_data is list of dict
  live_names = []
  live_IDs = []
  pos = 0
  while pos <= len(live_category_data) - 1:
    cat_streams_data = [item for item in live_stream_data if item['category_id'] == live_category_data[pos]['category_id']]
    live_names.append("{0:<40s} - {1:>3s} - {2:4d} streams".format(live_category_data[pos]['category_name'], live_category_data[pos]['category_id'], len(cat_streams_data)))
    total_streams += len(cat_streams_data)
    live_IDs.append(live_category_data[pos]['category_id'])
    pos += 1
  live_names.sort()

  if len(live_category_data) > 0:
    print('Live Category Count:                             {0:>4d}'.format(len(live_category_data)))
    print(delimiter)

    for i, entry in enumerate(live_names):
      print(entry)

    print(delimiter)
except ValueError as err:
  print("Value error: {0}".format(err))

r = x.categories(x.vodType)

try:
  vod_category_data = r.json() 

  #writeJSON (providername + '-vod-categories.json', vod_category_data)

  s = x.streams(x.vodType)
  vod_stream_data = s.json() 

  #writeJSON (providername + '-vod-streams.json', vod_stream_data)

  vod_names = []
  vod_IDs = []
  pos = 0
  while pos <= len(vod_category_data) - 1:
    cat_streams_data = [item for item in vod_stream_data if item['category_id'] == vod_category_data[pos]['category_id']]
    vod_names.append("{0:<40s} - {1:>3s} - {2:4d} streams".format(vod_category_data[pos]['category_name'], vod_category_data[pos]['category_id'], len(cat_streams_data)))
    total_streams += len(cat_streams_data)
    vod_IDs.append(vod_category_data[pos]['category_id'])
    pos += 1
  vod_names.sort()

  if len(vod_category_data) > 0:
    print(u'VOD Category Count:                              {0:>4d}'.format(len(vod_category_data)))
    print(delimiter)

    for i, entry in enumerate(vod_names):
      print(entry)

    print(delimiter)
except ValueError as err:
  print("Value error: {0}".format(err))

r = x.categories(x.seriesType)
try:
  series_category_data = r.json() 

  #writeJSON (providername + '-series-categories.json', series_category_data)

  s = x.streams(x.seriesType)
  series_stream_data = s.json() 

  #writeJSON (providername + '-series-streams.json', series_stream_data)

  series_names = []
  series_IDs = []

  pos = 0
  while pos <= len(series_category_data) - 1:
    cat_streams_data = [item for item in series_stream_data if item['category_id'] == series_category_data[pos]['category_id']]
    #writeJSON (series_category_data[pos]['category_id'] + '-stream-data.json', cat_streams_data)
    series_names.append(u"{0:<47s} - {1:>3s}".format(series_category_data[pos]['category_name'], series_category_data[pos]['category_id']))
    total_streams += len(cat_streams_data)
    series_IDs.append(series_category_data[pos]['category_id'])
    pos += 1
  series_names.sort()

  if len(series_category_data) > 0:
    print(u'Series Category Count:                           {0:>4d}'.format(len(series_category_data)))
    print(delimiter)

    for i, entry in enumerate(series_names):
      print(entry)

    print(delimiter)
except ValueError as err:
  print("Value error: {0}".format(err))

print('Total Stream Count:     {}\n'.format(total_streams))

NoneType = type(None)

if (config.display_live_info == 1):
  live_category_data.sort(key=VODName)
  for i, entry in enumerate(live_category_data):
    print('\n\nStreams for Live category {} - {}:\n'.format(entry['category_id'],entry['category_name']))
    cat_streams_data = [item for item in live_stream_data if item['category_id'] == entry['category_id']]
    print(u"{0:<75s} {1:>5s} {2:>4s} ".format('name','ID', 'EPG?'))
    print(delimiter)
    for i, stream in enumerate(cat_streams_data):
      print(u"{0:<75s} {1:>5d} {2:>4s}".format(stream['name'],stream['stream_id'],EPGString(stream['epg_channel_id'])))
    print(delimiter)
