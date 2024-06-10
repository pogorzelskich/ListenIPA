from audio_reformatting import SR, N_FFT

CRITERIA_NAMES = [["Thinking", "thi", 2],
                  ["Space", "spa", 2],
                  ["Long", "lon", 2],
                  ["Stress", "str", 2],
                  ["Consonant (Open, Close, Approximant, Non-sibilant fricative)", "con", 9],
                  ["Nasal", "nas", 2],
                  ["Plosive", "plo", 2],
                  ["Sibilant fricative", "sib", 2],
                  ["Trill", "tri", 2],
                  ["Lateral", "lat", 2],
                  ["Labialization, Rounded", "lbz", 3],
                  ["Bilabial", "bil", 2],
                  ["Dental", "den", 2],
                  ["Alveolar", "alv", 2],
                  ["Retroflex, Rhotic", "ret", 2],
                  ["Palatal, Front", "pal", 2],
                  ["Velar, Back", "vel", 2],
                  ["Uvular", "uvu", 2],
                  ["Pharyngeal/epiglottal", "pha", 2],
                  ["Glottal", "glo", 2],
                  ["Aspiration", "asp", 2],
                  ["Voiceless", "vls", 2]
                  ]
CRITERIA_TAGS_ID = {i[1]: n for n, i in enumerate(CRITERIA_NAMES)}
CRITERIA_LEN = len(CRITERIA_NAMES)

COMBINATION_CRITERIA_NAMES = [["Tap/flap", "tap", 2],
                              ["Labiodental", "lad", 2],
                              ["Postalveolar", "plv", 2]
                              ]
COMBINATION_CRITERIA_TAGS_ID = {i[1]: n for n, i in enumerate(COMBINATION_CRITERIA_NAMES)}
COMBINATION_CRITERIA_LEN = len(COMBINATION_CRITERIA_NAMES)

import numpy as np
import torch
from torch.utils.data import Dataset
import librosa
# import soundfile as sf

# Common sounds collection for classifying
class SoundClassifying:
    def __init__(self):
        with open('data/ipa_symbols.txt', 'r', encoding="utf8") as f:
            self.symbols_table = {i[0]: [float(j) for j in i[1:]] for i in [i[:-1].split("\t") for i in f.readlines()]}
        with open('data/ipa_mods.txt', 'r', encoding="utf8") as f:
            self.mods_table = {i[0]: [j for j in i[1:]] for i in [i[:-1].split("\t") for i in f.readlines()]}
    def symbol_info(self, sym): return self.symbols_table[sym].copy()
    def mod_info(self, sym): return self.mods_table[sym].copy()
    def empty(self): return [0.0 for i in CRITERIA_NAMES]

# Creating all combinantions
def combs(a):
    if len(a) == 0:
        return [[]]
    cs = []
    for c in combs(a[1:]):
        cs += [c, c+[a[0]]]
    return cs

# Diversifying notation with including and excluding values in brackets
def brackets_split(notation):
    notation_split = [i.split(")") for i in notation.split("(")]
    if len(notation_split) != 1:
        notation_start = notation_split[0][0]
        notation_split = notation_split[1:]
        notation_combs = combs(range(len(notation_split)))
        notation_split_vars = []
        for c_list in notation_combs:
            new_notation_var = notation_start
            for n, section in enumerate(notation_split):
                if n in c_list:
                    new_notation_var += section[0]
                new_notation_var += section[1]
            notation_split_vars.append(new_notation_var)
    else:
        notation_split_vars = notation_split[0]
    return notation_split_vars

