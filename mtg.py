import re

def define_vocab(corpus):
    vocab = []
    for i in range(len(corpus)):
        word = corpus[i]
        if word in vocab:
            continue
        else:
            vocab.append(word)
    return vocab    

def train_model(corpus:list, n:int):
    n_gram_dict = {}
    for i in range(len(corpus) - (n-1)):
        gram = ",".join(corpus[i:i+n])
        if gram in n_gram_dict.keys():
            n_gram_dict[gram] += 1
        else:
            n_gram_dict[gram] = 1
    return n_gram_dict

def finish_sentence(sentence: list, n: int, corpus: list, randomize=False):
    vocab = define_vocab(corpus)
    corpus_length = len(corpus)
    next_word = find_sequence(sentence, n, vocab, corpus_length, corpus, randomize)
    sentence.append(next_word)
    print(f"The next best word is '{next_word}'")
    if (len(sentence)==10) | (sentence[-1]== "."):
        print(sentence)
        return sentence
    else:
        return finish_sentence(sentence=sentence, n=n, corpus=corpus, randomize=False)
                    
def find_sequence(sentence:list, n:int, vocab, corpus_length, corpus, randomize):
    while n > 0:
        word_scores = {}
        if n > 1:
            input_text = ",".join(sentence[-(n-1):])
            testgramdict = train_model(corpus, n)
            lowergramdict = train_model(corpus, n-1)
            lower_gram = input_text
            if lowergramdict.get(lower_gram, 0) == 0:
                print("Need Lower N-Gram Up Here")
                n-=1
                continue
        elif n == 1:
            input_text = ""
            testgramdict = train_model(corpus, n)

        for word in vocab:
            if n > 1:
                if type(lower_gram) == tuple:
                    pass
                elif type(lower_gram) == str:
                    test_gram = lower_gram + "," + word
                test_gram_count = testgramdict.get(test_gram, 0)
                lower_gram_count = lowergramdict.get(lower_gram, 0)
                word_scores[word] = test_gram_count / lower_gram_count
            elif n == 1:
                word_scores[word] = testgramdict[word] / corpus_length
        
        if any(value > 0 for value in word_scores.values()):
            print('next word has been identified')
            highest_score = max(word_scores.values())
            best_words = []
            for key, value in word_scores.items():
                if value == highest_score:
                    best_words.append(key)
            #return best_words
        else:
            n-=1
            print("Need Lower N-Gram Down Here")
        if len(best_words) > 1:
            next_word = best_word_tie(best_words, input_text, corpus, n)
        elif len(best_words) == 1:
            next_word = best_words[0]
        return next_word
    
def best_word_tie(best_words, input_text, corpus, n):
    current_best_index = None
    for word in best_words:
        sequence = input_text + word
        for i in range(len(corpus) - (n-1)):
            test_seq = ",".join(corpus[i:i+n])
            if (test_seq == sequence):
                if current_best_index == None:
                    current_best_index = i
                    next_word = word
                elif i < current_best_index:
                    current_best_index = i
                    next_word = word 
                else:
                    continue
            else:
                continue
    return next_word

if __name__ == "__main__":
    corpus = "Babe. Theres something tragic about you. Something so magic about you, dont you agree? Babe. Theres something lonesome about you. Something so wholesome about you, get closer to me."
    # Use regular expression to split by spaces or punctuation
    split_tokens = re.findall(r'\w+|[.,!?]|[\'`]\w+|\w+[\'`]\w+', corpus)
    

    # Remove empty strings from the result
    split_tokens = [token for token in split_tokens if token]
    lower_corpus = [w.lower() for w in split_tokens]
    #define_ngram(lower_corpus)
    sentence = finish_sentence(["robot"], 10, lower_corpus, False)
    print(sentence)
    #vocab = define_vocab(lower_corpus)
    #print(vocab)



### determine most recent word inside the find_sequence function so that you can use the
### n value used in find_sequence, not just the default n value passed into the function.