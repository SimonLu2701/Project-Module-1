import streamlit as st


def levenshtein_distance(token1, token2):
    # Initialize distances matrix
    m = len(token1)
    n = len(token2)
    distances = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize first row and column
    for i in range(m + 1):
        distances[i][0] = i
    for j in range(n + 1):
        distances[0][j] = j

    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if token1[i - 1] == token2[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            distances[i][j] = min(distances[i - 1][j] + 1,      # Deletion
                                  distances[i][j - 1] + 1,      # Insertion
                                  distances[i - 1][j - 1] + substitution_cost)  # Substitution

    # Return the Levenshtein distance
    return distances[m][n]



def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


vocabs = load_vocab(file_path='./data/vocab.txt')


def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):

        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)

        # sorted by distance
        sorted_distences = dict(
            sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)

        col2.write('Distances:')
        col2.write(sorted_distences)


if __name__ == "__main__":
    main()
