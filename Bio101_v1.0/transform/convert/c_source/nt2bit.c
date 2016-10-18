/****************************************************************************
 * nt2bit - Convert a nucleotide sequence file to a binary file 
 * Usage: nt2bit in_file out_file
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
/*
int bit2nt(unsigned char byte, unsigned char *nts) {
  unsigned char mask = 0x03;	
  for (int i = 0; i<4; i++)
     nts[i] =nt_code[(byte >> (i*2)) & mask];
  return 0;
}
*/

//nt2bit, reverse conversion
unsigned char nt2bit(unsigned char *nts) {
  unsigned char byte = 0; 
  int i, j;
  for (i = 0; i<4; i++) 
     for(j = 0; j<4; j++)
	if(nt_code[j] == nts[i]) byte += (j<< (2*i));
  return byte;
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
  if ((size % 4) != 0) {
    printf("Corrupted file. The input file size should be a multiple of 4.");
    return 1;
  }
  size = size / 4;
  int cycles = size / BLOCKSIZE, tail = size % BLOCKSIZE;
  fseek(fi, 0L, SEEK_SET);

  unsigned char in[4*BLOCKSIZE], out[BLOCKSIZE];
  //initialize buffer with zeros
  memset(in, 0, sizeof(in));
  int i, j;
  for (i=0; i<cycles; i++) {
    // block-read in 1k data 
    fr = fread(in, 4*BLOCKSIZE, 1, fi);
    // convert
    for (j=0; j<BLOCKSIZE; j++)
	 out[j] = nt2bit(&in[4*j]);
    fr = fwrite(out, BLOCKSIZE, 1, fo);
  }

  //handle tail
  fr = fread(in, 4*tail, 1, fi);
  for (i=0; i<tail; ++i)
      out[i] = nt2bit(&in[4*i]);
  fr = fwrite(out, tail, 1, fo);

  fclose(fi);
  fclose(fo);
  return 0;
}
