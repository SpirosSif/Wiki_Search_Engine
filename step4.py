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
        if  algorithm_choice == '2':
            vector_space_model(query)
        if algorithm_choice == '3':
            probabilistic_retrieval(query)
       
        else:
            print("Μη έγκυρη επιλογή αλγορίθμου. Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")

def boolean_retrieval(query):
    inverted_index =  load_inverted_index_for_boolean()
    processed = load_processed()
    if inverted_index is None:
        print("Η λειτουργία Boolean Retrieval δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return
    if processed is None:
        print("Η λειτουργία Boolean Retrieval δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return
    result = []
    
    if "and" in query:
        query = query.replace('and', ' ')
        terms = query.split()
        print(f"Εκτέλεση Boolean Retrieval για το ερώτημα: {terms}")
        print (terms)
        #result = []
#    result1 = set()
        result_and = "1"*20
 
        for term in terms:
            if term.lower() in inverted_index:
                result.append(inverted_index[term.lower()])
 #           result1.update(processed[term.lower()])
            result_and = result_and and inverted_index[term]
        print(f"result of and: {result_and}")

    if "or" in query:
        query = query.replace('or', ' ')
        terms = query.split()
        print(f"Εκτέλεση Boolean Retrieval για το ερώτημα: {terms}")
        print (terms)
            #result = []
    #    result1 = set()
        result_or = "1"*20
     
        for term in terms:
            if term.lower() in inverted_index:
                result.append(inverted_index[term.lower()])
     #           result1.update(processed[term.lower()])
            result_or = result_or or inverted_index[term]
        result_or = list(result_or)
        print(f"result of or: {result_or}")
        
    if "not" in query:
       query = query.replace('not', ' ')
       terms = query.split()
       print(f"Εκτέλεση Boolean Retrieval για το ερώτημα: {terms}")
    
       result_not = "1" * 20  # Ξεκινάμε με όλα τα έγγραφα (όλα "1")

       for term in terms:
            if term.lower() in inverted_index:
                result.append(inverted_index[term.lower()])
 #           result1.update(processed[term.lower()])
            result_not = result_not and inverted_index[term]
       print(f"Αποτέλεσμα NOT !: {result_not}")
       size_of_list = len(result_not)
       for i in range(size_of_list):
            if result_not[i] == '1':
                result_not[i] = '0'
            else:
                result_not[i] = '1'

       print(f"Αποτέλεσμα NOT: {result_not}")
    
    
    #print(f"Αποτελέσματα Boolean Retrieval: {result}")

def vector_space_model(query):
    inverted_index = load_inverted_index()

    if inverted_index is None:
        print("Η λειτουργία Vector Space Model δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return

    terms = query.split()
    print(f"Εκτέλεση Vector Space Model για το ερώτημα: {terms}")

    document_vectors = {}
    query_vector = Counter(terms)

    for term, query_term_freq in query_vector.items():
        lower_term = term.lower()
        if lower_term in inverted_index:
            idf = math.log10(len(inverted_index) / len(inverted_index[lower_term]))

            for doc_id in inverted_index[lower_term]:
                doc_term_freq = inverted_index[lower_term].count(doc_id)
                tf_idf = doc_term_freq * idf

                if doc_id in document_vectors:
                    document_vectors[doc_id] += tf_idf * query_term_freq
                else:
                    document_vectors[doc_id] = tf_idf * query_term_freq

    # Ταξινόμηση των εγγράφων βάσει του cosine similarity
    ranked_documents = sorted(document_vectors.items(), key=lambda x: x[1], reverse=True)

    print(f"Αποτελέσματα Vector Space Model: {ranked_documents}")

def probabilistic_retrieval(query):
    processed = load_processed()

    if processed is None:
        print("Η λειτουργία Probabilistic Retrieval δεν είναι δυνατή λόγω απουσίας αρχείου processed.json.")
        return

    # Constants for BM25
    k1 = 1.5
    b = 0.75
    N = len(processed)  # Συνολικός Αριθμός των εγγράφων
    
    # Υπολογισμός του συνολικού αριθμού λέξεων στο "Content"
    total_words = 0
    for doc in processed:
        if "Content" in doc:  # Ελέγχει αν υπάρχει το πεδίο "Content"
            content = doc["Content"]
            total_words += len(content.split())  # Διαχωρισμός σε λέξεις και μέτρηση
    
    # Υπολογισμός του avgdl (μέσος αριθμός λέξεων ανά έγγραφο)
    if N > 0:
        avgdl = total_words / N
    else:
        N = 0

    # Διαχωρισμός του ερωτήματος σε όρους
    terms = query.split()
    scores = {}

    for doc in processed:
        if "Content" not in doc:
            continue  # Παράβλεψη εγγράφων χωρίς πεδίο "Content"

        content = doc["Content"]
        doc_length = len(content.split())
        doc_term_counter = Counter(content.lower().split())  # Καταμέτρηση συχνότητας όρων στο έγγραφο
        score = 0

        for term in terms:
            term = term.lower()  # Μετατροπή του όρου σε πεζά για σύγκριση
            ft = doc_term_counter.get(term, 0)  # Συχνότητα του όρου στο έγγραφο

            # Υπολογισμός Document Frequency (DF)
            
            df = 0 
            for d in processed:
                if "Content" in d and term in d["Content"].lower():
                    df = df + 1

            if df == 0:
                continue  # Παράβλεψη όρων που δεν εμφανίζονται σε κανένα έγγραφο

            # Υπολογισμός IDF
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1)

            # Υπολογισμός TF
            tf = (ft * (k1 + 1)) / (ft + k1 * (1 - b + b * (doc_length / avgdl)))

            # Υπολογισμός BM25 score
            score += idf * tf

        # Αποθήκευση του σκορ για το συγκεκριμένο έγγραφο
        scores[doc["ID"]] = score  # Υποθέτουμε ότι τα έγγραφα έχουν πεδίο "ID"

    # Ταξινόμηση των εγγράφων κατά αύξουσα σειρά του ID
    ranked_documents = sorted(scores.items(), key=lambda x: float(x[1]), reverse= True)

    # Εκτύπωση των αποτελεσμάτων
    print(f"Αποτελέσματα Probabilistic Retrieval για το ερώτημα '{query}':")
    for doc_id, score in ranked_documents:
        print(f"Έγγραφο ID: {doc_id}, Σκορ: {score}")

#φορτώνω τα στοιχεία του boolean_inverted_index.json 
def load_inverted_index_for_boolean(file_path='boolean_inverted_index.json'):
    
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
    

#φορτώνω τα στοιχεία του inverted_index.json 
def load_inverted_index(file_path='inverted_index.json'):
    
    try:
        with open(file_path,'r') as json_file:
            inverted_index = json.load(json_file)
        return inverted_index
    except FileNotFoundError:
        print(f"Το αρχείο {file_path} δεν βρέθηκε.")
        return None

if __name__ == "__main__":
    user_interface()