# Main classification function
def classify(notation_stage_1:str, classifying:SoundClassifying, amplify:float=1.0, reverse:bool=False, bias:float=0.0):
    vowels = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø",
              "ɘ", "ɵ", "ɤ", "o", "ə", "ɚ", "ɛ", "œ", "ɜ", "ɝ", "ɞ",
              "ʌ", "ɔ", "æ", "ɐ", "a", "ɶ", "ä", "ɑ", "ɒ", "̩"]
    curr_weight = 1.0
    sound_symbols = classifying.symbols_table.keys()
    sound_mods = classifying.mods_table.keys()

    # Initial notation
    notation_stage_2 = []
    for char in notation_stage_1:
        if char == " ":
            curr_classifying = classifying.empty()
            curr_classifying[CRITERIA_TAGS_ID["spa"]] = 1.0
            curr_classifying[CRITERIA_TAGS_ID["lon"]] = 0.0
            notation_stage_2.append([["_", char, "l"], curr_weight, curr_classifying])
        elif char == "|":
            curr_classifying = classifying.empty()
            curr_classifying[CRITERIA_TAGS_ID["spa"]] = 1.0
            curr_classifying[CRITERIA_TAGS_ID["lon"]] = 1.0
            notation_stage_2.append([["_", char, "l"], curr_weight, curr_classifying])
        elif char == "‿":
            curr_classifying = classifying.empty()
            curr_classifying[CRITERIA_TAGS_ID["spa"]] = 1.0
            curr_classifying[CRITERIA_TAGS_ID["lon"]] = 0.0
            notation_stage_2.append([["_", char, "s"], curr_weight, curr_classifying])
        elif char in sound_symbols:
            if char in vowels:
                notation_stage_2.append([["s", char, "v"], curr_weight, classifying.symbol_info(char)])
            else:
                notation_stage_2.append([["s", char, "c"], curr_weight, classifying.symbol_info(char)])
        elif "◌"+char in sound_mods:
                notation_stage_2.append([["m", char, "←"], curr_weight, classifying.mod_info("◌"+char)])
        elif char in sound_mods:
            notation_stage_2.append([["m", char, "→"], curr_weight, classifying.mod_info(char)])
    notation_stage_3 = []
    for sound in notation_stage_2:
        if sound[0][0] == "m":
            if sound[0][2] == "←":
                last_sound = notation_stage_3[-1].copy()
                last_sound[0] = last_sound[0].copy()
                last_sound[2] = last_sound[2].copy()
                for cat, val in enumerate(sound[2]):
                    if val == "":
                        last_sound[0][1] = notation_stage_3[-1][0][1] + sound[0][1]
                    elif val[0] == "-":
                        last_sound[0][1] = notation_stage_3[-1][0][1] + sound[0][1]
                        last_sound[2][cat] = notation_stage_3[-1][2][cat] - float(val[1:])
                        if last_sound[2][cat] < 0: last_sound[2][cat] = 0
                    elif val[0] == "+":
                        last_sound[0][1] = notation_stage_3[-1][0][1] + sound[0][1]
                        last_sound[2][cat] = notation_stage_3[-1][2][cat] + float(val[1:])
                        if last_sound[2][cat] > 1: last_sound[2][cat] = 1
                    elif val[:3] == "to ":
                        last_sound[0][1] = notation_stage_3[-1][0][1] + sound[0][1]
                        last_sound[2][cat] = (notation_stage_3[-1][2][cat] + float(val[3:])) / 2
                    elif val[:3] == "up ":
                        last_sound[0][1] = notation_stage_3[-1][0][1] + sound[0][1]

                        curr_val = notation_stage_3[-1][2][cat]
                        new_val = float(val[3:])
                        if curr_val < new_val:
                            last_sound[2][cat] = new_val
                    else:
                        last_sound[0][1] = notation_stage_3[-1][0][1] + sound[0][1]
                        last_sound[2][cat] = float(val)
                notation_stage_3[-1] = last_sound
            else:
                notation_stage_3.append(sound)
        else:
            notation_stage_3.append(sound)
    
    # Adding mods
    notation_stage_4 = []
    for sound in notation_stage_3[::-1]:
        if sound[0][0] == "m":
            if sound[0][2] == "→":
                for n in range(len(notation_stage_4)):
                    n_rev = len(notation_stage_4) - n - 1
                    if notation_stage_4[n_rev][0][0] != "s" or "̯" in notation_stage_4[n_rev][0][1]:
                        pass
                    elif "̩" in notation_stage_4[n_rev][0][1] or \
                    notation_stage_4[n_rev][2][CRITERIA_TAGS_ID["con"]] < 0.8125:
                        notation_stage_4[n_rev][0][1] = sound[0][1] + notation_stage_4[n_rev][0][1]
                        for s in range(len(sound[2])):
                            if sound[2][s] != "":
                                notation_stage_4[n_rev][2][s] += float(sound[2][s]) * sound[1]
                        break
            else:
                notation_stage_4.append(sound)
        else:
            notation_stage_4.append(sound)
    
    notation_stage_4 = notation_stage_4[::-1]
    
    # Stress (strtucture of words)
    structure = ""
    for sound in notation_stage_4:
        if sound[0][0] == "_" and sound[2][CRITERIA_TAGS_ID["lon"]] > 0.375:
            structure += "_"
        elif sound[0][0] == "_":
            structure += "-"
        elif sound[0][0] == "s":
            if (sound[0][2] == "v" or "̩" in sound[0][1]) and "̯" not in sound[0][1]:
                if sound[2][CRITERIA_TAGS_ID["str"]] > 0:
                    structure += "V"
                else:
                    structure += "v"
            elif (sound[0][2] == "c" or "̯" in sound[0][1]) and "̩" not in sound[0][1]:
                structure += "c"
        else:
            structure += "o"
        
    # Stress (stressing needed sounds)
    structure_check = [[0]*len(i)+["_"] if "v" in i and i.count("v") == 1 and i.count("V") == 0
                       else [1]*len(i)+["_"] for i in structure.split("_")]
    structure_list = []
    for i in structure_check:
        structure_list += i
    structure_list = structure_list[:-1]

    stressed = False
    for n, struc in enumerate(structure_list):
        if struc == 0 and not stressed:
            if structure[n] == "v":
                notation_stage_4[n][2][CRITERIA_TAGS_ID["str"]] = 1.0
                stressed = True
        elif struc == "_":
            stressed = False
    
    # Long sounds
    if len(notation_stage_4) != 0:
        notation_stage_5 = [notation_stage_4[0].copy()]
    else:
        notation_stage_5 = []
    for n in range(1, len(notation_stage_4)):
        sound1 = notation_stage_4[n][2].copy()
        sound2 = notation_stage_5[-1][2].copy()
        sound1[CRITERIA_TAGS_ID["lon"]] = 0.0
        sound2[CRITERIA_TAGS_ID["lon"]] = 0.0
        stress1 = sum([i in notation_stage_4[n][0][1] for i in "ˌˈ"]) == 0
        stress2 = sum([i in notation_stage_5[-1][0][1] for i in "ˌˈ"]) == 0
        cv1 = "̩" in notation_stage_4[n][0][1]
        cv2 = "̩" in notation_stage_5[-1][0][1]
        vc1 = "̯" in notation_stage_4[n][0][1]
        vc2 = "̯" in notation_stage_5[-1][0][1]
        if sound1 == sound2 and (stress1 and stress2) and cv1 == cv2 and vc1 == vc2:
            notation_stage_5[-1][0][1] += notation_stage_4[n][0][1]
            notation_stage_5[-1][2][CRITERIA_TAGS_ID["lon"]] = 1.0
        else:
            notation_stage_5.append(notation_stage_4[n])
    
    # Removing spaces from in the beginning and in the end
    notation_stage_6 = []
    no_longer_spaces = False
    for sound in notation_stage_5:
        if sound[2][CRITERIA_TAGS_ID["spa"]] != 1.0:
            no_longer_spaces = True
        if no_longer_spaces:
            notation_stage_6.append(sound)
    notation_stage_7 = []
    no_longer_spaces = False
    for sound in notation_stage_6[::-1]:
        if sound[2][CRITERIA_TAGS_ID["spa"]] != 1.0:
            no_longer_spaces = True
        if no_longer_spaces:
            notation_stage_7.append(sound)
    notation_stage_7 = notation_stage_7[::-1]

    # Multiplying and reversing
    notation_stage_amp = []
    for sound in notation_stage_7:
        if reverse:
            for cat in range(len(sound[2])):
                sound[2][cat] = amplify - (amplify * sound[2][cat]) + bias
        else:
            for cat in range(len(sound[2])):
                sound[2][cat] = amplify * sound[2][cat] + bias
        notation_stage_amp.append(sound)

    return notation_stage_amp

