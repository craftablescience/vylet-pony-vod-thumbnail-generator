import os
import webvtt
from common import DATA


if __name__ == "__main__":
    search = input("enter word or phrase: ")

    for stream in [stream for stream in DATA["streams"].keys() if DATA["streams"][stream]["subs"]]:
        path = f"../assets/subs/{stream}.en.vtt"
        if os.path.exists(path):
            for sentence in webvtt.read(path):
                if search in sentence.text:
                    print(stream, sentence.start_time, sentence.text)
