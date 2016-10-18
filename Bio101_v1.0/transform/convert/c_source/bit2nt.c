/****************************************************************************
 * bit2nt - Convert a binary file to a nucleotide sequence ASCII text file 
 * Usage: bit2nt in_file out_file 
 *        "in_file" is the input file name which is to be converted 
 *        "out_file" is the out file name 
 *
 * Xianlong Wang, Univesity of Electronic Science and Technology of China, 8/6/2016.
 * iGEM UESTC SOFTWARE 2016 team.      
 * Part of BIO101 (DNA STORAGE SYSTEM) Project.
 ****************************************************************************/

#include <string.h>
#include <stdio.h>

#define BLOCKSIZE (1024)

//bit2nt: one byte of bits convert into 4 bytes of A (65), C(67), G(71), T(84) sequence
// 00 -> A, 01 -> C, 10 -> G, 11 -> T 
static unsigned char nt_code[] = {65, 67, 71, 84};
int bit2nt(unsigned char byte, unsigned char *nts) {
  unsigned char mask = 0x03;	
  int i;
  for (i = 0; i<4; i++)
     nts[i] =nt_code[(byte >> (i*2)) & mask];
  return 0;
}

int main(int argc, char* argv[])
{

  //check arguments
  if (argc < 3) {
     printf("ERROR: Too few arguments.\n");
     printf("Usage: %s input_file outpout_file\n", argv[0]);
     return 1;
  }
  //check file existence

  //read file in the byte mode
  FILE* fi = fopen(argv[1], "rb");
  FILE* fo = fopen(argv[2], "wb");
  int fr; //file operation return value, untreated
  
  //check file size
  fseek(fi, 0L, SEEK_END);
  unsigned int size = ftell(fi);
  int cycles = size / BLOCKSIZE, tail = size % BLOCKSIZE ;
  fseek(fi, 0L, SEEK_SET);

  unsigned char in[BLOCKSIZE], out[4*BLOCKSIZE], nts[4];
  //initialize buffer with zeros
  memset(in, 0, sizeof(in));
  int i, j, k;
  for (i=0; i<cycles; i++) {
    // block-read in 1k data 
    fr = fread(in, BLOCKSIZE, 1, fi);
    // convert
    for (j=0; j<BLOCKSIZE; j++) {
	    bit2nt(in[j], nts);
	    for (k=0; k<4; k++) out[4*j+k] = nts[k] ;
    }
    fr = fwrite(out, 4*BLOCKSIZE, 1, fo);
  }
  //handle tail
  fr = fread(in, tail, 1, fi);
  for (i=0; i<tail; ++i) {
	  bit2nt(in[i], nts);
	  for (j=0; j<4; j++) out[4*i+j] = nts[j];
  }
  fr = fwrite(out, 4*tail, 1, fo);

  fclose(fi);
  fclose(fo);
  return 0;
}
