#include<stdio.h> 
#include<stdlib.h> 

extern char* get_env_val(char* env_var); 

char* get_env_val(char* env_var) { 
    return getenv(env_var)
}