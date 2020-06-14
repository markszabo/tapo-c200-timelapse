# Time-lapse with a Raspberry Pi and a TP-Link Tapo C200 IP-Camera

This is my setup to take time-lapse videos from my balcony with a Raspberry Pi using a TP-Link Tapo C200 IP-Camera.

[![Time-lapse](https://yt-embed.herokuapp.com/embed?v=Gn30s9ypFZ0)](https://www.youtube.com/watch?v=Gn30s9ypFZ0 "Time-lapse")

## High level overview

The TP-Link Tapo C200 provides an rtsp feed for its video. Once a username and password is set in the app, it is available on: [rtsp://user:pass@192.168.a.b:554/stream1](rtsp://user:pass@192.168.a.b:554/stream1) (Use VLC to see if it works.)

My Raspberry Pi takes a snapshot from that video feed at a configurable interval. This would be possible with `ffmpeg`, however I found that due to rtsp using UDP by default, the end result was often corrupted. Thus my script uses the vlc library for python, which starts VLC in the background, waits for 10 seconds for the stream to get stable and then starts capturing snapshots. The script only runs for a short period of time (e.g. 10 minutes), and then it is restarted by cron to limit the issues around the camera dropping connectivity or rebooting.

Pictures are collected to a separate folder per day. After midnight an other script is run to assemble the daily timelapse from yesterday's pictures, and then delete most of the pictures (all but every 10th in my setup, but the rate is configurable). This is to save space, but still keep the option to do multi-day time-lapses (e.g. pictures of 2pm every day for a year).

In my setup I take a picture every minute, so that's 1440 pictures a day. With 24 fps it results in a 1 minute long video.

## Size requirements (with my setup):

* 1 picture: 1.8 MB
* 1 day worth of pictures (1 picture per minute): 2.6 GB
* 1 day's final video (60 seconds): 45 MB
* 1 day's pictures kept for later (1 picture per 10 minute, 144 pictures per day): 260 MB

## Dependencies

```
sudo apt install libvlc-dev
sudo pip3 install python-vlc
```

## Setup

1. `mv timelapseconfig.py_example timelapseconfig.py` and update it accordingly
2. `python3 capture.py` to see if it works
3. Check the images being created
4. If everything looks good, add it to crontab: `crontab -e`

```
*/10 * * * * /usr/bin/python3 /home/pi/timelapse/capture.py >> /tmp/timelapse.log
```
5. Wait for a day, check the images
6. Try the video assembly: `python3 makevideo.py`
7. If it looks good, add it to crontab as well: `crontab -e`

```
5 1 * * * /usr/bin/python3 /home/pi/timelapse/makevideo.py >> /tmp/timelapse_makevideo.log
```

This will run it at 1:05 am every night.

8. Wait until next month, check the images
9. Try the video assembly: `python3 monthlyvideo.py`
10. If it looks good, add it to crontab as well: `crontab -e`

```
5 4 1 * * /usr/bin/python3 /home/pi/timelapse/monthlyvideo.py >> /tmp/timelapse_monthlyvideo.log
```

This will run it at 4:05 am first day of every month and create 2 videos:

* One with all the images kept from the days in the month (by default 144 image per day) resulting in 6 seconds per day, so overall a 3 minute video per month
* Second one with 2 seconds each day taken at midday (10am to 2pm with default values) resulting in a 1 minute video per month with (hopefully) more or less uniform lights (no flashing between nights and days)

## TODO and improvements

* Store the snapshots in JPG instead of PNG to save storage. VLC should be capable of doing that, but couldn't figure out the configuration yet
