import math
import random
from operator import attrgetter
from itertools import izip 

class ComparisonItem(object):
  """
  Implements a modified Elo ranking for pair-wise comparisons
  """
  def __init__(self, description):
    """
    description is the human readable 'thing' represented by this object.
    """
    self.description = description
    self.ranking_score = 1600.
    self.k = 32.
    self.num_comparisons = 0
  
  def win_probability(self, opponent):
    """
    What's the probability of me winning against this opponent - a ComparisonItem
    Assumes a normal distribution of opponents
    """
    exponent = (opponent.ranking_score - self.ranking_score)/400.
    expected_score = 1. / (1. + math.pow(10., exponent))
    return expected_score

  def record_matchup(self, opponent, actual_score):
    """
    update my ranking based on performance against an opponent, and also update the opponent
    first compute an expected score based on my ranking and the opponent's ranking
    compare the expected score to the actual score, and update rankings on by myself and opponent
    opponent is a ComparisonItem
    actual_score is either 1 (meaning this object was chosen) or 0 (meaning this object was not chosen)
    both this object and the opponent object are updated, it is incorrect to run record_matchup on both objects
    """
    expected_score = self.win_probability(opponent)
    expected_opp_score = opponent.win_probability(self)

    actual_score_opp = 0
    if(actual_score==0): actual_score_opp = 1

    self._update_ranking(actual_score, expected_score)
    opponent._update_ranking(actual_score_opp, expected_opp_score)

  def _update_ranking(self, actual_score, expected_score):
    """
    move the ranking closer to the ranking suggested by a matchup
    actual_score is 1 or 0
    expected_score is a float produced by win_probability
    """
    self.ranking_score = self.ranking_score + (self.k * (actual_score - expected_score))
    self.num_comparisons+=1
    if(self.k>1): self.k-=0.01

  def __repr__(self):
    return self.description 


class ComparisonTestItem(ComparisonItem):
  """
  Extends the basic ComparisionObject with a true rank attribute and a test voting function
  Allows running a simulation and computing RMSE/other error metrics
  """
  def __init__(self, description, true_rank):
    """
    description is a human readable string describing this thing
    true_rank is the true global ranking of this object against all others. 1 is the best in the whole-wide-world
    """
    ComparisonItem.__init__(self, description)
    self.true_rank = true_rank
  
  @staticmethod
  def NoisyVote(obj1, obj2):
    """
    A noisy vote mechanism which rolls a die and correctly votes most of the time. 
    This is intended to simulate human feedback on items where the judgment of 'best' may be subjective
    or some voters may be lazy/malicious/wrong
    """
    if(random.random()<0.95):
      # update the rankings with truthful data
      if(obj1.true_rank < obj2.true_rank):
        obj1.record_matchup(obj2, 1)
      else:
        obj1.record_matchup(obj2, 0)
    else:
      # update the rankings with false data
      if(obj1.true_rank < obj2.true_rank):
        obj1.record_matchup(obj2, 0)
      else:
        obj1.record_matchup(obj2, 1)
        


