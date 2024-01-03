numbers = []

for i in range(1,21):
    numbers.append(i)


double_evens = [x * 2 for x in numbers if x%2 == 0 and x >=10]

print(double_evens)


######################################################
# LAMBDA
######################################################

roo = lambda x: x**3

divide = lambda x: x/2

print(roo(3))

cubed = [roo(x) for x in numbers]

print(cubed)