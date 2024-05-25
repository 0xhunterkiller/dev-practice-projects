#include<stdio.h>
#include<cuda.h>

__constant__ int key;

__global__ void linsearch(int *a,int *p){
    int t = threadIdx.x;
    if(a[t] == key){
        *p = t;
    }
}
int main(){
    int n,k,*darr,*p,pos=-1;
    printf("Enter the Number of Elements : ");
    scanf("%d",&n);
    int arr[n];
    printf("Enter the Elements : \n");
    for(int i=0;i<n;i++){
        scanf("%d",&arr[i]);
    }
    printf("\nEnter the element to search for : ");
    scanf("%d",&k);
    cudaMalloc((void**)&darr,n*sizeof(int));
    cudaMemcpy(darr,&arr,n*sizeof(int),cudaMemcpyHostToDevice);
    cudaMalloc((void**)&p,sizeof(int));
    cudaMemcpy(p,&pos,sizeof(int),cudaMemcpyHostToDevice);
    cudaMemcpyToSymbol(key,k, sizeof(int));
    cudaEvent_t start,stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);
    linsearch<<<1,n>>>(darr,p);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaMemcpy(&pos,p,sizeof(int),cudaMemcpyDeviceToHost);
    printf("Element Found At : %d\n",pos);
    cudaFree(p);
    cudaFree(darr);
    return 0;
}