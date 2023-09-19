import re
import numpy as np

def define_vocab(corpus):
    '''Returns list of unique words in corpus called vocab'''
    vocab = []
    for i in range(len(corpus)):
        word = corpus[i]
        if word in vocab:
            continue
        else:
            vocab.append(word)
    return vocab    

def train_model(corpus:list, n:int):
    '''Returns dictionary: n_gram_dict
      KEY: Unique n-grams of length n
      VALUE: Count of occurances in corpus'''
    
    n_gram_dict = {}
    for i in range(len(corpus) - (n-1)):
        gram = ",".join(corpus[i:i+n]) ## join n-gram into single string of text with delimitor: ","
        if gram in n_gram_dict.keys(): 
            n_gram_dict[gram] += 1 ## if n-gram is in dictionary, add 1 to value (count)
        else:
            n_gram_dict[gram] = 1 ## if n-gram is not in dictionary, add it to dictionary and set value (count) == 1
    return n_gram_dict

def finish_sentence(sentence: list, n: int, corpus: list, randomize=False):
    '''Recurssive function that appends new words to sentence.
    Function completes when sentence length reaches 10 or a period is found.'''

    vocab = define_vocab(corpus)
    corpus_length = len(corpus)
    next_word = find_sequence(sentence, n, vocab, corpus_length, corpus, randomize)
    sentence.append(next_word)
    print(f"The next best word is '{next_word}'")
    if (len(sentence)==10) | (sentence[-1]== "."):
        print(sentence)
        return sentence
    else:
        return finish_sentence(sentence=sentence, n=n, corpus=corpus, randomize=randomize)
                    
def find_sequence(sentence:list, n:int, vocab:list, corpus_length, corpus, randomize):
    '''Identifies and returns the most likely next word using applicable n-gram model and stupid backoff'''
    
    while n > 0:
        word_scores = {}
        if n > 1:
            input_text = ",".join(sentence[-(n-1):]) ## join n-gram into single string of text with delimitor: ","
            lowergramdict = train_model(corpus, n-1) ## Denominator dictionary in n-gram equation
            if lowergramdict.get(input_text, 0) == 0: ## Stupid Backoff if input_text is not found in corpus.
                print("Need Lower N-Gram Up Here")
                n-=1
                continue
            lower_gram_count = lowergramdict.get(input_text, 0) ## Denominator for given input_text
            testgramdict = train_model(corpus, n) ## Create dictionary of n-grams of length n (numerator)
        elif n == 1:
            input_text = ""
            testgramdict = train_model(corpus, n) ## If using unigram, only need one n-gram dictionary

        for word in vocab: ## calculate probability of each n-gram
            if n > 1: ## Use sentence history for probability
                test_gram = input_text + "," + word
                test_gram_count = testgramdict.get(test_gram, 0)
                word_scores[word] = test_gram_count / lower_gram_count
            elif n == 1: ## Use (word count) / (total corpus count) for unigram
                word_scores[word] = testgramdict[word] / corpus_length

        if randomize == False: ## Deterministic Route
            if any(value > 0 for value in word_scores.values()): ## If any word has probability > 0, find word in word_scores.
                print('next word has been identified')
                highest_score = max(word_scores.values())
                best_words = []
                for key, value in word_scores.items():
                    if value == highest_score:
                        best_words.append(key)
            else: ## If all words in vocab have 0% probability, backoff
                n-=1
                print("Need Lower N-Gram Down Here")
                continue

            if len(best_words) > 1: ## if more than one word identified with highest probability
                next_word = best_word_tie(best_words, input_text, corpus, n)
            elif len(best_words) == 1: ## if only one word identified with highest probability
                next_word = best_words[0]

            return next_word
        
        else: # Randomized sampling route
            num = np.random.random()
            tot = 0
            for key, value in word_scores.items():
                tot += value
                if tot > num:
                    return key

def best_word_tie(best_words, input_text, corpus, n):
    '''Iterate through corpus and find earliest occurance of n-grams using words in best_words'''
    current_best_index = None
    for word in best_words:
        if input_text == "":
            sequence = word
        else:
            sequence = input_text + "," + word ## Create n-gram with potential next word
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

    #sentence = finish_sentence([".","theres","something"], 10, lower_corpus, False)
    sentence = finish_sentence(["robot"], 10, lower_corpus, True)
    print(sentence)
