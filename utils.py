def normalize(text): #just - test.text = test.text.apply(normalize)
    from pymorphy2 import MorphAnalyzer
    import re
    
    morph = MorphAnalyzer()
    global_morph = {}
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    words = re.findall(r'\w+', text)
    tmp = ""
    for word in words:
        if word in global_morph.keys():
            tmp += global_morph[word].normal_form
        else:
            global_morph[word] = morph.parse(word)[0]
            tmp += global_morph[word].normal_form
        tmp += " "
    return tmp[:-1]


def simple_del(text): #just - test.text = test.text.apply(normalize)
    #from pymorphy2 import MorphAnalyzer
    import re
    
    #morph = MorphAnalyzer()
    #global_morph = {}
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    return text

def save(clf, file_name = 'saved_clf.pkl'):
    from sklearn.externals import joblib
    
    joblib.dump(clf, file_name, compress=9)


def load(file_name):
    from sklearn.externals import joblib
    
    clf = joblib.load(file_name)
    
    return clf