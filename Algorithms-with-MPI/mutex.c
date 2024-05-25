#include<stdio.h>
#include<mpi.h>

int main(int argc,char *argv[]){
    int err, rank, size;
    err = MPI_Init(&argc,&argv);
    if(err != MPI_SUCCESS){
        printf("Error Initializing!\n");
        MPI_Abort(MPI_COMM_WORLD,1);
    }
    int shared = 0;

    if(rank == 0){
        int queue[10];
        for(int i=0;i<10;i++){
            queue[i] = 0;
        }
        int front = 0;
        int rear = -1;
        int count = 0;
        int lock = 0;
        int process;
        MPI_Status st;
        while(1){
            MPI_Recv(&process,1,MPI_INT,MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD,&st);
            if(st.MPI_SOURCE == 0){
                break;
            }
            printf("Queue has : ");
            for(int i=front;i<6;i++){
                if(queue[i] == 0)
                    break;
                printf("%d ",queue[i]);
            }
            printf("\n");
            if(st.MPI_TAG == 1){
                if(lock == 0 && count == 0){
                    lock = 1;
                    printf("Process %d acquired shared resource \n",process);
                    MPI_Send(&shared,1,MPI_INT,process,2,MPI_COMM_WORLD);
                }
                else{
                    queue[++rear] = process;
                    count++;
                }
            }
            if(st.MPI_TAG == 3){
                shared = process;
                printf("Process %d updated to %d\n",st.MPI_SOURCE,shared);
                int send = queue[front++];
                count--;
                if(send == 0){
                    break;
                }
                printf("Process %d acquired shared resource\n", send);
                MPI_Send(&shared,1,MPI_INT,send,2,MPI_COMM_WORLD);
            }
        }
    }
    else{
        MPI_Send(&rank,1,MPI_INT,0,1,MPI_COMM_WORLD);
        MPI_Status st;
        int recv;
        MPI_Recv(&shared,1,MPI_INT,0,2,MPI_COMM_WORLD,&st);
        if(st.MPI_TAG == 2){
            int before = shared;
            shared++;
            printf("Process [%d] : Before [%d] After [%d]",rank,before,shared);
            MPI_Send(&shared,1,MPI_INT,0,3,MPI_COMM_WORLD);
        }
    }
    MPI_Finalize();
}