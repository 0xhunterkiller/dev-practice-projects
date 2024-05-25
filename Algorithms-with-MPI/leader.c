#include<stdio.h>
#include<mpi.h>
#include<stdlib.h>

int main(int argc, char *argv[]){
    int err,rank,size,uid,recv,round=1;
    err = MPI_Init(&argc,&argv);
    if(err != MPI_SUCCESS){
        printf("Error Initializing\n");
        MPI_Abort(MPI_COMM_WORLD,1);
    }
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Status st;

    // Generate UIDs
    uid = (rand()*(rank+1) * size)%100;
    if(uid < 0){
        uid = uid + 100;
    }
    printf("Rank %d and UID %d\n",rank,uid);

    // Set Next and Prev
    int next = (rank == size-1 ? 0 : rank + 1);
    int prev = (rank == 0 ? size - 1 : rank - 1);

    // Send Initial Election Process
    MPI_Send(&uid,1,MPI_INT,next,round,MPI_COMM_WORLD);

    // Election
    while(1){
        MPI_Recv(&recv,1,MPI_INT,prev,MPI_ANY_TAG,MPI_COMM_WORLD,&st);
        if(st.MPI_TAG == 201){
            MPI_Send(&recv,1,MPI_INT,next,201,MPI_COMM_WORLD);
            break;
        }
        else{
            round = st.MPI_TAG;
            if(recv == uid){
                printf("I am the leader : Rank %d and UID %d\n",rank,uid);
                MPI_Send(&recv,1,MPI_INT,next,201,MPI_COMM_WORLD);
                break;
            }
            else if(recv > uid){
                MPI_Send(&recv,1,MPI_INT,next,round + 1,MPI_COMM_WORLD);
            }
        }
    }
    MPI_Finalize();
    return 0;
}