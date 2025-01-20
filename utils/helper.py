import os

def load_vocab():
    # Load the vocab from file and split by comma
    vocab_file = "vocab/vocab.txt"
    if not os.path.exists(vocab_file):
        print(f"Error: {vocab_file} not found.")
        vocab = []
    else:
        with open(vocab_file, "r", encoding="utf-8") as file:
            vocab_content = file.read().strip().replace("\n", "").replace("\r", "")
            vocab = vocab_content.split(",")  # Split characters by commas

    return vocab

