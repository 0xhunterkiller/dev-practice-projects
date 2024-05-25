#include<stdio.h>
#include<mpi.h>

int main(int argc,char *argv[]){
    int rank,size,err;
    err = MPI_Init(&argc,&argv);
    if(err != MPI_SUCCESS){
        printf("Error during Initialization.\n");
        MPI_Abort(MPI_COMM_WORLD,1);
    }
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    int buf = 12345;
    if(rank == 0){
        buf = 200;
    }
    int source = 0;
    printf("Before Bcast: Process %d has %d in Buffer\n",rank,buf);
    MPI_Bcast(&buf,1,MPI_INT,source,MPI_COMM_WORLD);
    printf("After  Bcast: Process %d has %d in Buffer\n",rank,buf);    

    MPI_Finalize();
    return 0;
}

/*
Before Bcast: Process 0 has 200 in Buffer
Before Bcast: Process 1 has 12345 in Buffer
Before Bcast: Process 3 has 12345 in Buffer
Before Bcast: Process 2 has 12345 in Buffer
Before Bcast: Process 4 has 12345 in Buffer
After  Bcast: Process 0 has 200 in Buffer
After  Bcast: Process 1 has 200 in Buffer
After  Bcast: Process 2 has 200 in Buffer
After  Bcast: Process 3 has 200 in Buffer
After  Bcast: Process 4 has 200 in Buffer
*/