import re

def define_ngram(corpus: list):
    trigram_dict = {}
    bigram_dict = {}
    unigram_dict = {}
    vocab = []

    for i in range(len(corpus) - 2):
        trigram = (corpus[i], corpus[i+1], corpus[i+2])
        if trigram in trigram_dict.keys():
            #trigram_dict[trigram]['count'] += 1
            trigram_dict[trigram] += 1
        else:
            #trigram_dict[trigram] = {}
            #trigram_dict[trigram]['count'] = 1
            #trigram_dict[trigram]['index'] = i
            trigram_dict[trigram] = 1


    for i in range(len(corpus) - 1):
        bigram = (corpus[i], corpus[i+1])
        if bigram in bigram_dict.keys():
            #bigram_dict[bigram]['count'] += 1
            bigram_dict[bigram] += 1
        else:
            #bigram_dict[bigram] = {}
            #bigram_dict[bigram]['count'] = 1
            #bigram_dict[bigram]['index'] = i
            bigram_dict[bigram] = 1
    
    for i in range(len(corpus)):
        unigram = corpus[i]
        if unigram in unigram_dict.keys():
            #unigram_dict[unigram]['count'] += 1
            unigram_dict[unigram] += 1
        else:
            #unigram_dict[unigram] = {}
            #unigram_dict[unigram]['count'] = 1
            #unigram_dict[unigram]['index'] = i
            unigram_dict[unigram] = 1
            vocab.append(unigram)

    print(unigram_dict)

    return trigram_dict, bigram_dict, unigram_dict, vocab


def finish_sentence(sentence: list, n: int, corpus: list, randomize=False):
    trigram_dict, bigram_dict, unigram_dict, vocab = define_ngram(corpus)
    corpus_length = len(corpus)
    current_history = {
        '3': {'input' : tuple(sentence[-2:]), 'testgramdict' : trigram_dict, 'lowergramdict' : bigram_dict},
        '2': {'input' : str(sentence[-1]), 'testgramdict' : bigram_dict, 'lowergramdict' : unigram_dict},
        '1': {'testgramdict': unigram_dict}
    }

    next_word = find_sequence(current_history, n, vocab, corpus_length, randomize)
    if len(next_word) > 1:
        current_best_index = None
        for word in next_word:
            sequence = list(current_history[str(n)]['input'])+[word]
            print(sequence)
            for i in range(len(corpus) - (n-1)):
                test_seq = corpus[i:i+n]
                if (test_seq == sequence) & (current_best_index == None):
                    current_best_index = i
                    next_word = word
                elif test_seq == sequence:
                    if i < current_best_index:
                        current_best_index = i
                        next_word = word 
                    else:
                        continue

    print(f'The next best word is {next_word}')
    sentence.append(next_word)
    if (len(sentence)==10) | (sentence[-1]== "."):
        return sentence
    else:
        finish_sentence(sentence=sentence, n=3, corpus=corpus, randomize=False)
                    
    #for word in vocab:
    #    test_trigram = (input[0], input[1], word)
    #    test_bigram = (input[0], input[1])
    #    if bigram_count == 0:
    #        print("go to unigram")
    #    trigram_count = trigram_dict.get(test_trigram, 0)
    #    bigram_count = bigram_dict.get(test_bigram, 0)
    #    score = trigram_count / bigram_count
    #    word_probabilities[word] = score


def find_sequence(current_history: dict, n:int, vocab, corpus_length, randomize):
    while n > 0:
        print(n)
        if n == 0:
            return "Fuck why is n 0"
        word_scores = {}
        if n > 1:
            lower_gram = current_history[str(n)]['input']
            print(lower_gram)
            print(current_history[str(n)]['lowergramdict'].get(lower_gram, 0))
            if current_history[str(n)]['lowergramdict'].get(lower_gram, 0) == 0:
                print("Need Lower N-Gram Up Here")
                n-=1
                continue

        for word in vocab:
            if n > 1:
                print(f'evaluating word: {word}')
                test_gram = tuple(list(current_history[str(n)]['input']) + [word])
                lower_gram = tuple(current_history[str(n)]['input'])
                test_gram_count = current_history[str(n)]['testgramdict'].get(test_gram, 0)
                lower_gram_count = current_history[str(n)]['lowergramdict'].get(lower_gram, 0)
                word_scores[word] = test_gram_count / lower_gram_count
            elif n == 1:
                word_scores[word] = current_history[str(n)][word]['count'] / corpus_length

        if any(value > 0 for value in word_scores.values()):
            print('next word has been identified')
            highest_score = max(word_scores.values())
            best_words = []
            for key, value in word_scores.items():
                if value == highest_score:
                    best_words.append(key)
            return best_words
                #first_word = best_words[0]
                #for word in best_words:
                #    current_best_index = current_history[str(n)]['testgramdict'][first_word]['index']
                #    new_index = current_history[str(n)]['testgramdict'][word]['index']
                #    if new_index < current_best_index:
                #        first_word = word
        else:
            n-=1
            print("Need Lower N-Gram Down Here")
        n-=1
        #print(test_gram)
        #print(lower_gram)
        #print(test_gram_count)
        #print(lower_gram_count)

    
            


if __name__ == "__main__":
    corpus = "Babe. Theres something tragic about you. Something so magic about you, dont you agree? Babe. Theres something lonesome about you. Something so wholesome about you, get closer to me."
    # Use regular expression to split by spaces or punctuation
    split_tokens = re.findall(r'\w+|[.,!?]|[\'`]\w+|\w+[\'`]\w+', corpus)
    

    # Remove empty strings from the result
    split_tokens = [token for token in split_tokens if token]
    lower_corpus = [w.lower() for w in split_tokens]
    #define_ngram(lower_corpus)
    sentence = finish_sentence([".", "theres", "something"], 3, lower_corpus, False)
    print(sentence)