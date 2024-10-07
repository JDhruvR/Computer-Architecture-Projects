#include<stdio.h>

int main(){
	int n, ans=0;
	scanf("%d", &n);
	if(n<=1){
		ans=0;
	}
	else{
		int flag=0;
		for(int i=2;i<n;i++){
			if(n%i==0){
				flag=1;
				ans=0;
				break;
			}
		}
		if(flag==0){
			ans=1;
		}	
	}
	printf("%d\n", ans);
}
