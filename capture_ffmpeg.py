import time
import ffmpeg
import datetime
import os
import sys
import timelapseconfig


# prepare the output folder
write_path = timelapseconfig.output_dir + datetime.datetime.today().strftime(timelapseconfig.daily_foldername_date_formatstring)
if not os.path.exists(write_path):
    os.makedirs(write_path)

print ("staring capture")
starttime = datetime.datetime.now().timestamp()
while datetime.datetime.now().timestamp() < starttime + timelapseconfig.cronjob_repeat_time:
    cycle_starttime = datetime.datetime.now().timestamp()
    file_name = write_path + "/" + str(int(datetime.datetime.now().timestamp())) + ".png"
    print(file_name)
    try:
        (
                ffmpeg.input(timelapseconfig.rtsp_url, ss="00:00:03").output(file_name, vframes=1).overwrite_output().run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)

    while datetime.datetime.now().timestamp() < cycle_starttime + timelapseconfig.delay_between_images:
        time.sleep(0.1)
