from ShazamAPI import Shazam
from pydub import AudioSegment
import os
import sys
import asyncio
from shazamio import Shazam
from pytube import YouTube

# Define the length of each segment in milliseconds
SEGMENT_LENGHT = 60 * 1000


def remove_files(dir):
    files = os.listdir(dir)
    for file in files:
        os.remove(f"{dir}/{file}")


def write_to_file(data):
    with open('song_names.txt', "a", encoding="utf-8") as f:
        f.write(data.encode('utf-8').decode('utf-8'))


# function to open song_names.txt and clean ducplicates
def clean_song_names():
    with open('song_names.txt', "r", encoding="utf-8") as f:
        # Skip the first 2 lines
        next(f)
        next(f)
        # Read the rest of the file
        lines = f.readlines()

    # Create a set to track unique song names and a list to store unique, ordered lines
    seen = set()
    unique_lines = []

    for line in lines:
        # Extract the song name part after the first " - "
        song_name = line.split(' - ', 1)[1]
        if song_name not in seen:
            unique_lines.append(line)
            seen.add(song_name)

    # Sort the lines based on the leading number
    unique_lines.sort(key=lambda x: int(x.split(' - ')[0]))

    with open('song_names_clean.txt', "w", encoding="utf-8") as f:
        f.writelines(unique_lines)


def segment_audio(audio_file):
    # Load the audio file (mp3 format)
    audio = AudioSegment.from_file(audio_file, format="mp3")

    # Split the audio into segments of length segment_length
    segments = [audio[i:i+SEGMENT_LENGHT]
                for i in range(0, len(audio), SEGMENT_LENGHT)]
    # Save each segment as a separate file
    for i, segment in enumerate(segments):
        segment.export(
            f"export/{i+1}.mp3", format="mp3")


def get_song_name(audio_file):
    mp3_file_content_to_recognize = open(audio_file, 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()

    for i in range(20):
        sound_data_tuple = next(recognize_generator)
        if 'track' in sound_data_tuple[1]:
            sound_data_dict = sound_data_tuple[1]
            name = sound_data_dict['track']['title'] + \
                " - " + sound_data_dict['track']['subtitle']
            return name

    return "Not found"


def download_youtube(url, output_path='Downloads'):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()

    # download the file
    out_file = video.download(output_path=output_path)

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    # result of success
    print(yt.title + " has been successfully downloaded.")


async def get_name(file):
    shazam = Shazam()
    data = await shazam.recognize(file)
    if 'track' not in data:
        return "Not found"

    title = data['track']['title']
    subtitle = data['track']['subtitle']
    print(f"{title} - {subtitle}")
    return f"{title} - {subtitle}"

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide an audio file")
        print("Usage: python shazam.py <audio_file>")
        exit()

    # download_youtube(sys.argv[1])
    print("Starting...")

    print("Removing files...")
    remove_files("export")

    # get the audio file from the user input
    audio_file = sys.argv[1]

    with open('song_names.txt', "w", encoding="utf-8") as f:
        f.write(f"Initial File: {audio_file}\n\n")

    print("Segmenting audio file...")
    segment_audio(audio_file)

    print("Getting song names...")
    files = os.listdir("export")
    for file in files:
        loop = asyncio.get_event_loop()
        name = loop.run_until_complete(get_name(f"export/{file}"))
        # write_to_file(data=f"{name}\n")
        write_to_file(data=f"{file.replace('.mp3', '')} - {name}\n")

    print("Cleaning up...")
    clean_song_names()
    remove_files("export")

    print("Done!")
