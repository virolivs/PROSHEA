import os
import subprocess
from configparser import ConfigParser
import time

totalstart = time.time()

Config_file = ConfigParser()

Config_file.read("Dav_To_JPEG/DavtoJPEG-config.conf")

DAV_INPUT = Config_file.get("DAVtoJPEG", "dav_inputpath")
JPEG_OUTPUT = Config_file.get("DAVtoJPEG", "jpeg_outputpath")
FFMPEG = Config_file.get("DAVtoJPEG", "FFMPEG_dir")

def extractFramesFromDav(davPath, jpegOutput):
    start = time.time()

    # FFmpeg command to extract JPEG images
    command = [FFMPEG, '-i', davPath, '-r', '1', '-s', '1920x1080', '-f', 'image2', jpegOutput]
    subprocess.run(command)

    end = time.time()
    print(f"Time taken in minutes: {(end-start)/60}")

if __name__ == "__main__":
    print("------Listing DAV files------")
    listdavfiles = os.listdir(DAV_INPUT)
    DAVfilesonly = [davfiles for davfiles in listdavfiles if davfiles.endswith('.dav')]

    print("------Extracting frames from DAV videos to JPEG images------")

    for i, DAVinput in enumerate(DAVfilesonly):
        DAV_Videoinput = os.path.join(DAV_INPUT, DAVinput)
        output_folder = os.path.join(JPEG_OUTPUT, os.path.splitext(DAVinput)[0])

        # Check if the output folder already exists, if not, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        JPEGoutput = os.path.join(output_folder, f"frame_%03d.jpeg")

        print(f"Processing: {i+1} file")

        extractFramesFromDav(DAV_Videoinput, JPEGoutput)

    totalend = time.time()
    print("------JPEG image extraction completed------")
    print(f"Total time taken in minutes: {(totalend - totalstart)/60}")
