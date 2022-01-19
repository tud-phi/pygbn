import numpy as np
from typing import *


def gbn(h: float, T: float, A: float, ts: float, 
        flag: int = 0, max_it: int = 100, seed: Optional[int] = None) -> np.array:
    # seed the random generator
    if seed is not None:
        np.random.seed(seed)

    # Computing the non-switching probability
    if flag == 0:
        p = 1 - h / ts
    elif flag == 1:
        p = 1 - 5 * h / ts
    elif flag == 2:
        p = 1 - 3 * h / ts
    else:
        raise ValueError("flag must be 0, 1, or 2")

    N = int(np.ceil(T / h).item()) # length of discrete signal

    valid_signal = False
    start = 1
    it = -1
    while valid_signal is False and it < max_it:
        it = it + 1
        
        # if x[i]==1, then switch the signal value, 
        # otherwise if x[i]==0, don't switch
        x = np.random.choice(2, N, p=[p, 1-p])

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
            n_s = np.sum(np.diff(signal)!=0)

            f_sw = int((n_s - n_s % 10) / 10)
            f_sw = int(2*f_sw + 3)
            s_sw = int(np.round((n_s - n_s % 20) / 20))

            ind = np.argwhere(np.concatenate([np.array([1]), np.diff(signal)!=0])).squeeze()

            if ind.ndim == 0 or ind.shape[0] == 0:
                continue

            dur_sw = np.diff(ind)
            dur_sw = np.sort(dur_sw*h) # in seconds

            if dur_sw.shape[0] < f_sw+1:
                continue

            if dur_sw.shape[0] < n_s-s_sw+1:
                continue

            av = 1 * T / ts
            if 0.8*av<n_s and n_s<1.2*av and dur_sw[f_sw]>0.1*ts and dur_sw[n_s-s_sw]<2.5*ts:
                valid_signal = True
            pass
        else:
            valid_signal = True

    if valid_signal == False:
        raise RuntimeWarning("Could not find a valid signal, returning last signal instead")

    return signal
