#include<stdio.h>
#include<mpi.h>
#define SIZE 4

int main(int argc,char *argv[]){
    int rank,size,err;
    err = MPI_Init(&argc,&argv);
    if(err != MPI_SUCCESS){
        printf("Error during Initialization.\n");
        MPI_Abort(MPI_COMM_WORLD,1);
    }
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    if(size != SIZE){
        printf("This task must be run on 4 processes.\n");
        MPI_Abort(MPI_COMM_WORLD,1);
    }
    int sendbuf[SIZE][SIZE] = {
        {1,2,3,4},
        {5,6,7,8},
        {9,10,11,12},
        {13,14,15,16}
    };
    int recvbuf[SIZE];
    int source = 0;

    MPI_Scatter(sendbuf,SIZE,MPI_INT,recvbuf,SIZE,MPI_INT,source,MPI_COMM_WORLD);
    printf("Process [%d]: Received Values : %d %d %d %d on a Scatter\n",rank,recvbuf[0],recvbuf[1],recvbuf[2],recvbuf[3]);

    int finalsums[SIZE];

    MPI_Reduce(recvbuf,finalsums,SIZE,MPI_INT,MPI_SUM,source,MPI_COMM_WORLD);

    if(rank == 0){
        printf("Process [%d]: Received Values : %d %d %d %d on a Reduce\n",rank,finalsums[0],finalsums[1],finalsums[2],finalsums[3]);
    }
    MPI_Finalize();
    return 0;
}