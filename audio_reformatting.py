import librosa
import numpy as np


SR = 11025
N_FFT = 1024

# Преобразование аудиофайла
def audio_reformatting(audio_path:str="./audio.mp3"):
    y, _ = librosa.load(audio_path, sr=SR)
    D_transpose_npy = np.transpose(librosa.stft(y, n_fft=N_FFT))
    return D_transpose_npy
