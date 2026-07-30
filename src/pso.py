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


# Piece 3 (Moving the swarm, three pulls)
def update_swarm(positions, velocities, pbest, gbest, w = 0.7, c1=1.5, c2=1.5):
    num_particles, num_assets = positions.shape
    r1 = np.random.random((num_particles, num_assets)) #this generates a random set of numbers between 0 and 1 for each particle and each asset. this is used to determine how much each particle is influenced by its own best position (pbest) and the global best position (gbest). using random.random ensures each nudge has a uniform chance of being selected.  
    r2 = np.random.random((num_particles, num_assets)) #this generates a random set of numbers between 0 and 1 for each particle and each asset. this is used to determine how much each particle is influenced by its own best position (pbest) and the global best position (gbest). using random.random ensures each nudge has a uniform chance of being selected.
    velocities = w * velocities + c1 * r1 * (pbest - positions) + c2 * r2 * (gbest - positions) #this is the formula for updating the velocities of the particles. it takes into account the current velocity, the distance to the particle's best position, and the distance to the global best position. the weights w, c1, and   c2 determine how much influence each of these factors has on the new velocity.
    positions += velocities #this updates the positions of the particles based on their new velocities      
    for i in range(num_particles):
        positions[i] = repair_weights(positions[i]) #this ensures that the weights of the portfolio allocation sum to 1 and are all non-negative after the update. this is important because we want to ensure that the portfolio allocation is valid after each update.    
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


