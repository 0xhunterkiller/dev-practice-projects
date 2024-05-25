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
    float sendbuf[SIZE][SIZE] = {
        {1.0,2.0,3.0,4.0},
        {5.0,6.0,7.0,8.0},
        {9.0,10.0,11.0,12.0},
        {13.0,14.0,15.0,16.0}
    };
    float recvbuf[SIZE];
    int sendcount = SIZE;
    int recvcount = SIZE;
    int source = 1;

    MPI_Scatter(sendbuf,sendcount,MPI_FLOAT,recvbuf,recvcount,MPI_FLOAT,source,MPI_COMM_WORLD);
    // MPI_Scatter();
    printf("Process [%d]: Received Values : %f %f %f %f on a Scatter\n",rank,recvbuf[0],recvbuf[1],recvbuf[2],recvbuf[3]);

    MPI_Finalize();
    return 0;
}