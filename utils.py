def normalize(text):  # just - test.text = test.text.apply(normalize)
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


def clean_text(text):  # just - test.text = test.text.apply(normalize)
    # from pymorphy2 import MorphAnalyzer
    import re

    # morph = MorphAnalyzer()
    # global_morph = {}
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    return text


def is_finance(clf, vect, text):
    proba = clf.predict_proba(vect.transform([text]))
    ar = clf.predict_proba(vect.transform(['Ришат']))
    if str(proba[0]) == str(ar[0]):
        return False
    else:
        return True


def save(clf, file_name='saved_clf.pkl'):
    from sklearn.externals import joblib

    joblib.dump(clf, file_name, compress=9)


def load(file_name):
    from sklearn.externals import joblib

    clf = joblib.load(file_name)

    return clf


def get_results(clf, vectorizer, X):
    a = clf.predict_proba(vectorizer.transform([X]))
    h = a[0]
    ans = {}
    for i in range(len(h)):
        ans[i] = h[i]
    ans = sorted(ans.items(), key=lambda x: x[1], reverse=True)
    return ans


def check_credit(message, answer):
    if answer == [10, 9]:
        return True
    elif message == "не финансовое сообщение":
        return True
