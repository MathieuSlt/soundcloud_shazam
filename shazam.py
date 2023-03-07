from ShazamAPI import Shazam
from pydub import AudioSegment
import os
import sys


def remove_file(dir):
    files = os.listdir(dir)
    for file in files:
        os.remove(f"{dir}/{file}")


def write_to_file(data):
    with open('res.txt', "a") as f:
        f.write(data)


# Split the audio file into segments
def segment_audio(audio_file):
    # Load the audio file (mp3 format)
    audio = AudioSegment.from_file(audio_file, format="mp3")
    # Define the length of each segment in milliseconds
    segment_length = 120 * 1000
    # Split the audio into segments of length segment_length
    segments = [audio[i:i+segment_length]
                for i in range(0, len(audio), segment_length)]
    # Save each segment as a separate file
    for i, segment in enumerate(segments):
        segment.export(
            f"export/{audio_file[:-4]}_segment{i+1}.mp3", format="mp3")


def get_song_name(audio_file):
    mp3_file_content_to_recognize = open(audio_file, 'rb').read()

    shazam = Shazam(
        mp3_file_content_to_recognize
    )

    recognize_generator = shazam.recognizeSong()
    sound_data_tuple = next(recognize_generator)
    if sound_data_tuple[0] == 8.0:
        return "Not found"
    sound_data_dict = sound_data_tuple[1]
    name = sound_data_dict['track']['title'] + \
        " - " + sound_data_dict['track']['subtitle']
    return name


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Please provide an audio file")
        print("Usage: python shazam.py <audio_file>")
        exit()

    print("Starting...")

    print("Removing files...")
    remove_file("export")

    # get the audio file from the user input
    audio_file = sys.argv[1]

    # audio_file = "Nightmare Prelude.mp3"

    with open('res.txt', "w") as f:
        f.write(f"Initial File: {audio_file}\n\n")

    print("Segmenting audio file...")
    segment_audio(audio_file)

    print("Getting song names...")
    files = os.listdir("export")
    for file in files:
        name = get_song_name(f"export/{file}")
        write_to_file(data=f"{name}\n")

    print("Done!")
