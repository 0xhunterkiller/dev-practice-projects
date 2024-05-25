#include<stdio.h>
#include<mpi.h>
#define PING_PONG_LIMIT 3
int main(int argc,char *argv[]){
	int rank,size,err,ppc;
	err = MPI_Init(&argc,&argv);
	if(err!=MPI_SUCCESS){
		printf("Error Initializing MPI\n");
		MPI_Abort(MPI_COMM_WORLD,1);
	}
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&size);

	if(size != 2){
		printf("Run this process with 2 processes.");
		MPI_Abort(MPI_COMM_WORLD,1);
	}	

	int partner = (rank+1)%2;
	ppc = 0;

	while(ppc < PING_PONG_LIMIT){
		if(rank == ppc%2){
			ppc++;
			MPI_Send(&ppc,1,MPI_INT,partner,0,MPI_COMM_WORLD);
			printf("Sending Ping Pong Count : %d from %d to %d\n",ppc,rank,partner);
		}
		else{
			MPI_Recv(&ppc,1,MPI_INT,partner,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
			printf("Received Ping Pong Count : %d from %d\n",ppc,rank);
		}
	}
	MPI_Finalize();
	return 0;
}
