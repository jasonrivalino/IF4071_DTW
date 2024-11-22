import os
from dtw import dtw, dtw_library
from mfcc import extract_mfcc
import numpy as np

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
        
    # List to store average distances for each vowel group
    average_distances = []
    
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
                # Extract base vowel (e.g., 'A')
                dataset_vowel = os.path.basename(datasetfile).split(' ')[0]
                
                if vowel == dataset_vowel:  # Compare only if vowels match
                    dataset_mfcc = extract_mfcc(datasetfile)
                    distance = dtw(test_mfcc, dataset_mfcc)
                    results.append((distance, testfile, datasetfile))
        
        # Sort results by distance
        results.sort(key=lambda x: x[0])
        
        # Display the sorted results
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. Sound between {os.path.basename(result[1])} and {os.path.basename(result[2])} have {result[0]} distance")
        
        # Calculate and print average distance, then append to average_distances list
        average = sum([x[0] for x in results]) / len(results)
        print(f"Jarak rata-rata untuk vokal '{vowel}': {average}\n\n\n")
        
        # Append average distance for the vowel group
        average_distances.append(average)
        
    return average_distances

def compare_all_audio_files(directory_sound_input, directory_sound_compare):
    if len(directory_sound_input) < 1 or len(directory_sound_compare) < 1:
        return "Not enough files to compare."
    
    # List to store average distances for each comparison
    average_distances = []
    correct_count = 0
    total_count = 0
    
    # Iterate through each template file
    for templatefile in directory_sound_input:
        template_vowel = os.path.basename(templatefile).split(' ')[0]  # Extract base vowel (e.g., 'A')
        print(f"Comparing template file '{os.path.basename(templatefile)}' with test files:")
        
        results = []
        
        # Compare each test file with the current template file
        template_mfcc = extract_mfcc(templatefile)
        for testfile in directory_sound_compare:
            test_mfcc = extract_mfcc(testfile)
            distance = dtw(template_mfcc, test_mfcc)
            results.append((distance, testfile))
        
        # Sort results by distance
        results.sort(key=lambda x: x[0])
        
        # Display the sorted results
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. Sound between {os.path.basename(templatefile)} and {os.path.basename(result[1])} have {result[0]} distance")
        
        # Check if the shortest distance is to the correct vowel
        closest_testfile = results[0][1]
        closest_vowel = os.path.basename(closest_testfile).split(' ')[0]
        is_correct = (template_vowel == closest_vowel)
        print(f"Shortest distance for '{os.path.basename(templatefile)}' is to '{os.path.basename(closest_testfile)}' - {'Correct' if is_correct else 'Incorrect'}")
        
        # Update correct count and total count
        if is_correct:
            correct_count += 1
        total_count += 1
        
        # Calculate and print average distance, then append to average_distances list
        average = sum([x[0] for x in results]) / len(results)
        print(f"Jarak rata-rata untuk template '{os.path.basename(templatefile)}': {average}\n\n\n")
        
        # Append average distance for the template file
        average_distances.append(average)
    
    # Calculate accuracy
    accuracy = (correct_count / total_count) * 100
    
    return accuracy

# Function to select folder and file input
def select_folder_input(current_dir):
    folders = os.listdir(os.path.join(current_dir, "..\\template"))
    
    print("Pilih folder audio file:")
    for i, folder in enumerate(folders):
        print(f"{i+1}. {folder}")
    print()
    folder_choice = input("Masukkan pilihan dengan angka: ")
    
    while int(folder_choice) < 1 or int(folder_choice) > len(folders):
        print("Pilihan tidak valid.")
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
def select_folder_compare(current_dir, speakers_split=False):
    if speakers_split:
        # Choose test folder from seen_speakers folder or unseen_speakers folder
        print("Pilih folder audio file untuk perbandingan:")
        print("1. Seen Speakers")
        print("2. Unseen Speakers")
        folder_choice = input("Masukkan pilihan dengan angka: ")
        print()
        
        while folder_choice not in ["1", "2"]:
            print("Pilihan tidak valid.")
            folder_choice = input("Masukkan pilihan dengan angka: ")
            
        if folder_choice == "1":
            directory_name = "..\\test\\seen_speakers"
        else:
            directory_name = "..\\test\\unseen_speakers"
    else:
        directory_name = "..\\test\\seen_speakers"
    
    
    folders = os.listdir(os.path.join(current_dir, directory_name))
    
    print("Pilih folder audio file:")
    for i, folder in enumerate(folders):
        print(f"{i+1}. {folder}")
    print()
    
    folder_choice = input("Masukkan pilihan dengan angka: ")
    
    while int(folder_choice) < 1 or int(folder_choice) > len(folders):
        print("Pilihan tidak valid.")
        folder_choice = input("Masukkan pilihan dengan angka: ")
    
    folder = folders[int(folder_choice) - 1]
    
    while True:
        testcases = []
        directory_file = []
        
        print()
        print(f"Folder yang dipilih: {folder}")
        print(f"File .wav yang tersedia di folder ini:")
        
        for file in os.listdir(os.path.join(current_dir, directory_name, folder)):
            if file.endswith(".wav"):
                testcases.append(file)
                directory_file.append(os.path.join(current_dir, directory_name, folder, file))
                print(f"{len(testcases)}. {file}")
        print()
                
        if not testcases:
            print(f"Tidak ada file .wav di folder {folder}.")
            print()
            folder_choice = input("Masukkan pilihan dengan angka: ")
            folder = folders[int(folder_choice) - 1]            
        else:
            return testcases, directory_file

