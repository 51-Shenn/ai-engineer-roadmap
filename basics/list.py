lst = [1, 2, 3, 4]
cp_list = []

number = 5
index = 1

lst.append(5) # add item to the end of the list
lst.insert(index, number) # insert 5 at index 1
print(f"\nInserted {number} at index {index}: " + str(lst))

lst.remove(number) # remove the first occurence of 5
print(f"Removed the first occurence of {number}: " + str(lst))

index = 2
lst.pop(index) # remove list element at index [2]
print(f"Popped element at index {index}: " + str(lst))

lst.reverse() # reverse the list
print("Reversed: " + str(lst))

cp_list.extend(lst)
print("Extended (cp_list value): " + str(cp_list))

lst.sort() # sort the list
print("Sorted: " + str(lst))

lst.clear()
print("Cleared: " + str(lst) + "\n")

print(f"Length of lst: {len(lst)}")
print(f"Length of cp_list: {len(cp_list)}\n")
