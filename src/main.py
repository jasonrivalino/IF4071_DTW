import os
from dtw import dtw
from mfcc import extract_mfcc

# Function to compare two audio files using DTW and group them by vowel
def compare_audio_files(directory_sound_input, directory_sound_compare):
    if len(directory_sound_input) < 1 or len(directory_sound_compare) < 1:
        return "Not enough files to compare."
    
    # Extract vowel from file names for grouping (e.g., 'A', 'E', etc.)
    test_file_groups = {}
    
    # Group test files by their vowel (base name)
    for testfile in directory_sound_compare:
        vowel = os.path.basename(testfile).split(' ')[0]  # Extract base vowel (e.g., 'A')
        
        if vowel not in test_file_groups:
            test_file_groups[vowel] = []
        test_file_groups[vowel].append(testfile)
    
    # Iterate through each group of test files (by vowel)
    for vowel, testfiles in test_file_groups.items():
        print(f"Voice files for vowel '{vowel}':")
        print(f"Template files: [{', '.join([os.path.basename(f) for f in directory_sound_input])}]")
        print(f"Test files: [{', '.join([os.path.basename(f) for f in testfiles])}]")
        print()
        print("Hasil perbandingan file audio:")
        
        results = []
        
        # Compare test files with template files that have the same vowel
        for testfile in testfiles:
            test_mfcc = extract_mfcc(testfile)
            
            for datasetfile in directory_sound_input:
                dataset_vowel = os.path.basename(datasetfile).split(' ')[0]  # Extract base vowel (e.g., 'A')
                
                if vowel == dataset_vowel:  # Compare only if vowels match
                    dataset_mfcc = extract_mfcc(datasetfile)
                    distance = dtw(test_mfcc, dataset_mfcc)
                    results.append((distance, testfile, datasetfile))
        
        # Sort results by distance
        results.sort(key=lambda x: x[0])
        
        # Display the sorted results
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. Sound between {os.path.basename(result[1])} and {os.path.basename(result[2])} have {result[0]} distance")
        print("\n")
    
    return results

# Function to select folder and file input
def select_folder_input(current_dir):
    folders = os.listdir(os.path.join(current_dir, "..\\template"))
    
    print("Pilih folder audio file:")
    for i, folder in enumerate(folders):
        print(f"{i+1}. {folder}")
    print()
    folder_choice = input("Masukkan pilihan dengan angka: ")
    
    folder = folders[int(folder_choice) - 1]
    
    while True:
        datasets = []
        directory_file = []
        
        print()
        print(f"Folder yang dipilih: {folder}")
        print(f"File .wav yang tersedia di folder ini:")
        
        for file in os.listdir(os.path.join(current_dir, "..\\template", folder)):
            if file.endswith(".wav"):
                datasets.append(file)
                directory_file.append(os.path.join(current_dir, "..\\template", folder, file))
                print(f"{len(datasets)}. {file}")
        print()
                
        if not datasets:
            print(f"Tidak ada file .wav di folder {folder}.")
            print()
            folder_choice = input("Masukkan pilihan dengan angka: ")
            folder = folders[int(folder_choice) - 1]            
        else:
            return [datasets, directory_file]

# Function to select folder and file compare
def select_folder_compare(current_dir):
    folders = os.listdir(os.path.join(current_dir, "..\\test"))
    
    print("Pilih folder audio file:")
    for i, folder in enumerate(folders):
        print(f"{i+1}. {folder}")
    print()
    
    folder_choice = input("Masukkan pilihan dengan angka: ")
    
    folder = folders[int(folder_choice) - 1]
    
    while True:
        testcases = []
        directory_file = []
        
        print()
        print(f"Folder yang dipilih: {folder}")
        print(f"File .wav yang tersedia di folder ini:")
        
        for file in os.listdir(os.path.join(current_dir, "..\\test", folder)):
            if file.endswith(".wav"):
                testcases.append(file)
                directory_file.append(os.path.join(current_dir, "..\\test", folder, file))
                print(f"{len(testcases)}. {file}")
        print()
                
        if not testcases:
            print(f"Tidak ada file .wav di folder {folder}.")
            print()
            folder_choice = input("Masukkan pilihan dengan angka: ")
            folder = folders[int(folder_choice) - 1]            
        else:
            return testcases, directory_file

# Main function to compare all test cases
if __name__ == "__main__":
    dataset_dir = 'template'
    testcase_dir = 'test'
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
    
    print("\n(1) Pilih folder dalam template untuk audio input")
    print()
    [sound_input, directory_sound_input] = select_folder_input(current_dir)
    print("Daftar file yang tersedia di folder sound input: ")
    print(sound_input)
    
    print()
    print()
    print("----------------------------------------------------------------------------------------------------")
    print()
    
    print("\n(2) Pilih folder dalam test untuk audio yang akan dibandingkan")
    print()
    [sound_compare, directory_sound_compare] = select_folder_compare(current_dir)
    print("Daftar file yang tersedia di sound compare: ")
    print(sound_compare)
    
    print()
    print()
    print("----------------------------------------------------------------------------------------------------")
    print()
    print()
    
    compare_result = compare_audio_files(directory_sound_input, directory_sound_compare)