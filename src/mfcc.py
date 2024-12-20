import scipy.io.wavfile as wav
from python_speech_features import mfcc
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

# Adding pre-processing functions using Gaussian Mixture Models (GMMs) for feature extraction
def gaussian_preprocessing(mfcc_features, sigma=1):
    # Apply Gaussian filter to the MFCC features
    mfcc_features = gaussian_filter(mfcc_features, sigma=sigma)
    
    return mfcc_features

# Function to extract MFCC features using python_speech_features
def extract_mfcc(file_path, sigma=1):
    # Load the audio file
    rate, sig = wav.read(file_path)
    
    # Extract MFCC features with increased NFFT to avoid warning
    mfcc_feat = mfcc(sig, rate, nfft=2048)  # Increased NFFT size to avoid truncation warning
    
    # Apply Gaussian preprocessing to the MFCC features
    mfcc_smooth = gaussian_preprocessing(mfcc_feat)
    
    return mfcc_smooth