# Dataset collect
class ListenIPADataset(Dataset):
    def __init__(self, notations:list, amplify:float=1.0, reverse:bool=False, bias:float=0.0):
        self.classifying = SoundClassifying()
        self.amplify = amplify
        self.reverse = reverse
        self.bias = bias
        self.pairs = notations
    
    def append(self, pair):
        self.pairs.append(pair)
    
    def pop(self, index:int=-1):
        self.pairs.pop(index)
    
    def criteria_max(self):
        return self.bias if self.reverse else self.amplify+self.bias
    
    def criteria_min(self):
        return self.amplify+self.bias if self.reverse else self.bias
    
    def thinking_empty(self):
        if self.reverse:
            returning_array = [self.bias] + [self.amplify + self.bias for i in CRITERIA_NAMES[1:]]
        else:
            returning_array = [self.amplify + self.bias] + [self.bias for i in CRITERIA_NAMES[1:]]

        return tuple(returning_array)
    
    def output_audio_npy(self, index:int):
        return np.load(f'data/audio_data_stft/{self.pairs[index][0]}.npy')
    
    def output_audio_mp3(self, index:int, curr_sr:int=SR):
        return librosa.load(f'data/audio_data/{self.pairs[index][0]}.mp3', sr=curr_sr)
        # y, sr = librosa.load(self.pairs[index][0], sr=curr_sr)

    def output_labels(self, index:int, is_shortened=True):
        curr_weights = [brackets_split(i[1:-1].strip()) for ipa_id, i in self.pairs[index][1]]
        t = []
        if is_shortened:
            for weight in curr_weights:
                for variant in [[i2[2] for i2 in classify(i1, self.classifying, self.amplify, self.reverse, self.bias)] for i1 in weight]:
                    t.append(tuple([tuple(k) for k in variant]))
        else:
            for weight in curr_weights:
                for variant in [[i2 for i2 in classify(i1, self.classifying, self.amplify, self.reverse, self.bias)] for i1 in weight]:
                    t.append(tuple([(tuple(k[0]), k[1], tuple(k[2])) for k in variant]))
        return tuple(set(t))

    def output_audio_id(self, index:int):
        return self.pairs[index][0]
    
    def output_labels_text(self, index:int):
        return self.pairs[index][1]
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, index:int):
        return {"audio": self.output_audio_npy(index), "labels": self.output_labels(index),
                "audio_id": self.output_audio_id(index), "labels_text": self.output_labels_text(index)}
