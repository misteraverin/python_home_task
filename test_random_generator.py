from errors import ValidationError, InvalidProbabilitiesError
from random_generator import RandomGen
import unittest
import random
from collections import Counter


class TestRandomGenInputConditions(unittest.TestCase):
    def _setup_random_gen(
            self, random_nums: list[int], probabilities: list[float],
    ):
        self._random_generator = RandomGen(random_nums, probabilities, )

    def _assert_raise_error(
            self,
            probabilities: list[float],
            random_nums: list[int],
            error: ValidationError,
            code: int,
    ) -> None:
        with self.assertRaises(error) as context:
            self._setup_random_gen(probabilities, random_nums)
            self.assertEqual(context.exception.code, code)

    def test_catch_exception_if_negative_probabilities(self):
        self._assert_raise_error(
            probabilities=[0.5, -0.4],
            random_nums=[2, 3],
            error=InvalidProbabilitiesError,
            code=1,
        )

    def test_catch_exception_if_length_mismatched(self):
        self._assert_raise_error(
            probabilities=[0.5, 0.1, 0.4],
            random_nums=[2, 3],
            error=InvalidProbabilitiesError,
            code=2,
        )

    def test_catch_exception_if_probabilities_sum_is_not_one(self):
        self._assert_raise_error(
            probabilities=[0.5, 0.1, 0.7],
            random_nums=[2, 3, 6],
            error=InvalidProbabilitiesError,
            code=3,
        )


class TestRandomGenHelpFunctions(unittest.TestCase):
    def test_cumulative_sum(self):
        random_generator = RandomGen([1, 2, 5], [0.1, 0.4, 0.5])
        assert [0.1, 0.5, 1.0] == random_generator._cumulative_sum([0.1, 0.4, 0.5])

    def test_search_index_greater_than_number(self):
        random_generator = RandomGen([1, 2, 5], [0.1, 0.4, 0.5])
        cumulative_sum = random_generator._cumulative_sum([0.1, 0.4, 0.5])
        assert random_generator._search_index_greater_than_number(cumulative_sum, 0.4) == 1


class TestRandomGen(unittest.TestCase):
    def test_next_num(self):
        random.seed(167345)  # We fix that for deterministic tests results
        number_of_calls = 1000
        numbers = [1, 2, 3, 4, 5]
        probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
        expected_results = {3: 581, 2: 290, 4: 107, 5: 11, 1: 11}
        generator = RandomGen(numbers, probabilities)

        counter_results = Counter()
        for attempt in range(number_of_calls):
            current_value = generator.next_num()
            counter_results[current_value] += 1

        self.assertDictEqual(expected_results, counter_results)


if __name__ == "__main__":
    unittest.main()
