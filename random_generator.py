from __future__ import division
import bisect
import random
from errors import InvalidProbabilitiesError


class RandomGen:
    def __init__(self, random_nums, probabilities):
        """
        Initialise the random number generator with a set of allowed numbers,
        and probabilities for each number to occur.
        """
        self._random_nums = random_nums
        self._probabilities = probabilities
        self._validate_params()
        self._cumulative_probabilities = self._cumulative_sum(probabilities)

    def next_num(self):
        random_value = random.random()
        index_of_number = self._search_index_greater_than_number(
            self._cumulative_probabilities, random_value
        )
        return self._random_nums[index_of_number]

    def _validate_params(self) -> None:
        self._check_probabilities_length()
        self._check_probabilities_sum()
        self._check_negative_probabilities()

    def _check_probabilities_length(self) -> None:
        if len(self._random_nums) != len(self._probabilities):
            raise InvalidProbabilitiesError(
                f"Length of probabilities {len(self._random_nums)} != Length of random nums {len(self._random_nums)}"
            )

    def _check_probabilities_sum(self) -> None:
        sum_probabilities = sum(self._probabilities)
        if abs(sum_probabilities - 1.0) > 1e-10:
            raise InvalidProbabilitiesError(
                f"Probabilities sum is {sum_probabilities}, should be 1.0"
            )

    def _check_negative_probabilities(self) -> None:
        if any(x < 0.0 for x in self._probabilities):
            raise InvalidProbabilitiesError(
                f"Negative probabilities {self._probabilities}"
            )

    @staticmethod
    def _cumulative_sum(values: list[float]) -> list[float]:
        cumulative_values, current_value = [], 0.0

        for value in values:
            current_value += value
            cumulative_values.append(current_value)

        return cumulative_values

    @staticmethod
    def _search_index_greater_than_number(values, number):
        """
        It performs binary-search in sorted array for finding element
        """
        index = bisect.bisect_right(values, number)

        if index != len(values):
            return index
        else:
            raise ValueError(f"Cannot find valid index for {number} in {values}")
