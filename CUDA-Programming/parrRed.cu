#include<stdio.h>
#include<cuda.h>

__global__ void parrred(int *arr){
    int t = threadIdx.x;
    for(int i=0;i<8;i*=2){
        if(t%(2*i) == 0 && t+i < 8){
            arr[t] = arr[t] + arr[t+(2*i)];
        }
    }
    __syncthreads();
}
int main(){
    int *da,arr[8] = {1,2,3,4,5,6,7,8};
    float ms;
    cudaMalloc((void**)&da,sizeof(int)*8);
    cudaMemcpy(da,&arr,sizeof(int)*8,cudaMemcpyHostToDevice);
    cudaEvent_t start,stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    parrred<<<1,8>>>(da);
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