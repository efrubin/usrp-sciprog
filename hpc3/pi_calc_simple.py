#!/usr/bin/env python

import numpy as np
import time
from mpi4py import MPI
Ntot = 1e9
Ntot = int(Ntot)

comm = MPI.COMM_WORLD
myrank = comm.Get_rank()
nproc = comm.Get_size()


N = Ntot/nproc

tstart = time.clock()
pi=0
for i in range(N):
	x = np.random.rand()
	y = np.random.rand()

	if x**2 + y**2 < 1:
		pi+=1

pi = comm.reduce(pi, op=MPI.SUM, root=0)
Ntot = comm.reduce(N, op=MPI.SUM, root=0)

if myrank==0:
	pi *= 4./Ntot
	relerr = abs(pi-np.pi)/np.pi
	tstop = time.clock()
	telsaped = tstop - tstart
	print 'Approximate pi = %1.3f' % pi
	print "Error = %1.3e" % relerr
	print "Elapsed time = %1.3f" % telsaped