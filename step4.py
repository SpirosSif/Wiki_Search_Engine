import json
import math
from collections import Counter

def user_interface():
    print("Καλώς ήρθατε στην μηχανή αναζήτησης για τους ήρωες του 1821!")

    while True:
        query = input("Εισαγάγετε το ερώτημά σας ή γράψτε exit για έξοδο: ").strip().lower()

        if query == 'exit':
            print("Ευχαριστούμε που χρησιμοποιήσατε τη μηχανη αναζήτησης μας.")
            break

        algorithm_choice = input("Επιλέξτε αλγόριθμο ανάκτησης:\n1) Boolean Retrieval\n2) Vector Space Model (VSM)\n3) Probabilistic Retrieval Models(OKAPI BM25)\nΕπιλογή: ").strip()

        if algorithm_choice == '1':
            boolean_retrieval(query)
            break
        elif algorithm_choice == '2':
            vector_space_model(query)
            break
        elif algorithm_choice == '3':
            probabilistic_retrieval(query)
            break
        else:
            print("Μη έγκυρη επιλογή αλγορίθμου. Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")

if __name__ == "__main__":
    user_interface()