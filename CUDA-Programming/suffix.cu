#include<stdio.h>
#include<cuda.h>
#include<math.h>

__global__ void suffix(int *arr){
    int t = threadIdx.x;
    for(int i=0;i<2;i++){
        if(t + (int)pow(2,i) < 8){
            arr[t] = arr[t] + arr[t + (int)pow(2,i)];
        }
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
    prefix<<<1,8>>>(da);
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