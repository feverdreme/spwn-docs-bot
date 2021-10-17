import Levenshtein
from enum import Enum, auto
from functools import reduce
from src.Entry import Entry

class Ordering(Enum):
    ALPHABETIC = auto()
    DISTANCE = auto()


class Searcher:
    def __init__(self, *searchlist) -> None:
        self.searchlist = reduce(lambda a, b: a + b, searchlist)

    def search_for(self, search_term: str, max_distance: int = 3, order_by: Ordering = Ordering.ALPHABETIC) -> list[Entry]:
        result = [
            (entry, Levenshtein.distance(search_term, entry.title))
            for entry in self.searchlist
        ]
        result = filter(
            lambda entry_pair:
                entry_pair[1] <= max_distance,
            result
        )
        result = map(
            lambda entry_pair:
                entry_pair[0].with_attr("ldistance", entry_pair[1]),
            result
        )
        result: list[Entry] = list(result)

        match order_by:
            case Ordering.ALPHABETIC:
                result.sort(key=lambda entry: entry.title)

            case Ordering.DISTANCE:
                result.sort(key=lambda entry: entry.ldistance)
        
        # remove the distance attribute
        return result
