#Piece 1 (Data Cleaning for Sharpe Calculation)
import numpy as np
def repair_weights(w):
    w = np.maximum(w, 0)
    return w/np.sum(w)


if __name__ == "__main__":
    # --- quick test ---
    messy = np.array([0.4, -0.2, 0.8, 0.3])
    print("messy   :", messy)
    print("cleaned :", repair_weights(messy))
    print("sums to :", repair_weights(messy).sum())