import time
import vlc
import datetime
import os
import timelapseconfig

#prepare VLC
i = vlc.Instance("--vout=dummy") # when running from cron, there is no screen attached
camera = i.media_player_new()
camera.set_mrl(timelapseconfig.rtsp_url)
camera.audio_set_volume(0)
camera.play()

# prepare the output folder
write_path = timelapseconfig.output_dir + datetime.datetime.today().strftime(timelapseconfig.daily_foldername_date_formatstring)
if not os.path.exists(write_path):
    os.makedirs(write_path)

print ('waiting for VLC')
time.sleep(10)
print ("staring capture")
starttime = datetime.datetime.now().timestamp()
while datetime.datetime.now().timestamp() < starttime + timelapseconfig.cronjob_repeat_time:
    cycle_starttime = datetime.datetime.now().timestamp()
    file_name = write_path + "/" + str(int(datetime.datetime.now().timestamp())) + ".png"
    print(file_name)
    camera.video_take_snapshot(0,file_name,1920,1080)
    while datetime.datetime.now().timestamp() < cycle_starttime + timelapseconfig.delay_between_images:
        time.sleep(0.1)
