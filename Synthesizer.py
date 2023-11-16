import os
import simpleaudio
import argparse
import nltk
from nltk.corpus import cmudict
import re
import numpy as np

'''
Speech Synthesiser Programme
Author: Kexin GAO
-----------------------------------INSTRUCTION--------------------------------------
This is a speech synthesiser programme which can read the input text.
You can either play the output, or save the output, or, for sure, do them both.
You can set the volume from 1 to 100.
Date from 1900 to 1999 (DD/MM, DD/MM/YY, DD/MM/YYYY) in the text can be read.
Have fun!
------------------------------------------------------------------------------------
'''

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

    '''
    THE FRONT-END OF THE SYNTHESIZER
    Extract the wav files by mapping file names and the files in the diphones folder.
    Load the extracted wav files, concatenate the file data.
    Output the concatenated file, set the volume, play it, save it.
    '''

    def __init__(self, diphone_list, wav_folder):
        self.diphones = {}
        self.wav_folder = wav_folder
        self.diphone_list = diphone_list
        self.output = self.get_wavs()

    def get_wavs(self):
        # Concatenate the diphone files into a complete wav file
        # Output the concatenated wav file
        for root, dirs, files in os.walk(self.wav_folder, topdown=False):
            for file in files:
                self.diphones[file] = os.path.join(root, file)
        array_list = []
        if len(self.diphone_list) == 0:
            pass
        else:
            for item in self.diphone_list:
                try:
                    self.output = simpleaudio.Audio()
                    self.output.load(self.diphones[item])
                    array_list.append(self.output.data)
                except Exception as exp:
                    pass
                    # print("Error: {} is missing...".format(exp))
            self.output.data = np.array([items for sublist in array_list for items in sublist])
            return self.output

    def set_volume(self, volume):
        # Set the volume of the output
        if len(self.diphone_list) == 0:
            pass
        else:
            if not 0 <= volume <= 100:
                raise ValueError("Expected scaling factor between 0 and 100")
            self.output.rescale(volume/100)

    def save_output(self):
        # Save the output to the default directory with a file name
        if len(self.diphone_list) == 0:
            print("Unable to save, please check your input")
        else:
            self.output.save(args.outfile)

    def play_output(self):
        # Play the output file
        if len(self.diphone_list) == 0:
            print("Unable to play, please check your input")
        else:
            self.output.play()


