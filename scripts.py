import os
import socket
import re
from collections import Counter

# Define file paths
file1_path = "/home/data/IF-1.txt"
file2_path = "/home/data/AlwaysRememberUsThisWay-1.txt"
output_directory = "/home/data/output"
output_file_path = os.path.join(output_directory, "result.txt")

# Ensure output directory exists before writing the file
os.makedirs(output_directory, exist_ok=True)

# Function to clean and split text into words
def clean_and_split(text):
    text = text.lower()
    text = re.sub(r"[^\w\s']", " ", text)  # Remove punctuation except apostrophes
    return text.split()

# Count words in each file
def count_words(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            words = clean_and_split(file.read())
            return len(words), words
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return 0, []

# Get word counts
count1, words1 = count_words(file1_path)
count2, words2 = count_words(file2_path)

# Calculate grand total
grand_total = count1 + count2

# Identify top 3 most frequent words in IF-1.txt
top_3_if1 = Counter(words1).most_common(3)

# Handle contractions in AlwaysRememberUsThisWay-1.txt
contractions = {
    "i'm": ["i", "am"],
    "can't": ["can", "not"],
    "don't": ["do", "not"],
    "isn't": ["is", "not"],
    "aren't": ["are", "not"],
    "it's": ["it", "is"],
    "they're": ["they", "are"],
    "we're": ["we", "are"]
}

expanded_words2 = []
for word in words2:
    if word in contractions:
        expanded_words2.extend(contractions[word])
    else:
        expanded_words2.append(word)

# Identify top 3 most frequent words in AlwaysRememberUsThisWay-1.txt
top_3_always_remember = Counter(expanded_words2).most_common(3)

# Determine the IP address of the machine running the container
ip_address = socket.gethostbyname(socket.gethostname())

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Write results to output file
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(f"Total words in IF-1.txt: {count1}\n")
    f.write(f"Total words in AlwaysRememberUsThisWay-1.txt: {count2}\n")
    f.write(f"Grand total of words: {grand_total}\n")
    f.write(f"Top 3 words in IF-1.txt: {top_3_if1}\n")
    f.write(f"Top 3 words in AlwaysRememberUsThisWay-1.txt: {top_3_always_remember}\n")
    f.write(f"IP Address: {ip_address}\n")

# Print results to console before exiting
with open(output_file_path, "r", encoding="utf-8") as f:
    print(f.read())
