import numpy as np
import matplotlib.pyplot as plt

patterns = np.array([[1,0,0,0,1,0,0,0,1], [0,0,1,0,1,0,1,0,0], [0,1,0,1,1,1,0,1,0], [1,0,0,1,0,0,1,0,0]])#np.array([[1,1,1,0,0,0,0,0,0], [0,0,0,1,1,1,0,0,0], [0,0,0,0,0,0,1,1,1], [0,1,0,1,0,1,0,1,0]])
patterns = 2*patterns-1


weights = np.zeros((9,9))#np.eye(9) / 9

for i in range(9):
    for j in range(9):
        if i!=j:
            weights[i,j] = np.dot(patterns[:,i], patterns[:,j])
            #if np.abs(weights[i,j]) < .5:
            #    weights[i,j] = 0

def step(P, th=0.1):
    Pp = weights @ P
    return np.where(Pp>=th, 1, -1)

P0 = np.array([0,0,0,0,0,0,1,0,0])
P = P0
J = step(P)

nstep = 1
while np.abs(P-J).sum() > 0:
    P, J = J, step(J)
    nstep += 1
print(nstep)

fig, axes = plt.subplots(nrows=1, ncols=3)
axes[0].matshow(P0.reshape((3,3)))
axes[1].matshow(P.reshape((3,3)))
axes[2].matshow(weights)
plt.show()