#include<stdio.h>
#include<cuda.h>

__global__ void enumsort(int *arr){
    int t = threadIdx.x;
    int q;
    int c=0;
    for(int i=0;i<8;i++){
        if(t!=i && arr[t] > arr[i]){
            c++;
        }
    }
    q = arr[t];
    __syncthreads();
    arr[c] = q; 
}
int main(){
    float ms;
    int *da;
    int arr[8] = {2,3,5,4,6,8,7,9};
    cudaMalloc((void**)&da,sizeof(int)*8);
    cudaMemcpy(da,&arr,sizeof(int)*8,cudaMemcpyHostToDevice);
    cudaEvent_t start,stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    enumsort<<<1,8>>>(da);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&ms,start,stop);
    printf("Finished in %f ms\n",ms);
    printf("Final Array : ");
    cudaMemcpy(&arr,da,sizeof(int)*8,cudaMemcpyDeviceToHost);
    for(int i=0;i<8;i++){
        printf("%d ",arr[i]);
    }
    printf("\n");
}