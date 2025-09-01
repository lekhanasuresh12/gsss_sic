from partition1 import partition_array as pa

def quick_sort(array,low,high):
    if high > low:
        pivot_index = pa(array, low, high)
        quick_sort(array, low, pivot_index-1)
        quick_sort(array, pivot_index +1, high)


l1=[34,223,22,31,1,100,50,40,22,72]
print(f'before sorting: {l1}')
quick_sort(l1, 0, len(11)-1)
print(f'after sorting: {11}')

            

