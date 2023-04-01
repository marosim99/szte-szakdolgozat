import numbers

THRESHOLD = 40


def find_min_y(items):
    min_y_item = items[0]

    for item in items:

        if item.top_left[1] < min_y_item.top_left[1]:
            min_y_item = item

        elif item.top_left[1] == min_y_item.top_left[1]:
            if item.top_left[0] < min_y_item.top_left[0]:
                min_y_item = item

    print(f"Found minimum y: {min_y_item.__str__()}")
    return min_y_item


def find_max_y(items):
    max_y_item = items[0]

    for item in items:
        if item.top_left[1] > max_y_item.top_left[1]:
            max_y_item = item

    # print(max_y_item.__str__())
    return max_y_item.top_left[1]


def find_min_x(items):
    min_x_item = items[0]

    for item in items:
        if item.top_left[0] < min_x_item.top_left[0]:
            min_x_item = item

    # print(min_x_item.__str__())
    return min_x_item.top_left[0]


def find_max_x(items):
    max_x_item = items[0]

    for item in items:
        if item.top_left[0] > max_x_item.top_left[0]:
            max_x_item = item

    # print(max_x_item.__str__())
    return max_x_item.top_left[0]


def find_pair(text_item, items):
    if text_item.is_examined == 0 and text_item.assigned_to == 0:
        text_item.is_examined = 1
        item_right = search_right(text_item, items)

        if item_right is not None:
            print("closest item on right:")
            print(item_right)

            text_item.is_key = 1
            item_right.is_value = 1
            item_right.is_examined = 1

            item_right.assigned_to = text_item
            text_item.assigned_to = item_right
            # return item_right
        else:
            print("no item found on right")
            # return None
    # else:
        # return None


def search_right(text_item, items):
    found_items = list()
    upper_bound = text_item.top_left[1] + THRESHOLD
    lower_bound = text_item.top_left[1] - THRESHOLD

    for item in items:
        if item.is_examined == 0 and item.assigned_to == 0 and (lower_bound <= item.top_left[1] <= upper_bound) and item.top_left[0] > text_item.top_left[0]:
            found_items.append(item)
            print("found item!")
            print(item.__str__())

    if found_items:
        if len(found_items) == 1:
            return found_items[0]
        else:
            return get_closest_item_right(found_items, text_item)
    else:
        print("empty")
        return None


def get_closest_item_right(found_items, text_item):
    closest_item_y = found_items[0]

    for item in found_items:
        if item.top_left[1] < closest_item_y.top_left[1]:
            closest_item_y = item

    return closest_item_y

