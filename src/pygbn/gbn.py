import numpy as np
from typing import *


def gbn(h: float, T: float, A: float, ts: float, flag: int = 0) -> np.array:
    # Computing the non-switching probability
    if flag == 0:
        p = 1 - h / ts
    elif flag == 1:
        p = 1 - 5 * h / ts
    elif flag == 2:
        p = 1 - 3 * h / ts
    else:
        raise ValueError("flag must be 0, 1, or 2")

    N = int(np.ceil(T/h).item()) # length of discrete signal

    valid_signal = False
    start = 1
    while ~valid_signal:
        # if x[i]==1, then switch the signal value, 
        # otherwise if x[i]==0, don't switch
        x = np.random.choice(2, N, p=[1-p, p])

        signal = np.empty_like(x)
        for i in range(N):
            if x[i] == 1:
                signal[i] = -start * A
                start = -start
            else:
                signal[i] = start * A

        # Verifying the designed GBN-signal %%%%%%%%%%%%%%%%%%%%%%%%%%%
        # 
        # If the process model is an overdamped system the test-signal
        # should be verified
        # 
        # 1) The test signal should not be used, if the number of
        #    switches is too large (more that 120 % of the calculated
        #    average number of switches) or too less (less than 80 %
        #    of the calculated average number of switches)
        # 2) Allow for each 20 expected switches one sequence in the
        #    signal without a switch longer than 2.5*settling time
        # 3) Allow the signal to have 2 switches faster than 0.1 times
        #    the settling time for each 10 expected switches
        # 

        if flag == 0:
            av = 1*T/ts
            pass
        else:
            valid_signal = True

    return signal
