#include<stdio.h>
#include<cuda.h>

__global__ void oddeven(int *arr){
    int t = threadIdx.x;
    for(int i=0;i<4;i++){
        if(t%2 == 0 && t < 7){
            if(arr[t] > arr[t+1]){
                int temp = arr[t];
                arr[t] = arr[t+1];
                arr[t+1] = temp;
            }
        }
        __syncthreads();
        if(t%2 == 1 && t < 7){
            if(arr[t] > arr[t+1]){
                int temp = arr[t];
                arr[t] = arr[t+1];
                arr[t+1] = temp;
            }
        }
        __syncthreads();
    }
}
int main(){
    int *da,arr[8] = {2,5,4,3,6,8,7,9};
    float ms;
    cudaMalloc((void**)&da,sizeof(int)*8);
    cudaMemcpy(da,&arr,sizeof(int)*8,cudaMemcpyHostToDevice);
    cudaEvent_t start,stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    oddeven<<<1,8>>>(da);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&ms,start,stop);
    cudaMemcpy(&arr,da,sizeof(int)*8,cudaMemcpyDeviceToHost);
    printf("Finished in %f milliseconds\n",ms);
    for(int i=0;i<8;i++){
        printf("%d ",arr[i]);
    }
    printf("\n");
    return 0;
}