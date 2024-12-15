import json

# Διαβάζω το αρχείο JSON
with open(r'C:\Users\smoul\Anaktisi\processed.json', 'r') as f:
    documents = json.load(f)  # Φορτώνω τα δεδομένα

# Λίστα που θα περιέχει όλους τους όρους
all_terms = []

# Αντίστροφο ευρετήριο
inverted_index = {}
boolean_inverted_index = {}
temp = {}

# Επεξεργασία κάθε εγγράφου
for document in documents: # for document in all_data:
    doc_id = document.get('ID')
    for field, field_value in document.items():
        if field == "ID": # ερώτηση
            continue
        if isinstance(field_value, str):  # Ελέγχω αν το πεδίο είναι string
            terms = field_value.split()
            all_terms.extend(terms)  # Προσθήκη όρων στη λίστα για όλα τα έγγραφα

            # Δημιουργία του ανεστραμμένου ευρετηρίου
            for term in terms:
                if term in inverted_index:
                    inverted_index[term].append(doc_id)
                else:
                    inverted_index[term] = [doc_id]
    
for term in inverted_index:
    unique_ids = set(inverted_index[term])  # Αφαιρούμε τα διπλότυπα
    sorted_ids = sorted(unique_ids, key=int)  # Ταξινομούμε αριθμητικά
    inverted_index[term] = sorted_ids  # Μετατροπή σε λίστα και ενημέρωση του inverted_index
    
for term in inverted_index:
    temp = inverted_index[term]
    if term not in boolean_inverted_index:
        boolean_inverted_index[term] = []
    for index in range(20):
        if index < len(temp) and temp[index] == str(index + 1):
            boolean_inverted_index[term].append(str(1))
        else:
            boolean_inverted_index[term].append(str(0))
            
    
    
# Αποθήκευση του ανεστραμμένου ευρετηρίου σε ένα αρχείο JSON
with open('inverted_index.json', 'w') as json_file:
    json.dump(inverted_index, json_file)
    
# Αποθήκευση του ανεστραμμένου ευρετηρίου σε ένα αρχείο JSON
with open('boolean_inverted_index.json', 'w') as json_file:
    json.dump(boolean_inverted_index, json_file)

# Δοκιμαστική εκτύπωση μερικών όρων
print(all_terms[:10])