def pad_to_longest_mfccs(mfcc_list):
    """
    Pads MFCC arrays in the list to match the longest array's first dimension.
    Only pads arrays with less dimension.
    """
    max_length = max(mfcc.shape[0] for mfcc in mfcc_list)
    padded_mfccs = []

    for mfcc in mfcc_list:
        if mfcc.shape[0] < max_length:
            # Pad with zeros only to match max length
            padded = np.pad(mfcc, ((0, max_length - mfcc.shape[0]), (0, 0)), mode='constant')
            padded_mfccs.append(padded)
        else:
            # No padding needed
            padded_mfccs.append(mfcc)

    return np.array(padded_mfccs)

# Use this function before computing the mean
def compute_average_templates(template_folders):
    """Computes average MFCC templates for each vowel."""
    vowels = ['A', 'I', 'U', 'E', 'O']
    average_templates = {}

    for vowel in vowels:
        mfcc_list = []
        for folder in template_folders:
            all_files = os.listdir(os.path.join("template", folder))

            files = [f for f in all_files if f.startswith(vowel) and f.endswith('.wav')]

            for file in files:
                file_path = os.path.join("template", folder, file)
                mfcc_list.append(extract_mfcc(file_path))

        if mfcc_list:
            # Pad only the shorter MFCCs to match the longest
            padded_mfccs = pad_to_longest_mfccs(mfcc_list)
            # Compute the mean
            average_templates[vowel] = np.mean(padded_mfccs, axis=0)

    return average_templates

def compare_with_average_templates(average_templates, test_files, comparison_option):
    results = {}
    sorted_distance = {}
    correct_count = 0
    total_count = 0

    for testfile in test_files:
        test_vowel = os.path.basename(testfile).split(' ')[0]
        test_mfcc = extract_mfcc(testfile)
        distances = {}

        if test_vowel in average_templates:
            for vowel, avg_template_mfcc in average_templates.items():
                # Use your custom DTW function here
                distance = dtw(test_mfcc, avg_template_mfcc)
                distances[vowel] = distance

            speaker_name = os.path.basename(testfile).split('_')[0]  # Adjust based on your filename format
            if speaker_name not in results:
                results[speaker_name] = []
            results[speaker_name].append((os.path.basename(testfile), distances))

    for speaker, tests in results.items():
        print(f"\n{speaker}")
        if comparison_option == "1":
            # Extract only the vowels for the header
            vowels = [test[0].split()[0] for test in tests]  # Extract the first part of the filename as the vowel
            print("Audio Vowel\t\t" + "\t\t".join(vowels))
        else:
            print("Audio Vowel\t\tA\t\tE\t\tI\t\tO\t\tU")

        # Calculate and print averages
        if comparison_option == "1":
            avg_distances = {vowel: np.mean([distances[vowel] for _, distances in tests]) for vowel in vowels}
            avg_distances_str = "\t".join([f"{avg_distances[vowel]:.6f}" for vowel in vowels])
            print(f"Average Compare\t\t{avg_distances_str}")
        else:
            avg_distances = {vowel: np.mean([distances[vowel] for _, distances in tests]) for vowel in ['A', 'E', 'I', 'O', 'U']}
            avg_distances_str = "\t".join([f"{avg_distances[vowel]:.6f}" for vowel in ['A', 'E', 'I', 'O', 'U']])
            print(f"Average Compare\t\t{avg_distances_str}")
        
            # Sort results by distance
            sorted_distance = sorted(avg_distances.items(), key=lambda x: x[1])

            # Check if the shortest distance is to the correct vowel
            closest_vowel = sorted_distance[0][0]
            is_correct = (speaker[0] == closest_vowel)
            print(f"Shortest distance for Average Template Vowel '{speaker[0]}' is to '{closest_vowel}' - {'Correct' if is_correct else 'Incorrect'}")
                
            # Update correct count and total count
            if is_correct:
                correct_count += 1
            total_count += 1

    # Calculate accuracy
    if comparison_option != '1':
        accuracy = (correct_count / total_count) * 100
        print(f"Akurasi total: {accuracy}%")
    
    return results

