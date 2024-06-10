import torch
import numpy as np

from criteria_to_symbols import *
from model import *
from listen_ipa_dataset import CRITERIA_LEN
from audio_reformatting import *


torch.set_printoptions(precision=8)
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

kernel_size = 15
num_layers = 4
old_version = True

MODEL = ListenIPA(513, CRITERIA_LEN, kernel_size, num_layers, old_version)

model_path = './model_epoch_3.pth'
MODEL.load_state_dict(torch.load(model_path))
MODEL.eval()

# audio_path = "./zzzzzzz.wav"
def audio_to_ipa(audio_path="./audio.mp3", saving=True, think_value=0.5):
    audio_frames = audio_reformatting(audio_path)
    with torch.no_grad():
        hidden = MODEL.init_hidden()
        outputs = []
        for audio_frame in audio_frames:
            audio_frame = torch.from_numpy(audio_frame).unsqueeze(0).unsqueeze(0)
            output, hidden = MODEL(audio_frame, hidden)
            outputs.append(output.to(DEVICE))
        collected_outputs = [[float(j) for j in i[0][0]] for i in outputs]
        ipa = output_to_symbols(collected_outputs, think_value)
        if saving:
            with open(audio_path+".txt", 'w', encoding="utf8") as f:
                f.write(ipa)
        return ipa

def multiple_audio_to_ipa(audio_paths:list, saving=True, think_value=0.5):
    return [[audio_path, audio_to_ipa(audio_path, saving, think_value)] for audio_path in audio_paths]

def save_all(ipas:list, folder_path:str):
    with open(folder_path+"!all_files.txt", 'w', encoding="utf8") as f:
        for ipa in ipas:
            f.write(f"{ipa[0]}\t{ipa[1]}\n")

SUPPORTED_FILES = [".mp3", ".ogg", ".wav", ".flac", ".m4a"]
def folder_audio_to_ipa(folder_path:str, saving=True, think_value=0.5):
    import os
    folder_path = folder_path.replace("\\", "/")
    folder_path = folder_path if folder_path[-1] == "/" else folder_path+"/"
    all_folder_files = os.listdir(path=folder_path)

    audio_folder_files = []
    for file in all_folder_files:
        full_file_path = folder_path+file
        _, file_extension = os.path.splitext(full_file_path)
        if file_extension in SUPPORTED_FILES:
            audio_folder_files.append(full_file_path)
    ipas = multiple_audio_to_ipa(audio_folder_files, saving, think_value)
    if saving:
        save_all(ipas, folder_path)
    return ipas


if __name__ == "__main__":
    print(DEVICE)
    print(audio_to_ipa("./audio.mp3", think_value=0.65))
    for i in folder_audio_to_ipa('./data/!!!\\', think_value=0.65):
        print(i[0], i[1], sep="\t")
