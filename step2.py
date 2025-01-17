#pip install pandas
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string

#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')

def preprocess_text(text):
    #tokenization
    words = word_tokenize(str(text))  # Μετατρέπουμε σε string για να αντιμετωπίσουμε ακέραιους
    
    processed_words = []
    
    for word in words:
        #check if the word is a number
        if word.isdigit():
            processed_words.append(str(word))  # Αποθηκεύουμε τον ακέραιο ως string
        else:
            #remove punctuation( Αφαίρεση σημείων στίξης)
            word = word.strip(string.punctuation)
            
            #stemming(κοβω τις καταληξεις)
            stemmer = PorterStemmer()
            word = stemmer.stem(word)
            
            #lemmatization(απλοποιω τις λεξεις)
            lemmatizer = WordNetLemmatizer()
            word = lemmatizer.lemmatize(word)
            
            #remove stop words(σβήνω λέξεις χωρίς νόημα)
            stop_words = set(stopwords.words('english'))
            if word.lower() not in stop_words:
                processed_words.append(word.lower())
    
    return ' '.join(processed_words)

#διαβάζω το αρχείο results.json
df = pd.read_json(r'C:\Users\smoul\Anaktisi\results.json')


#εφαρμόζω την προεπεξεργασία σε κάθε κελί του πίνακα
for column in df.columns:
    df[column] = df[column].apply(preprocess_text)

#ορίζει τα νέα ονόματα για τις στήλες
new_columns = {
    0: 'First_Title',
    1: 'ID',
    2: 'Informations',
    3: 'Date',
    4: 'Content',
}

#μετονομάζει τις στήλες χρησιμοποιώντας το λεξικό που ορίσαμε
df = df.rename(columns=new_columns)

# Εφαρμογή του regex στη στήλη 'Content', αν υπάρχει
if 'Content' in df.columns:  # Ελέγχει αν υπάρχει στήλη 'text'
    df['Content'] = df['Content'].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', str(x)))

# Αποθηκεύω το νέο αρχείο processed.json
json_filename = "processed.json"
with open(json_filename, 'w', encoding='utf-8') as json_file:
    # Χρησιμοποιούμε τη μέθοδο to_json της pandas
    df.to_json(json_file, force_ascii=False, indent=2, orient="records")

print("Η επεξεργασία ολοκληρώθηκε και τα δεδομένα αποθηκεύτηκαν στο αρχείο processed.json.")
