import numpy as np 
#Question 8
D_ij = np.matrix ([[1,0,0,0,0],
       [0,4,0,0,0],
       [0,0,2,0,0],
       [0,0,0,1,0],
       [0,0,0,0,2]])
  
A_ij = np.matrix ([[0,1,0,0,0],
       [1,0,1,1,1],
       [0,1,0,0,1],
       [0,1,0,0,0],
       [0,1,1,0,0]])
print('Using the adjacency matrix: L=D_ij-A_ij')
print(np.subtract(D_ij, A_ij))
print('Using the incidance matrix: L=K*K_Transpose')
K = np.matrix ([[1,0,0,0,0],
       [-1,1,1,1,0],
       [0,-1,0,0,1],
       [0,0,-1,0,0],
       [0,0,0,-1,-1]])
K_T=K.getT()
print(np.dot(K, K_T))