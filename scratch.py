import math

def round_to_x_minus_1_digits_nearest_5(num):
    x = len(str(abs(int(num)))) if num != 0 else 1  # ensure x≥1 even for 0
    step = 5 * 10**(x - 2)
    return math.ceil(num / step) * step


print(round_to_x_minus_1_digits_nearest_5(4))
print(round_to_x_minus_1_digits_nearest_5(147))

print(round_to_x_minus_1_digits_nearest_5(1147))