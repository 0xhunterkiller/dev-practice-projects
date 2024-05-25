#include<stdio.h>
#include<cuda.h>

__global__ void sumn(int *arr,int *res){
    int t = blockIdx.x*blockDim.x + threadIdx.x;
    atomicAdd(res,arr[t]);
}
int main(){
    int n = 100;
    int *da,*res,result,arr[n];
    for(int i=0;i<n;i++){
        arr[n] = i+1;
    }
    float ms;
    cudaMalloc((void**)&da,sizeof(int)*n);
    cudaMalloc((void**)&res,sizeof(int));
    cudaMemcpy(da,&arr,sizeof(int)*n,cudaMemcpyHostToDevice);
    cudaEvent_t start,stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    sumn<<<2,50>>>(da,res);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&ms,start,stop);
    cudaMemcpy(&result,res,sizeof(int),cudaMemcpyDeviceToHost);
    printf("Finished in %f milliseconds\n",ms);
    printf("Sum is %d\n",result);
    printf("\n");
    return 0;
}