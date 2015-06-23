SRC     = mpi_sample.c
EXE     = mpi_sample
OBJ    +=$(SRC:.c=.o)
CC      = mpicc
CFLAGS  = -O3
LDFLAGS = 
NPROC   = 8

#-- Implicit rules --
.c.o:
	$(CC) $(CFLAGS) -c $<

#-- Targets --
all: $(EXE)

run: $(EXE)
	mpirun -np $(NPROC) $(EXE)

$(EXE):  $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $@ $(LDFLAGS)

clean:
	rm -f *.o $(EXE)
