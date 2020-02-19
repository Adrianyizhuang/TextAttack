"""
    Gao, Lanchantin, Soffa, Qi.
    
    Black-box Generation of Adversarial Text Sequences to Evade Deep Learning 
        Classifiers.
    
    ArXiv, abs/1801.04354.
    
"""

from textattack.attack_methods import GreedyWordSwapWIR
from textattack.constraints.overlap import LevenshteinEditDistance
from textattack.transformations import \
    CompositeTransformation, WordSwapNeighboringCharacterSwap, \
    WordSwapRandomCharacterDeletion, WordSwapRandomCharacterInsertion, \
    WordSwapRandomCharacterSubstitution, WordSwapNeighboringCharacterSwap

def Gao2018DeepWordBug(model, use_all_transformations=True):
    #
    # Swap characters out from words. Choose the best of four potential transformations. 
    #
    if use_all_transformations:
        # We propose four similar methods:
        transformation = CompositeTransformation([
            # (1) Swap: Swap two adjacent letters in the word.
            WordSwapNeighboringCharacterSwap(),
            # (2) Substitution: Substitute a letter in the word with a random letter.
            WordSwapRandomCharacterSubstitution(),
            # (3) Deletion: Delete a random letter from the word.
            WordSwapRandomCharacterDeletion(),
            # (4) Insertion: Insert a random letter in the word.
            WordSwapRandomCharacterInsertion()
        ])
    else: 
        # We use the Combined Score and the Substitution Transformer to generate 
        # adversarial samples, with the maximum edit distance difference of 30 
        # (ϵ = 30).
        transformation = WordSwapRandomCharacterSubstitution()
    #
    # In these experiments, we hold the maximum difference
    # on edit distance (ϵ) to a constant 30 for each sample.
    #
    constraints = [
        LevenshteinEditDistance(30)
    ]
    #
    # Greedily swap words with "Word Importance Ranking".
    #
    attack = GreedyWordSwapWIR(model, transformation=transformation,
        constraints=[], max_depth=None)
    
    return attack