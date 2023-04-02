import helpers


def key_find_test(items):
    print("/-- running key_find_test --/\n")
    items_copy = list()

    for item in items:
        if item.text == "Nationality:" or item.text == "HUN":
            items_copy.append(item)

    helpers.find_next_key(items_copy)


def right_search_test(items):
    print("/-- running right_search_test on: --/\n")
    print(items[3])
    helpers.find_value_for_key(items[3], items)


def below_search_test(items):
    print("/-- running below_search_test on: --/\n")
    print(items[1])
    helpers.find_value_for_key(items[1], items)


def no_pair_test(items):
    print("/-- running no_pair_test on: --/\n")
    print(items[0])
    helpers.find_value_for_key(items[0], items)

