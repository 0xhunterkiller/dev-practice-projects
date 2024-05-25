#include<stdio.h>
#include<cuda.h>

__global__ void prime(int *arr,int n){
    int t = threadIdx.x + blockIdx.x*blockDim.x;
    int flag = 1;
    for(int i=2;i<(int)t/2;i++){
        if(t%i == 0){
            flag = 0;
        }
    }
    if(t < 2){
        flag = 0;
    }
    if(t == 2){
        flag = 1;
    }
    if(flag == 1){
        arr[t] = 1;
    }
}
int main(){
    int n;
    int *da,arr[n];
    float ms;
    cudaMalloc((void**)&da,sizeof(int)*n);
    cudaMemcpy(da,&arr,sizeof(int)*n,cudaMemcpyHostToDevice);
    cudaEvent_t start,stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    prefix<<<5,n>>>(da);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&ms,start,stop);
    cudaMemcpy(&arr,da,sizeof(int)*n,cudaMemcpyDeviceToHost);
    printf("Finished in %f milliseconds\n",ms);
    printf("Prime Number Distribution from 0 to %d\n",n);
    for(int i=0;i<n;i++){
        printf("%d ",arr[i]);
    }
    printf("\n");
    return 0;
}
