import subprocess
import json
import requests


class Seminar2:
    def exercise_1(self):
        # output a video that will show the macroblocks and the motion vectors
        # first we cut the whole video
        subprocess.call(['ffmpeg', '-ss', '00:00:00.0', '-i', 'BBB.mp4', '-c', 'copy', '-t', '00:00:12.0', 'BBB_12s.mp4'])
        subprocess.call(
            ['ffmpeg', '-flags2', '+export_mvs', '-i', 'BBB_12s.mp4', '-vf', 'codecview=mv=pf+bf+bb', 'output.mp4'])

    def exercise_2(self):
        # You’re going to create a script in order to create a new BBB container
        # ·Cut BBB into 1 minute only video
        # ·Export BBB(1min) audio as MP3 stereo track.
        # ·Export BBB(1min) audio in AAC w/ lower bitrate
        # cut video (1min)
        subprocess.call(
            ['ffmpeg', '-ss', '00:00:00.0', '-i', 'BBB.mp4', '-c', 'copy', '-t', '00:01:00.0', 'BBB_1min.mp4'])
        # mp3 stereo track
        subprocess.call(
            ['ffmpeg', '-i', 'BBB_1min.mp4', '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', 'output_ex2.mp3'])
        # aac bitrate: 64k
        subprocess.call(
            ['ffmpeg', '-i', 'output_ex2.mp3', '-c:a', 'libfdk_aac', '-b:a', '64k', 'output_ex2.mp4'])

    def exercise_3(self):
        # Create a script which reads the tracks from an MP4 container and it is able to say which Broadcasting
        # Standard fits
        with open('file.json', 'w+') as f:
            subprocess.run(
                ['ffprobe', '-v', 'quiet', '-of', 'json', '-show_format', '-show_streams', 'output_ex2.mp4'], stdout=f)
            f.close()

        with open('file.json') as f:
            # data = f.read()
            data_json = json.load(f)
            d1 = data_json['streams'][0]['codec_name']  # we need the codec_name
            d2 = data_json['format']['format_name']  # we need the format_name
            found_broadcast = False
            # DVB-T
            if (d1 == "aac" or d1 == "ac3" or d1 == "mp3") and ("mp4" in d2 or "h264" in d2):
                found_broadcast = True
                print("DVB-T is a possible broadcasting standard")
            # ATSC
            if d1 == "ac3" and ("mp4" in d2 or "h264" in d2):
                found_broadcast = True
                print("ATSC is a possible broadcasting standard")
            # ISDB-T
            if d1 == "aac" and ("mp4" in d2 or "h264" in d2):
                found_broadcast = True
                print("ISDB-T is a possible broadcasting standard")
            # DTMB
            if (d1 == "dra" or d1 == "aac" or d1 == "ac3" or d1 == "mp2" or d1 == "mp3") and ("mp4" in d2 or "h264" in d2 or "avs" in d2 or "avs+" in d2):
                found_broadcast = True
                print("DTMB is a possible broadcasting standard")
            # if we have not found any broadcasting standard that fits:
            if not found_broadcast:
                print("Error, this container does not fit any broadcasting standard")

    def exercise_4(self):
        # Create a script which will download subtitles, integrate them and output a video with printed subtitles
        link = "https://dl.opensubtitles.org/es/download/file/59342"  # link of subtitles of another video
        subtitles = requests.get(link)  # library requests for getting the info of the file
        with open("subtitles.srt", "w") as sub_file:
            sub_file.write(subtitles.text)  # subtitles.srt has the subtitles
        subprocess.call(
            ['ffmpeg', '-i', 'BBB_12s.mp4', '-vf', 'subtitles=subtitles.srt', 'BBB_subtitles.mp4'])


# calling functions
def questions():
    question = input("Would you like to run any other exercise (y/n)? ")
    if question == 'y':
        ex = input("Which exercise do you want to run? ")
        print("You entered:" + ex)
        ex = int(ex)
        c = 1
    else:
        c = 0
        ex = 0
    return ex, c


seminar2 = Seminar2()

exercise_number = input("Which exercise do you want to run? ")
print("You entered:" + exercise_number)
exercise_number = int(exercise_number)
count = 1

while count != 0:
    if exercise_number == 1:
        seminar2.exercise_1()
        exercise_number, count = questions()
    elif exercise_number == 2:
        seminar2.exercise_2()
        exercise_number, count = questions()
    elif exercise_number == 3:
        seminar2.exercise_3()
        exercise_number, count = questions()
    elif exercise_number == 4:
        seminar2.exercise_4()
        exercise_number, count = questions()
    else:
        print("This number is not valid, try again")
        exercise_number = input("Which exercise do you want to run? ")
        print("You entered:" + exercise_number)
        exercise_number = int(exercise_number)


