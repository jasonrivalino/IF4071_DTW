import os
from dtw import dtw
from mfcc import extract_mfcc

# Function to compare two audio files using DTW
def compare_audio(file1, file2, threshold=100.0):
    # Extract MFCC features from both audio files
    mfcc1 = extract_mfcc(file1)
    mfcc2 = extract_mfcc(file2)
    
    # Calculate DTW similarity
    distance = dtw(mfcc1, mfcc2)
    
    # Check if the distance is within the threshold
    if distance < threshold:
        return f"Match! Distance: {distance}, below threshold {threshold}."
    else:
        return f"No match. Distance: {distance}, exceeds threshold {threshold}."


# Function to select folder and file
def select_folder_and_file(current_dir):
    # Loop for selecting the folder
    while True:
        print("Pilih folder audio file:")
        print("1. Jason")
        print("2. Louis")
        print("3. Satria")
        print("4. Faris")
        print()
        folder_choice = input("Masukkan pilihan dengan angka: ")
        
        # Determine folder based on input
        if folder_choice == "1":
            folder = "1 - Jason"
            break
        elif folder_choice == "2":
            folder = "2 - Louis"
            break
        elif folder_choice == "3":
            folder = "3 - Satria"
            break
        elif folder_choice == "4":
            folder = "4 - Faris"
            break
        else:
            print("Pilihan tidak valid, coba lagi.")
    
    print(f"Folder yang dipilih: {folder}")
    
    # Loop for selecting the file name
    while True:
        file_input = input("\nTulis nama file audio input (tanpa format, e.g., input_sound): ")
        
        # Automatically append the file extension if the user doesn't include it
        file_path_wav = os.path.join(current_dir, "..\\sound", folder, file_input + ".wav")
        file_path_mp3 = os.path.join(current_dir, "..\\sound", folder, file_input + ".mp3")
        
        # Check if the file exists with .wav or .mp3 extension
        if os.path.isfile(file_path_wav):
            print(f"File ditemukan: {file_input}.wav")
            print()
            return file_path_wav
        elif os.path.isfile(file_path_mp3):
            print(f"File ditemukan: {file_input}.mp3")
            print()
            return file_path_mp3
        else:
            print("File tidak ditemukan, coba lagi.")


# Main function to compare two audio files
if __name__ == "__main__":
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
    
    # Select folder and file for file1
    print("\n(1) Pilih folder dan file untuk audio input")
    print()
    file1 = select_folder_and_file(current_dir)
    
    # Select folder and file for file2
    print("\n(2) Pilih folder dan file untuk audio yang akan dibandingkan")
    print()
    file2 = select_folder_and_file(current_dir)
    
    # Threshold for DTW comparison
    threshold = 150
    
    # Compare the two audio files
    result = compare_audio(file1, file2, threshold=threshold)
    print(result)