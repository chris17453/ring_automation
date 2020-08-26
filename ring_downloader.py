import os
import errno
import json
import argparse
import getpass
from pathlib import Path
from pprint import pprint
from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError




user_agent="RingAutomation/1.0"
cache_file = Path("ring_creds.cache")

def init():
    
    if cache_file.is_file():
        auth = Auth(user_agent, json.loads(cache_file.read_text()), token_updated)
    else:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        auth = Auth(user_Agent, None, token_updated)
        try:
            auth.fetch_token(username, password)
        except MissingTokenError:
            auth.fetch_token(username, password, otp_callback())

    ring = Ring(auth)
    ring.update_data()
    return ring

def info(msg):
    print(" - {0}".format(msg))

def download(deck,data_dir,device_type,device):
    base_dir=os.path.join(data_dir,'videos',device_type,device)
    
    # make a directory for this base dir if it doesnt exist
    try:
        if os.path.exists(base_dir)==False: 
            os.makedirs(base_dir)
    except OSError as e:
        if errno.EEXIST != e.errno:
            raise

    count = 0
    eid = 0
    while True:
        events = deck.history()
        for event in events:
            eid = event['id']

            file_name=os.path.join(base_dir,'{0}.mp4'.format(eid))
            if os.path.exists(file_name)==True:
                info("Skipping: {0}".format(file_name))
                continue

            deck.recording_download(eid, filename=file_name)
            info('Downloaded: {0}'.format(file_name))
            count += 1
    

def token_updated(token):
    cache_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code

def list_videos(ring):
    info("Videos")
    devices = ring.devices()
    
    for device_type in devices:
            if len(devices[device_type])>0:
                if device_type=='chimes': continue
                for device in devices[device_type]:
                    deck = device
        
                    events = deck.history()
                    for event in events:
                        eid = event['id']
                        if eid < LAST_ONE:
                            continue
                        info('video: {0},{1},{2}'.format(device_type,device.name,event['id']))


    info('--' * 50)

def download_videos(ring,data_dir):
    info("Downloading Videos")
    devices = ring.devices()
    
    for device_type in devices:
        if device_type=='chimes': continue
        if len(devices[device_type])>0:
            for device in devices[device_type]:
                deck = device
                download(deck,data_dir,device_type,device.name)
    info('--' * 50)

def show_doorbell_events(ring):
    info("Doorbell events")
    devices = ring.devices()
    for doorbell in devices['doorbots']:

        # listing the last 15 events of any kind
        for event in doorbell.history(limit=15):
            info('ID:       %s' % event['id'])
            info('Kind:     %s' % event['kind'])
            info('Answered: %s' % event['answered'])
            info('When:     %s' % event['created_at'])
            info('--' * 50)

        # get a event list only the triggered by motion
        events = doorbell.history(kind='motion')    

def show_info(ring):
    info("Device Information")
    devices = ring.devices()
    for dev in list(devices['stickup_cams'] + devices['chimes'] + devices['doorbots']):
        dev.update_health_data()
        info('Address:    %s' % dev.address)
        info('Family:     %s' % dev.family)
        info('ID:         %s' % dev.id)
        info('Name:       %s' % dev.name)
        info('Timezone:   %s' % dev.timezone)
        info('Wifi Name:  %s' % dev.wifi_name)
        info('Wifi RSSI:  %s' % dev.wifi_signal_strength)
        info('--' * 50)


if __name__ == "__main__":

    data_dir=os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser("ring_downloader", usage='%(prog)s [options]', description="""download ring videos""", epilog="")
    parser.add_argument('-i', '--device-info'     , help='print device info',action="store_true")
    parser.add_argument('-d', '--download'        , help='download device videos',action="store_true")
    parser.add_argument('-b', '--doorbell-events' , help='show doorbell events',action="store_true")
    parser.add_argument(      '--list-videos'     , help='list all device videos',action="store_true")
    parser.add_argument(      '--data'            , help='set output data dir',default=data_dir)
     
    args = parser.parse_args()
    info("Data Dir: {0}".format(args.data))

    ring=init()
    if args.download==True:
        download_videos(ring,args.data)

    if args.device_info==True:
        show_info(ring)

    if args.doorbell_events==True:
        show_doorbell_events(ring)

    if args.list_videos==True:
        list_videos(ring)

