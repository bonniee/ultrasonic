import nltk
import numpy as np

def get_probabilities(corpus, alpha="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    corpus = ''.join([c for c in corpus if c in alpha])
    counts = [corpus.count(c) for c in alpha]
    start_probs = np.array(counts, dtype=float) / sum(counts)
    trans_counts = [[0.1 + corpus.count("%s%s" % (a,b)) for b in alpha] for a in alpha]
    trans_probs = np.array([np.array(x, dtype=float)/sum(x) for x in trans_counts])
    return (start_probs, trans_probs)

start_probs, trans_probs = get_probabilities("THISSHOULDBEAHUGESTRINGLIKETHISBUTHUNDREDSOFTIMESBIGGER")

class Viterbi():
    def __init__(self, start_probs, trans_probs):
        self.trans_probs = np.array(trans_probs)
        
        # viterbi [t,i] is [probability of being at state i at time t | observations up to t, most likely previous state]
        # -1 indicates no previous state
        # t=1 indicates the first observation; t=0 indicates start probabilities
        self.viterbi = [[[x,-1] for x in start_probs]]
    
    # obs_probs = [list of things that sum to 1]
    def observe(self, obs_probs):
        # obs_props[i] == P(i|obs)
        next_probs = [[0,-1]] * len(self.viterbi[-1])
        
        for i, (prob_at, _) in enumerate(self.viterbi[-1]):
            for j, prob_to in enumerate(self.trans_probs[i,:]):
                next_prob = prob_at * prob_to * obs_probs[j]
                if next_prob > next_probs[j][0]:
                    next_probs[j] = [next_prob, i]
                    
        # normalize
        total = sum(x[0] for x in next_probs)
        next_probs = [[i/total, j] for (i,j) in next_probs]
        
        self.viterbi.append(next_probs)
        
    def best_path(self):
        path = []
        
        # Find the most recent node of the best path
        count = -1 + len(self.viterbi)
        i = np.argmax([p for (p,prev) in self.viterbi[count]])  # index of class
        (prob, prev) = self.viterbi[count][i]
        
        while prev != -1:
            count -= 1
            path = [clf.classifier.classes_[i]] + path
            
            i = prev
            (prob, prev) = self.viterbi[count][i]
        
        return path