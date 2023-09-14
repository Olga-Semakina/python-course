"""
Given an array of size n, find the most common and the least common elements.
The most common element is the element that appears more than n // 2 times.
The least common element is the element that appears fewer than other.

You may assume that the array is non-empty and the most common element
always exist in the array.

Example 1:

Input: [3,2,3]
Output: 3, 2

Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2, 1

"""
from typing import List, Tuple


def major_and_minor_elem(list):
    # create a dictionary to get only unique values
    dictionary = dict.fromkeys(list, 0)

    # set number of occurrences in the list
    for value, _ in dictionary.items():
        count = list.count(value)
        dictionary.update({value: count})

    # find the least common number
    least_common = min(dictionary, key=dictionary.get)

    most_common = list[0]
    list_size = len(list)
    # find the most common number
    for value, count in dictionary.items():
        if (count > list_size // 2):
            most_common = value
            break

    return (most_common, least_common)
