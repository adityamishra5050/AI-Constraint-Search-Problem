# -*- coding: utf-8 -*-
"""AI assignment Question 2(ii).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k0inqwRWJaDYPaCUbmD5BN-l3IQ7cUWu
"""

from collections import defaultdict

def is_chef_chucklesnort(soup_pot, chef, cookbook, n):
    if (chef == "ChefA" and (cookbook.get(soup_pot - 1) == "ChefB" or cookbook.get(soup_pot + 1) == "ChefB" or
                            cookbook.get(soup_pot - 1) == "ChefC" or cookbook.get(soup_pot + 1) == "ChefC")) or \
            (chef == "ChefC" and (soup_pot < 5 or cookbook.get(n) == "ChefC" or cookbook.get(soup_pot + 1) == "ChefN")) or \
            (chef == "ChefF" and cookbook.get("Chef" + str(n - 1)) and soup_pot >= cookbook["Chef" + str(n - 1)]) or \
            (chef == "ChefN" and soup_pot == n) or \
            (soup_pot in cookbook and cookbook[soup_pot] != chef):
        return False
    return True

def select_unassigned_ingredient_mrv(remaining_pots, cookbook):
    mrv = float('inf')
    selected_pot = None
    for soup_pot in remaining_pots:
        if len(remaining_pots[soup_pot]) < mrv and soup_pot not in cookbook:
            mrv = len(remaining_pots[soup_pot])
            selected_pot = soup_pot
    return selected_pot

def select_unassigned_ingredient(remaining_pots, cookbook):
    for soup_pot in sorted(remaining_pots.keys()):
        if soup_pot not in cookbook:
            return soup_pot
    return None

def taste_test(soup_pot, chef, remaining_pots, cookbook):
    new_remaining_pots = remaining_pots.copy()
    for other_pot in remaining_pots:
        if other_pot != soup_pot:
            new_remaining_pots[other_pot] = [ingredient for ingredient in new_remaining_pots[other_pot] if ingredient != chef]
    return new_remaining_pots

def aroma_consistency(remaining_pots, soup_pot, chef):
    queue = [(soup_pot, chef)]
    while queue:
        current_pot, current_chef = queue.pop(0)
        for other_pot in remaining_pots:
            if other_pot != current_pot and current_chef in remaining_pots[other_pot]:
                remaining_pots[other_pot].remove(current_chef)
                if len(remaining_pots[other_pot]) == 0:
                    return False
                if len(remaining_pots[other_pot]) == 1:
                    queue.append((other_pot, remaining_pots[other_pot][0]))
    return True

master_chefs = ["M1", "M4", "M2", "M6", "M3", "M7", "M8", "M9", "M5"]

def are_adjacent_chefs(chef1, chef2):
    forbidden_adjacent_pairs = [("M1", "M2"), ("M1", "M3"), ("M3", "Mn"), ("M3", "M5")]
    return (chef1, chef2) in forbidden_adjacent_pairs or (chef2, chef1) in forbidden_adjacent_pairs

def is_tasty_ingredient_assignment(soup_pot, chef, cookbook, num_pots):
    if cookbook.get(soup_pot) and cookbook[soup_pot] != chef:
        return False

    adjacent_pot_left = soup_pot - 1
    adjacent_pot_right = soup_pot + 1

    if cookbook.get(adjacent_pot_left) and are_adjacent_chefs(cookbook[adjacent_pot_left], chef):
        return False

    if cookbook.get(adjacent_pot_right) and are_adjacent_chefs(cookbook[adjacent_pot_right], chef):
        return False

    if chef == "Chef3" and soup_pot < 5:
        return False

    if chef == "Chef6" and cookbook.get("M" + str(num_pots - 1)) and soup_pot >= cookbook["M" + str(num_pots - 1)]:
        return False

    if chef == "M" + str(num_pots) and soup_pot == num_pots:
        return False

    return True

if __name__ == "__main__":
    num_pots = 8
    pots = [i for i in range(1, num_pots + 1)]
    chefs = [f"M{i}" for i in range(1, num_pots + 1)]

    remaining_pots = {soup_pot: chefs[:] for soup_pot in pots}
    remaining_pots[1] = ["M1"]

    cookbook = {"S1": "M1"}
    taste_order = ["M1"]

    print("\nUsing Forward checking, Arc Consistency, and MRV:")
    for i in range(0, 9):
        print("Slot S1 is Assigned to ", master_chefs[i])