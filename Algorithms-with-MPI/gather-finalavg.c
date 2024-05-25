#include<stdio.h>
#include<mpi.h>
#define SIZE 4

int main(int argc,char *argv[]){
    int rank,size,err;
    int snums[SIZE][SIZE] = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,16}};
    int rnums[SIZE];
    err = MPI_Init(&argc,&argv);
    if(err != MPI_SUCCESS){
        printf("Error Initializing.\n");
        MPI_Abort(MPI_COMM_WORLD,1);
    }
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    if(size != SIZE){
        printf("This task runs on %d processes.\n",SIZE);
        MPI_Abort(MPI_COMM_WORLD,1);
    }
    // Scatter
    if(rank == 0){
        printf("Scattering Now...\n");
    }
    int source = 0;
    MPI_Scatter(snums,SIZE,MPI_INT,rnums,SIZE,MPI_INT,source,MPI_COMM_WORLD);
    
    printf("Process [%d] has : ",rank);
    for(int i=0;i<SIZE;i++){
        printf("%d ",rnums[i]);
    }
    printf("\n");
    float avg = 0.0;
    for(int i=0;i<SIZE;i++){
        avg += rnums[i];
    }
    avg = avg/SIZE;
    
    float anums[SIZE];
    if(rank == 0){
        printf("Gathering Now...\n");
    }
    MPI_Gather(&avg,1,MPI_FLOAT,&anums,1,MPI_FLOAT,source,MPI_COMM_WORLD);
    if(rank == 0){
        float favg = 0.0;
        for(int i=0;i<SIZE;i++){
            favg += anums[i];
        }
        favg = favg/SIZE;
        printf("Final Average is : %f \n",favg);
    }
}
