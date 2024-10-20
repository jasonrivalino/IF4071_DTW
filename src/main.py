import os
from dtw import dtw
from mfcc import extract_mfcc

# Function to compare two audio files using DTW
def compare_audio_files(selected_files, threshold=100.0):
    # Check if there are at least two files to compare
    if len(selected_files) < 2:
        return "Not enough files to compare."
    
    # Extract MFCC features from the first file
    mfcc1 = extract_mfcc(selected_files[0])
    
    results = []
    
    # Loop through the rest of the files and compare them to the first file
    for file in selected_files[1:]:
        # Extract MFCC features from the current file
        mfcc2 = extract_mfcc(file)
        
        # Calculate DTW similarity
        distance = dtw(mfcc1, mfcc2)
        
        # Prepare the result message
        if distance < threshold:
            result = f"Sound between {os.path.basename(selected_files[0])} and {os.path.basename(file)} have {distance} distance"
        else:
            result = f"Sound between {os.path.basename(selected_files[0])} and {os.path.basename(file)} have {distance} distance"
        
        # Append the result along with the distance for sorting
        results.append((distance, result))
    
    # Sort the results by distance (first element of the tuple)
    results.sort(key=lambda x: x[0])
    
    # Extract only the result messages after sorting
    sorted_results = [result for _, result in results]
    
    return sorted_results

# Function to select folder and file input
def select_folder_and_file_input(current_dir):
    # Access all folders in the sound directory and choose 1 sound from each folder
    folders = os.listdir(os.path.join(current_dir, "..\\sound"))
    print("Pilih folder audio file:")
    for i, folder in enumerate(folders):
        print(f"{i+1}. {folder}")
    print()
    folder_choice = input("Masukkan pilihan dengan angka: ")
    
    # Determine folder based on input
    folder = folders[int(folder_choice) - 1]
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
            
# Function to select folder and file compare
def select_folder_and_file_compare(current_dir):
    # Access all folders in the sound directory
    sound_dir = os.path.join(current_dir, "..\\sound")
    folders = [f for f in os.listdir(sound_dir) if os.path.isdir(os.path.join(sound_dir, f))]
    
    selected_files = []

    # Loop through each folder and ask the user to choose a sound file from each one
    for folder in folders:
        print(f"Folder: {folder}")
        folder_path = os.path.join(sound_dir, folder)
        
        while True:
            # Ask user to input the sound file name without the extension
            file_input = input(f"Masukkan nama file audio di folder '{folder}' (tanpa format, e.g., input_sound): ")
            
            # Check for both .wav and .mp3 extensions
            file_path_wav = os.path.join(folder_path, file_input + ".wav")
            file_path_mp3 = os.path.join(folder_path, file_input + ".mp3")
            
            # Validate if file exists
            if os.path.isfile(file_path_wav):
                print(f"File ditemukan: {file_input}.wav di folder {folder}\n")
                selected_files.append(file_path_wav)
                break
            elif os.path.isfile(file_path_mp3):
                print(f"File ditemukan: {file_input}.mp3 di folder {folder}\n")
                selected_files.append(file_path_mp3)
                break
            else:
                print("File tidak ditemukan, coba lagi.")

    return selected_files

# Main function to compare all test cases
if __name__ == "__main__":
    dataset_dir = 'sound'
    testcase_dir = 'test cases'

    datasets = []
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.wav'):
                datasets.append(os.path.join(root, file))

    testcases = []
    for root, dirs, files in os.walk(testcase_dir):
        for file in files:
            if file.endswith('.wav'):
                testcases.append(os.path.join(root, file))

    # Iterate through each file and extract MFCC
    mfcc_dataset = {}
    mfcc_test = {}

    for filepath in datasets:
        mfcc_feat = extract_mfcc(filepath)
        mfcc_dataset[filepath] = mfcc_feat

    for filepath in testcases:
        mfcc_feat = extract_mfcc(filepath)
        mfcc_test[filepath] = mfcc_feat

    # Iterate and calculate the minimum distances
    for testfile, testmfcc in mfcc_test.items():
        print(f"----------- {testfile} -----------\n")

        results = []
        for datasetfile, datasetmfcc in mfcc_dataset.items():
            distance = dtw(testmfcc, datasetmfcc)
            results.append((distance, datasetfile))

        results.sort(key=lambda x: x[0])
        print(f"Test file: {testfile}")
        for result in results[:5]: # Show only top 5 results
            print(f"{result[1]}: {result[0]}")
        print("\n\n")