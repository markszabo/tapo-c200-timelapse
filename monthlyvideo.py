from datetime import datetime, timedelta
import os

import timelapseconfig

lastmonth = (datetime.now() - timedelta(15)).strftime(timelapseconfig.monthly_filename_date_formatstring)
output_fulldays_video_path = timelapseconfig.output_dir_for_monthly_timelapse_videos + lastmonth + "_fulldays.mp4"
output_short_video_path = timelapseconfig.output_dir_for_monthly_timelapse_videos + lastmonth + "_short.mp4"

os.chdir(timelapseconfig.output_dir)

# ffmpeg -r 24 -pattern_type glob -i '2020-05-*/*.png' -s hd1080 -vcodec libx264 out05.mp4
cmd = "ffmpeg -r 24 -pattern_type glob -i '" + lastmonth + "*/*.png' -s hd1080 -vcodec libx264 '" + output_fulldays_video_path + "'"
print("Running command: " + cmd)
returnval = os.system(cmd)
print("Command returned: " + str(returnval))

concat_demuxer_input_file = timelapseconfig.output_dir + "concat_demuxer_input.txt"

f = open(concat_demuxer_input_file, "w")

img_file_path = ""

output_dir_content = os.listdir(timelapseconfig.output_dir)
output_dir_content.sort()

for dir in output_dir_content:
    if os.path.isdir(timelapseconfig.output_dir + dir) and dir.startswith(lastmonth):
        images = os.listdir(timelapseconfig.output_dir + dir)
        images.sort()
        for img in images[60:85]: #10am to 2pm with the default values (1 picture per 10 minutes)
            img_file_path = timelapseconfig.output_dir + dir + os.path.sep + img
            f.write("file '" + img_file_path + "'\nduration 0.04\n")

f.write("file '" + img_file_path + "'\n") # the last image has to be specified twice, see https://trac.ffmpeg.org/wiki/Slideshow#Concatdemuxer
f.close()

# ffmpeg -f concat -i input.txt -vsync vfr -pix_fmt yuv420p output.mp4
cmd = "ffmpeg -f concat -safe 0 -i '" + concat_demuxer_input_file + "' -vsync vfr -pix_fmt yuv420p '" + output_short_video_path + "'"
print("Running command: " + cmd)
returnval = os.system(cmd)
print("Command returned: " + str(returnval))
