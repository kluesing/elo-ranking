elo-ranking
===========

ComparisonItem
Implements a modified Elo ranking system. The two key attributes are ranking_score and k exponent. A higher ranking_score means the item is better (and should have lower rank). A higher k means we're less sure about the ranking of this item and the item should make larger adjustments to its ranking_score. Each time a comparison is made, the value of the k exponent is decreased on that particular item. This has the functional effect of reducing the magnitude of changes in ranking scores as more comparisons are made against that item. (Big movements in the beginning, more refined movement over time)

ComparisonTestItem
Subclasses the ComparisonItem adding a true_rank attribute representing an oracle's knowledge of where this item should be ranked. 1 is the best rank. Also adds a NosiyVote class method which allows us to model a subjective human comparer. The NosiyVote will correctly compare two items 95% of the time, and rate the wrong item better 5% of the time. This represents an environment where human raters with subjective/different/error prone preferences are comparing items.
