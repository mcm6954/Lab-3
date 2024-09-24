"""
CSAPX Lab 3: Tripods

Implementation of a combination sort method.
Uses merge sort for lists with at least eight elements, and insertion sort for lists
smaller than eight elements, including any such lists within the merge sort recursion.

Author: Mia McSwain
Instructor: Sean Strout
"""
from tripods import Tripod

def insertion_sort(data: list[Tripod]) -> None:
    """
    Perform an in-place insertion sort of data
    :param data: The data to be sorted (a list)
    """
    for mark in range(1, len(data)):
        j = mark
        while j > 0 and data[j-1].total > data[j].total:
            data[j], data[j-1] = data[j-1], data[j]
            j -= 1

def _split(data: list[Tripod]) -> tuple[list[Tripod], list[Tripod]]:
    """
    Split the data into halves and return the two halves
    :param data: The list to split in half
    :return: Two lists, cut in half
    """
    return data[:len(data)//2], data[len(data)//2:]

def _merge(left: list[Tripod], right: list[Tripod]) -> list[Tripod]:
    """
    Merges two sorted list, left and right, into a combined sorted result
    :param left: A sorted list
    :param right: A sorted list
    :return: One combined sorted list
    """
    # the sorted left + right will be stored in result
    result = []
    left_index, right_index = 0, 0

    # loop through until either the left or right list is exhausted
    while left_index < len(left) and right_index < len(right):
        if left[left_index].total <= right[right_index].total:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    # take the un-exhausted list and extend the remainder onto the result
    if left_index < len(left):
        result.extend(left[left_index:])
    elif right_index < len(right):
        result.extend(right[right_index:])

    return result

def combi_sort(data: list[Tripod]) -> list:
   """
   Sorts data using insertion or merge sort depending of the length of the data
   :param data: The data to be sorted (a list)
   :return: Returns the sorted list
   """""
   if len(data) < 8:
        insertion_sort(data)
        return data
   else:
       left, right = _split(data)
       return _merge(combi_sort(left), combi_sort(right))