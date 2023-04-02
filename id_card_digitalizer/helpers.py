THRESHOLD = 40

# def find_max_y(items):
#     max_y_item = items[0]
#
#     for item in items:
#         if item.top_left[1] > max_y_item.top_left[1]:
#             max_y_item = item
#
#     # print(max_y_item.__str__())
#     return max_y_item.top_left[1]


# def find_min_x(items):
#     min_x_item = items[0]
#
#     for item in items:
#         if item.top_left[0] < min_x_item.top_left[0]:
#             min_x_item = item
#
#     # print(min_x_item.__str__())
#     return min_x_item.top_left[0]


# def find_max_x(items):
#     max_x_item = items[0]
#
#     for item in items:
#         if item.top_left[0] > max_x_item.top_left[0]:
#             max_x_item = item
#
#     # print(max_x_item.__str__())
#     return max_x_item.top_left[0]

def print_card_text_items(card_text_items):
    for cti in card_text_items:
        print(cti.__str__())
        print("/-------/\n")

def find_next_key(items):
    next_key = next(item for item in items if item.is_examined == 0)

    for item in items:
        if item.is_examined == 0:
            if item.top_left[1] < next_key.top_left[1]:
                next_key = item
    # print("/-- key found by Y coordinate: --/\n")
    # print(next_key)
    # print("\n")
    upper_bound = next_key.top_left[1] + THRESHOLD
    lower_bound = next_key.top_left[1] - THRESHOLD

    for item in items:
        if item.is_examined == 0:
            if(lower_bound <= item.top_left[1] <= upper_bound) and item.top_left[0] < next_key.top_left[0]:
                # print("/-- found a new key within threshold --/\n")
                next_key = item

    print(f"/-- Found next key: {next_key.text} --/\n")
    return next_key


def find_key_value_pairs(items):
    i = 0
    while any(item.is_examined == 0 for item in items):
        next_key = find_next_key(items)
        find_value_for_key(next_key, items)


def find_value_for_key(key, items):
    if key.is_examined == 0 and key.assigned_to == 0:
        key.is_examined = 1
        item_right = search_right(key, items)

        if item_right is not None:
            print("/-- closest item on right: --/\n")
            print(item_right)
            print("\n")

            key.is_key = 1
            item_right.is_value = 1
            item_right.is_examined = 1
            item_right.assigned_to = key
            key.assigned_to = item_right

        else:
            item_below = search_below(key, items)

            if item_below is not None:
                print("/-- closest item below: --/\n")
                print(item_below)
                print("\n")

                key.is_key = 1
                item_below.is_value = 1
                item_below.is_examined = 1
                item_below.assigned_to = key
                key.assigned_to = item_below
    else:
        print("/-- no value pair found --/\n")
        return None


def search_right(key, items):
    found_items = list()
    upper_bound = key.top_left[1] + THRESHOLD
    lower_bound = key.top_left[1] - THRESHOLD

    for item in items:
        if item.is_examined == 0 and item.assigned_to == 0:
            if (lower_bound <= item.top_left[1] <= upper_bound) and item.top_left[0] > key.top_left[0]:
                found_items.append(item)
                # print("/-- found item on right: --/\n")
                # print(item)
                # print("\n")

    if found_items:
        if len(found_items) == 1:
            return found_items[0]
        else:
            return get_closest_item_right(found_items, key)
    else:
        print("/-- search_right found no items /-- \n")
        return None


def get_closest_item_right(found_items, text_item):
    closest_item_right = found_items[0]

    for item in found_items:
        if item.top_left[0] <= closest_item_right.top_left[0]:
            closest_item_right = item

    return closest_item_right


def search_below(key, items):
    found_items = list()
    upper_bound = key.top_left[0] + THRESHOLD
    lower_bound = key.top_left[0] - THRESHOLD

    for item in items:
        if item.is_examined == 0 and item.assigned_to == 0:
            if (lower_bound <= item.top_left[0] <= upper_bound) and item.top_left[1] > key.top_left[1]:
                found_items.append(item)
                # print("/-- found item below: --/\n")
                # print(item)
                # print("\n")

    if found_items:
        if len(found_items) == 1:
            return found_items[0]
        else:
            return get_closest_item_below(found_items, key)
    else:
        print("/-- search_below found no items /--\n")
        return None


def get_closest_item_below(found_items, text_item):
    closest_item_below = found_items[0]

    for item in found_items:
        if item.top_left[1] <= closest_item_below.top_left[1]:
            closest_item_below = item

    return closest_item_below

