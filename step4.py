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
       
        else:
            print("Μη έγκυρη επιλογή αλγορίθμου. Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")

def boolean_retrieval(query):
    inverted_index = load_inverted_index()
    processed = load_processed()
    if inverted_index is None:
        print("Η λειτουργία Boolean Retrieval δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return
    if processed is None:
        print("Η λειτουργία Boolean Retrieval δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return
    query = query.replace('and', ' ') #.replace('or', ' ').replace('not', ' ')
    terms = query.split()
    print(f"Εκτέλεση Boolean Retrieval για το ερώτημα: {terms}")
    print (terms)
    result = []
#    result1 = set()
    result_and = "1"*20
 
    for term in terms:
        if term.lower() in inverted_index:
            result.append(inverted_index[term.lower()])
 #           result1.update(processed[term.lower()])
        result_and = result_and and inverted_index[term]

    print(f"result of and: {result_and}")    
    #print(f"Αποτελέσματα Boolean Retrieval: {result}")

#φορτώνω τα στοιχεία του inverted_index.json 
def load_inverted_index(file_path='boolean_inverted_index.json'):
    
    try:
        with open(file_path,'r') as json_file:
            inverted_index = json.load(json_file)
        return inverted_index
    except FileNotFoundError:
        print(f"Το αρχείο {file_path} δεν βρέθηκε.")
        return None
          
#φορτώνω τα στοιχεία του inverted_index.json 
def load_processed(file_path='processed.json'):
    try:
        with open(file_path,'r') as processed_file:
            processed = json.load(processed_file)
        return processed
    except FileNotFoundError:
        print(f"Το αρχείο {file_path} δεν βρέθηκε.")
        return None



if __name__ == "__main__":
    user_interface()
