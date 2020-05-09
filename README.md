# Time-lapse with a Raspberry Pi and a TP-Link Tapo C200 IP-Camera

This is my setup to take time-lapse videos from my balcony with a Raspberry Pi using a TP-Link Tapo C200 IP-Camera.

[![Time-lapse](https://yt-embed.herokuapp.com/embed?v=Gn30s9ypFZ0)](https://www.youtube.com/watch?v=Gn30s9ypFZ0 "Time-lapse")

## High level overview

The TP-Link Tapo C200 provides an rtsp feed for its video. Once a username and password is set in the app, it is available on: [rtsp://user:pass@192.168.a.b:554/stream1](rtsp://user:pass@192.168.a.b:554/stream1) (Use VLC to see if it works.)

My Raspberry Pi takes a snapshot from that video feed at a configurable interval. This would be possible with `ffmpeg`, however I found that due to rtsp using UDP by default, the end result was often corrupted. Thus my script uses the vlc library for python, which starts VLC in the background, waits for 10 seconds for the stream to get stable and then starts capturing snapshots. The script only runs for a short period of time (e.g. 10 minutes), and then it is restarted by cron to limit the issues around the camera dropping connectivity or rebooting.

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
7. If it looks good, at that to crontab as well: `crontab -e`

```

```
