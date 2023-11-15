import os
import simpleaudio
import argparse
from nltk.corpus import cmudict
import re

#import numpy
#import datetime
#...others?

### NOTE: DO NOT CHANGE ANY OF THE EXISTING ARGUMENTS
parser = argparse.ArgumentParser(
    description='A basic text-to-speech app that synthesises an input phrase using diphone unit selection.')
parser.add_argument('--diphones', default="./diphones", help="Folder containing diphone wavs")
parser.add_argument('--play', '-p', action="store_true", default=False, help="Play the output audio")
parser.add_argument('--outfile', '-o', action="store", dest="outfile", type=str, help="Save the output audio to a file",
                    default=None)
parser.add_argument('phrase', nargs=1, help="The phrase to be synthesised")

# Arguments for extensions
parser.add_argument('--spell', '-s', action="store_true", default=False,
                    help="Spell the phrase instead of pronouncing it")
parser.add_argument('--crossfade', '-c', action="store_true", default=False,
					help="Enable slightly smoother concatenation by cross-fading between diphone units")
parser.add_argument('--volume', '-v', default=None, type=int,
                    help="An int between 0 and 100 representing the desired volume")

args = parser.parse_args()

print(args.diphones)


class Synth:
    def __init__(self, wav_folder):
        self.diphones = {}
        self.get_wavs(wav_folder)

    def get_wavs(self, wav_folder):
        for root, dirs, files in os.walk(wav_folder, topdown=False):
            for file in files:
                pass  # delete this line and implement

class Utterance:
    def __init__(self, phrase):
        print(phrase)
        pass # delete this and implement

    def get_phone_seq(self):
        pass  # delete this line and implement


if __name__ == "__main__":
    utt = Utterance(args.phrase[0])
    phone_seq = utt.get_phone_seq()

    diphone_synth = Synth(wav_folder=args.diphones)

    # out is the Audio object which will become your output
    # you need to modify out.data to produce the correct synthesis
    out = simpleaudio.Audio(rate=16000)
    print(out.data, type(out.data))