class Utterance:

    '''
    THE BACK-END OF THE SYNTHESIZER
    Split the input phrase into words, and then parse the words into phones.
    Combine phones into diphones, and then format them as the filename "xx-xx.wav".
    Output the list of formatted file name strings.
    '''

    def __init__(self, phrase):
        self.phrase = phrase
        self.normalized_phrase = []
        self.phone_list = []
        self.normalized_phone = []
        self.diphone_list = []
        self.file_list = []

        print(phrase)

    def date_to_text(self):
        # If the input phrase contains a date(DD/MM, DD/MM/YY, DD/MM/YYYY), parse it into words

        match = re.search(r'[0-9]{1,2}/[0-9]{1,2}/*[0-9]{0,4}', self.phrase)
        # Check whether there is a date content
        if match is not None:
            # If there is a date content, parse it

            date = match.group(0)
            _parts = date.split("/")
            datelist = [int(_part) for _part in _parts]
            if len(datelist) == 2:
                _day = datelist[0]
                _month = datelist[1]
            else:
                _day = datelist[0]
                _month = datelist[1]
                _year = datelist[2]

            ord_num = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth', 7: 'seventh',
                       8: 'eighth', 9: 'ninth', 10: 'tenth', 11: 'eleventh', 12: 'twelfth', 13: 'thirteenth',
                       14: 'fourteenth', 15: 'fifteenth', 16: 'sixteenth', 17: 'seventeenth', 18: 'eighteenth',
                       19: 'nineteenth', 20: 'twentieth', 30: 'thirtieth'}
            int_num = {0: " ", 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
                       6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
                       11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
                       15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
                       19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty',
                       70: 'seventy', 80: 'eighty', 90: 'ninety'}
            mon_dic = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                       7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

            def parse_day(num):
                # Parse the number of the day into English phrase
                # Output the string of the phrase, exp "twenty first"
                if num >=1 and num <= 20:
                    return ord_num[num]
                elif num >= 21 and num <= 31:
                    unit = int(num % 10)
                    dec = int(num / 10) * 10
                    return "{} {}".format(int_num[dec], ord_num[unit])
                else:
                    print("Error: the date is incorrect, please check you input")


            def parse_year(num):
                # Parse the number of the year into English words
                # Output the string of the year
                if num >= 1900 and num <= 1999:
                    # The case that the form of the year is in "YYYY" format
                    first_part = 19
                    sec_part = int(num % 100)
                    if sec_part < 10:
                        return "{} {}".format(int_num[first_part], 'zero {}'.format(int_num[sec_part]))
                    elif sec_part > 20:
                        unit = int(sec_part % 10)
                        dec = int(sec_part / 10) * 10
                        return "{} {} {}".format(int_num[first_part], int_num[dec], int_num[unit])
                    else:
                        return "{} {}".format(int_num[first_part], int_num[num])
                elif num >= 0 and num <= 99:
                    # The case that the form of the year is in "YY" format
                    first_part = 19
                    if num < 10:
                        return "{} {}".format(int_num[first_part], 'zero {}'.format(int_num[num]))
                    elif num > 20:
                        unit = int(num % 10)
                        dec = int(num / 10) * 10
                        return "{} {} {}".format(int_num[first_part], int_num[dec], int_num[unit])
                    else:
                        return "{} {}".format(int_num[first_part], int_num[num])
                else:
                    # Other incorrect format, pass the method
                    pass

            if len(datelist) == 2:
                # The case that the form of the date is in "DD/MM" format
                # Output the string of the complete date
                if _day <= 31 and _month <= 12:
                    output = mon_dic[_month], " ", parse_day(_day)
                    date_text = ''.join(output)
                    self.phrase = re.sub(r'[0-9]{1,2}/[0-9]{1,2}/*[0-9]{0,4}', date_text, self.phrase)
                else: print("Error: the date is incorrect, please check you input")
            else:
                # The case that the form of the date is in "DD/MM/(YY)YY" format
                # Output the string of the complete date
                if _day <= 31 and _month <= 12 and _year >= 1900 and _year <= 1999:
                    # The case that the year is in "YYYY" format
                    output = mon_dic[_month], " ", parse_day(_day), " ", parse_year(_year)
                    date_text = ''.join(output)
                    self.phrase = re.sub(r'[0-9]{1,2}/[0-9]{1,2}/*[0-9]{0,4}', date_text, self.phrase)
                elif _day <= 31 and _month <= 12 and _year >= 0 and _year <= 99:
                    # The case that the year is in "YY" format
                    output = mon_dic[_month], " ", parse_day(_day), " ", parse_year(_year)
                    date_text = ''.join(output)
                    self.phrase = re.sub(r'[0-9]{1,2}/[0-9]{1,2}/*[0-9]{0,4}', date_text, self.phrase)
                else:
                    # Other case, print error message
                    print("Error: the date is incorrect, please check you input")
        else:
            # If there is no date in the content, pass this method
            pass

    def normalize_phrase(self):
        # Lowercase the phrase, remove the punctuations, split it into words
        # Output a list of word strings
        self.phrase = self.phrase.lower()
        self.phrase = re.sub(r'[^\w\s]', '', self.phrase)
        self.normalized_phrase = self.phrase.split()

    def get_phone(self):
        # Get the phones of each word in the phrase
        # Output a list of phone strings
        dict = nltk.corpus.cmudict.dict()
        for word in self.normalized_phrase:
            try:
                self.phone_list.append(dict[word][0])
            except Exception as exp:
                print("Error: {} cannot be played...".format(exp))
        self.phone_list = [items for sublist in self.phone_list for items in sublist]

    def normalize_phone(self):
        # Lowercase the phones, and remove the numbers in them
        # Output a list of lowercased phone strings without numbers in them
        if len(self.phone_list) == 0:
            pass
        else:
            for items in self.phone_list:
                items = items.lower()
                items = re.sub("\d+", "", items)
                self.normalized_phone.append(items)

    def get_diphone(self):
        # Concatenate each two adjacent phones into diphones, and format them into the filename
        # Output a list of filename strings
        if len(self.normalized_phone) == 0:
            pass
        else:
            for i in range(len(self.normalized_phone)-1):
                front_phone = self.normalized_phone[i]
                back_phone = self.normalized_phone[i+1]
                diphone = front_phone + "-" + back_phone + ".wav"
                self.diphone_list.append(diphone)
            self.diphone_list.insert(0, "pau" + "-" + self.normalized_phone[0] + ".wav")
            self.diphone_list.append(self.normalized_phone[i+1] + "-" + "pau" + ".wav")

    def get_phone_seq(self):
        # A main function which runs the previous functions in this class
        # Return the list of filename strings and save them into a temp_list for later use in the class Synth
        self.date_to_text()
        self.normalize_phrase()
        self.get_phone()
        self.normalize_phone()
        self.get_diphone()
        temp_list = self.diphone_list
        return temp_list


if __name__ == "__main__":
    utt = Utterance(args.phrase[0])
    phone_seq = utt.get_phone_seq()

    diphone_synth = Synth(phone_seq, wav_folder=args.diphones)
    if args.volume:
        diphone_synth.set_volume(args.volume)
    if args.play:
        diphone_synth.play_output()
    if args.outfile:
        diphone_synth.save_output()

    # out is the Audio object which will become your output
    # you need to modify out.data to produce the correct synthesis
    out = simpleaudio.Audio(rate=16000)
    out = diphone_synth.get_wavs()
    # print(out.data, type(out.data))
