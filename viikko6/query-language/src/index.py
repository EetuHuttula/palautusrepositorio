from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, HasFewerThan, Not, Or, PlaysIn, All

class QueryBuilder:
    def __init__(self):
        self._matcher = All()

    def plays_in(self, team):
        self._matcher = And(self._matcher, PlaysIn(team))
        return self
    
    def one_of(self, *matchers):
        built = [m.build() if hasattr(m, "build") else m for m in matchers]
        self._matcher = Or(*built)
        return self

    def has_at_least(self, value, attr):
        self._matcher = And(self._matcher, HasAtLeast(value, attr))
        return self

    def has_fewer_than(self, value, attr):
        self._matcher = And(self._matcher, HasFewerThan(value, attr))
        return self

    def Or(self):
        self._matcher = Or(self._matcher)
        return self

    def Not(self):
        self._matcher = Not(self._matcher)
        return self
    
    def build(self):
        return self._matcher

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)
    
    matcher = (
        QueryBuilder()
        .one_of(
            QueryBuilder()
            .plays_in("PHI")
            .has_at_least(10, "assists")
            .has_fewer_than(10, "goals"),
            QueryBuilder()
            .plays_in("EDM")
            .has_at_least(50, "points"),
        )
        .build()
    )


    for player in stats.matches(matcher):
        print(player)

    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all))

if __name__ == "__main__":
    main()
