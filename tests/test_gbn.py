# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

import numpy as np
from pygbn import gbn


class TestGbn(unittest.TestCase):
    def init_parameters(self):
        self.h = 0.05 # sampling period [s]
        self.T = 1 # length of signal [s]
        self.A = 1 # amplitude of signal
        self.ts = 1 # estimated settling time of the process [s]

    def seed(self):
        np.random.seed(1)

    def test_gbn_oscillary_min_phase(self):
        self.seed()
        self.init_parameters()

        # generate time array
        t = np.arange(start=0, stop=self.T, step=self.h)

        # generate the signal
        # the gbn function returns a time array and a signal array
        u = gbn(self.h, self.T, self.A, self.ts, 1)
        u_target = np.array([-1,  1,  1, -1, -1, 
                             -1, -1,  1, -1,  1, 
                             -1,  1,  1, -1, -1,  
                             1, -1,  1,  1,  1])

        self.assertEqual(t.shape, u.shape)
        self.assertListEqual(u.tolist(), u_target.tolist())


if __name__ == '__main__':
    unittest.main()
