import numpy as np 
#Question 9
a = np.array([[4,-1,-1,-1], [-1,2,0,-1], [-1,0,1,0],[-1,-1,0,2]])
b = np.array([ 500, 600, -800, -100])

x = np.linalg.solve(a, b)
print(x)