import datetime
import xtream

import config

delimiter = "=====================================================\n"

x = xtream

# login details
x.server   = config.provider['server']
x.username = config.provider['username']
x.password = config.provider['password']

r = x.authenticate()

data = r.json()

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

  s = x.streams(x.liveType)
  live_stream_data = s.json() 

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
    print('Total Live Streams:                             {0:>4d}'.format(total_streams))
    print(delimiter)

    # List streams by live category
    for category in live_category_data:
        print(f"Category: {category['category_name']} (ID: {category['category_id']})")
        cat_streams = [stream for stream in live_stream_data if stream['category_id'] == category['category_id']]
        if cat_streams:
            for stream in cat_streams:
                print(f"  - {stream.get('name', 'Unnamed Stream')} (ID: {stream.get('stream_id', 'N/A')})")
        else:
            print("  No streams in this category.")
        print(delimiter)  # Blank line between categories

except ValueError as err:
  print("Value error: {0}".format(err))