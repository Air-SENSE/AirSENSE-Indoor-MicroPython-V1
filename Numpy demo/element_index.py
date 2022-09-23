import numpy as np

arr = np.array([1,3,4,5,6], dtype = int)
arr1 = np.array([(4,5,6), (1,2,3)], dtype = int)
arr2 = np.array(([(2,4,0,6), (4,7,5,6)],
                 [(0,3,2,1), (9,4,5,6)],
                 [(5,8,6,4), (1,4,6,8)]), dtype = int)

#Get the Third element from the following array.
print("arr[2]=", arr[2])
#Get the element from the following array at second list and third axits.
print("arr1[1:2]=", arr1[1,2])
#Get the elements from first to fourth element from arr
print("arr[0:3]=", arr[0:3])
#Get the element from the following array at (2,2,4) from 3-D Array.
print("arr2[1,2,3]=", arr2[1,1,3])
#Get all the element from all lists and from end of each list (:) to second element
print("arr1[:,:1]=", arr1[:,:2])