def main_option_1(current_dir):
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
    
    print("MENAMPILKAN INFORMASI PERBANDINGAN SUARA:")
    print()
    compare_result = compare_audio_files(directory_sound_input, directory_sound_compare)

    print("----------------------------------------------------------------------------------------------------")
    print()
    print()
    print()
    
    # Show final information
    template_folder_name = os.path.basename(os.path.dirname(directory_sound_input[0]))
    test_folder_name = os.path.basename(os.path.dirname(directory_sound_compare[0]))
    
    print("INFORMASI AKHIR: ")
    print(f"Audio template yang dipilih yaitu: {template_folder_name}")
    print(f"Audio test yang dipilih yaitu: {test_folder_name}")
    print(f"Hasil perbandingan file audio untuk semua vokal: {compare_result}")
    all_average = sum(compare_result) / len(compare_result)
    print(f"Jarak rata-rata untuk semua vokal: {all_average}")
    print()

def main_option_2(current_dir):
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

    print("MENAMPILKAN INFORMASI PERBANDINGAN SUARA:")
    print()
    accuracy = compare_all_audio_files(directory_sound_input, directory_sound_compare)

    print("----------------------------------------------------------------------------------------------------")
    print()
    print()
    print()
    
    # Show final information
    template_folder_name = os.path.basename(os.path.dirname(directory_sound_input[0]))
    test_folder_name = os.path.basename(os.path.dirname(directory_sound_compare[0]))
    
    print("INFORMASI AKHIR: ")
    print(f"Audio template yang dipilih yaitu: {template_folder_name}")
    print(f"Audio test yang dipilih yaitu: {test_folder_name}")
    print(f"Akurasi total: {accuracy}%")
    print()

def main_average_templates():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define template folders
    template_folders = ["Faris (Template)", "Jason (Template)", "Louis (Template)", "Satria (Template)"]
    
    print()
    print()
    print("----------------------------------------------------------------------------------------------------")
    print()
    print()
    
    # Compute average templates
    print("Computing average templates...")
    average_templates = compute_average_templates(template_folders)
    print("Average templates computed successfully.")
    
    print()
    print()
    print("----------------------------------------------------------------------------------------------------")
    print()
    print()
    
    # Select test folder
    print("(1) Pilih folder dalam test untuk audio yang akan dibandingkan")
    [sound_compare, directory_sound_compare] = select_folder_compare(current_dir, speakers_split=True)
    print("Daftar file yang tersedia di sound compare: ")
    print(sound_compare)
    
    print()
    print()
    print("----------------------------------------------------------------------------------------------------")
    print()
    print()
    
    # Choose option between same vowel or all vowels
    print("Pilih opsi pencocokan dengan template rata-rata:")
    print("1. Pencocokan dengan template rata-rata untuk vokal yang sama")
    print("2. Pencocokan dengan template rata-rata untuk semua vokal")
    
    comparison_option = input("Masukkan pilihan Anda (1/2): ")
    
    while comparison_option not in ["1", "2"]:
        print("Pilihan tidak valid.")
        comparison_option = input("Masukkan pilihan Anda (1/2): ")
        
    print()
    print()
    print("----------------------------------------------------------------------------------------------------")
    print()
    print()
        
    if comparison_option == "1":
        # Compare using same vowel
        print("(2) Perhitungan dengan menggunakan average template untuk vokal yang sama:")
        compare_with_average_templates(average_templates, directory_sound_compare, comparison_option)
        print()
    else:    
        # Compare using averaged templates
        print("(2) Perhitungan dengan menggunakan average template untuk semua vokal:")
        compare_with_average_templates(average_templates, directory_sound_compare, comparison_option)
        print()

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
    
    print("Pilih opsi:")
    print("1. Melakukan perhitungan jarak antara file audio")
    print("2. Menghitung akurasi total")
    print("3. Menggunakan template rata-rata untuk perbandingan")
    choice = input("Masukkan pilihan Anda (1/2/3): ")

    while choice not in ["1", "2", "3"]:
        print("Pilihan tidak valid.")
        choice = input("Masukkan pilihan Anda (1/2/3): ")
        
    if choice == "1":
        main_option_1(current_dir)
    elif choice == "2":
        main_option_2(current_dir)
    elif choice == "3":
        main_average_templates()

if __name__ == "__main__":
    main()