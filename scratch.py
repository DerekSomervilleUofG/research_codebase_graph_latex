def bubble_sort(numbers):
    is_sorted = False
    counter = 1
    index = len(numbers) - 1
    inner_index = 0
    while index >= 1 and not is_sorted:
        is_sorted = True
        for inner_index in range(index):
            if numbers[inner_index] > numbers[inner_index + 1]:
                numbers[inner_index], numbers[inner_index + 1] = \
                    numbers[inner_index + 1], numbers[inner_index]
                is_sorted = False
        counter += 1
    print(counter)
    return numbers
print(bubble_sort([7,3,5,2,4]))