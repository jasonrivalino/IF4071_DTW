import scipy.io.wavfile as wav
from python_speech_features import mfcc

# Function to extract MFCC features using python_speech_features
def extract_mfcc(file_path):
    # Load the audio file
    rate, sig = wav.read(file_path)
    # Extract MFCC features
    mfcc_feat = mfcc(sig, rate)
    return mfcc_feat