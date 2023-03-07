# Soundclound_Shazam

The idea is to provide a mix of soundcloud or wherever with mp3 format then the script is splitting it in 3 minutes segments.

Then it shazam each segment to write the song name in res.txt.

## Requirements 

On Linux

```sh
sudo apt install ffmpeg 

pip install ShazamApi
pip install pydub

python shazam.py <audio_file>
```

