#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void win() {
  char buf[50];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    fflush(stdout);
    exit(0);
  }
  fgets(buf,50,f); // size bound read
  puts(buf);
  fflush(stdout);
}

void vuln(){
  char buffer[64];
  printf("Enter some data: ");
  fflush(stdout);
  read(STDIN_FILENO, buffer, 128);
  printf("Your data was read. Did you get the flag?\n");
  fflush(stdout);
}

int main(int argc, char **argv){
  pid_t pid;
  while(1){
    pid = fork();
    if (pid < 0) {
      perror("fork failed");
	  exit(EXIT_FAILURE);
	}
	if (pid == 0) {
	  vuln();
	  exit(EXIT_SUCCESS);
	} else {
	  wait(NULL);
	}
  }
  return 0;
}