# ring downloader
- a general purpose script for interacting with ring products 



### A callout to the library that makes it possible
- https://github.com/tchellomello/python-ring-doorbell


![alt text](https://github.com/chris17453/ring_automation/blob/master/example/Screenshot%20from%202020-08-26%2011-28-17.png?raw=true "Example Video Image")

## Usage
```
$ python ring_downloader.py  -h

usage: ring_downloader [options]

interact with ring devices

optional arguments:
  -h, --help            show this help message and exit
  -i, --device-info     print device info
  -d, --download        download device videos
  -b, --doorbell-events
                        show doorbell events
  --list-videos         list all device videos
  --data DATA           set output data dir
```


## doorbell event list example
```bash
 $ python ring_downloader.py -b
 - ID:       6864885519054005002
 - Kind:     on_demand
 - Answered: True
 - When:     2020-08-25 11:41:54+00:00
 - ----------------------------------------------------------------------------------------------------
 - ID:       6864605736294409600
 - Kind:     motion
 - Answered: False
 - When:     2020-08-24 17:36:12+00:00
 - ----------------------------------------------------------------------------------------------------
 ```

 ## device info example
```bash
 $ python ring_downloader.py -i
 - Data Dir: /home/nd/repos/ring
 - Device Information
 - Address:    123 Mockingbird Lane, GA, 30012, US
 - Family:     chimes
 - ID:         49278390
 - Name:       Downstairs
 - Timezone:   America/New_York
 - Wifi Name:  WyFySSID
 - Wifi RSSI:  -45.0
 - ----------------------------------------------------------------------------------------------------
 - Address:    123 Mockingbird Lane, GA, 30012, US
 - Family:     doorbots
 - ID:         49276358
 - Name:       Front Door
 - Timezone:   America/New_York
 - Wifi Name:  WyFySSID
 - Wifi RSSI:  -70.0
 - ----------------------------------------------------------------------------------------------------
```

## list videos example
```bash
 $ python ring_downloader.py -v
 - Data Dir: /home/nd/repos/ring
 - Videos
 - video: doorbots,Front Door,6865268883539879306
 - video: doorbots,Front Door,6865015484764382602
 - video: doorbots,Front Door,6864933923335431602
 - video: doorbots,Front Door,6864933657047459200
 - video: doorbots,Front Door,6864909669655111100
 - ----------------------------------------------------------------------------------------------------
```


## download videos example
```bash
 $ python ring_downloader.py -d
 - Data Dir: /home/nd/repos/ring
 - Downloading Videos
 - Skipping: /home/nd/repos/ring/videos/doorbots/Front Door/6865268883539879366.mp4
 - Downloaded: 6865015484764382662 to /home/nd/repos/ring/videos/doorbots/Front Door/6865015484764382662.mp4
 - Downloaded: 6864933923335431622 to /home/nd/repos/ring/videos/doorbots/Front Door/6864933923335431622.mp4
 - Downloaded: 6864933657047459270 to /home/nd/repos/ring/videos/doorbots/Front Door/6864933657047459270.mp4
```