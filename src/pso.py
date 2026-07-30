#Piece 1 (Data Cleaning for Clean Sharpe Calculation)
import numpy as np
def repair_weights(w):
    w = np.maximum(w, 0) #this helps us turn negative weights to zero so that we can follow the rules of portfolio allocation (no short selling)
    return w/np.sum(w) #this ensures that the weights sum to 1 which is a requirement for portfolio allocation 100%


# Piece 2 (Swarm Initialization for Portfolio Allocation)
def initialize_swarm(num_particles, num_assets): #herein num_particles represent the number of rows which is an entire set of weights for the specific portfolio allocation and num_assets represent the columns or the different weights of a single ticker acros the entire portfolio allocation
    positions = np.random.random((num_particles, num_assets)) #this generates a random set of weights for the portfolio allocation.
    for i in range (num_particles):
        positions[i] = repair_weights(positions[i])
    velocities = np.random.uniform(-0.1, 0.1, (num_particles, num_assets)) #this generates a random set of velocities with the range of nudges being only -0.1 to 0.1 which is a small nudge to the weights of the portfolio. using random.uniform ensures each nudge has a uniform chance of being selected.
    return positions, velocities  

if __name__ == "__main__":
    # --- quick test for 1
    messy = np.array([0.4, -0.2, 0.8, 0.3])
    print("messy   :", messy)
    print("cleaned :", repair_weights(messy))
    print("sums to :", repair_weights(messy).sum())  
    # --- quick test for 2

    # --- test Piece 2: initialize_swarm ---
    positions, velocities = initialize_swarm(5, 4)   # make a small swarm: 5 particles, 4 assets
    print()
    print("positions shape :", positions.shape)        # should be (5, 4)
    print("each row sums to:", positions.sum(axis=1))  # should all be 1
    print("velocities shape:", velocities.shape)       # should be (5, 4)


