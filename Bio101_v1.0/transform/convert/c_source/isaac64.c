/****************************************************************************
 * ISAAC - File encryption program using the ISAAC method developed by B. Jenkins
 *         The same code can be used for both encryption and decryption purposes.
 * Usage: isaac in_file out_file token
 *        "in_file" is the input file name which is to be encrypted or decrypted  
 *        "out_file" is the out file name which has been encrypted or decrypted
 *        "token" is the password to encrypt the in_file. At most 256 ASCII code
 *        will be used. Longer string will be truncated.
 *
 * Xianlong Wang, Univesity of Electronic Science and Technology of China, 8/5/2016.
 * iGEM UESTC SOFTWARE 2016 team.      
 * Part of BIO101 (DNA STORAGE SYSTEM) Project.
 ****************************************************************************/

/*
------------------------------------------------------------------------------
ISAAC64.c. By Bob Jenkins, 1996.  Public Domain.
------------------------------------------------------------------------------
*/
#include <string.h>
#ifndef STANDARD
#include "standard.h"
#endif
#ifndef ISAAC64
#include "isaac64.h"
#endif

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
extern    ub8 randrsl[RANDSIZ], randcnt;
static    ub8 mm[RANDSIZ];
static    ub8 aa=0, bb=0, cc=0;

#define ind(mm,x)  (*(ub8 *)((ub1 *)(mm) + ((x) & ((RANDSIZ-1)<<3))))
#define rngstep(mix,a,b,mm,m,m2,r,x) \
{ \
  x = *m;  \
  a = (mix) + *(m2++); \
  *(m++) = y = ind(mm,x) + a + b; \
  *(r++) = b = ind(mm,y>>RANDSIZL) + x; \
}

void isaac64()
{
  register ub8 a,b,x,y,*m,*m2,*r,*mend;
  m=mm; r=randrsl;
  a = aa; b = bb + (++cc);
  for (m = mm, mend = m2 = m+(RANDSIZ/2); m<mend; )
  {
    rngstep(~(a^(a<<21)), a, b, mm, m, m2, r, x);
    rngstep(  a^(a>>5)  , a, b, mm, m, m2, r, x);
    rngstep(  a^(a<<12) , a, b, mm, m, m2, r, x);
    rngstep(  a^(a>>33) , a, b, mm, m, m2, r, x);
  }
  for (m2 = mm; m2<mend; )
  {
    rngstep(~(a^(a<<21)), a, b, mm, m, m2, r, x);
    rngstep(  a^(a>>5)  , a, b, mm, m, m2, r, x);
    rngstep(  a^(a<<12) , a, b, mm, m, m2, r, x);
    rngstep(  a^(a>>33) , a, b, mm, m, m2, r, x);
  }
  bb = b; aa = a;
  //added by xwang
  randcnt = 0;
}

#define mix(a,b,c,d,e,f,g,h) \
{ \
   a-=e; f^=h>>9;  h+=a; \
   b-=f; g^=a<<9;  a+=b; \
   c-=g; h^=b>>23; b+=c; \
   d-=h; a^=c<<15; c+=d; \
   e-=a; b^=d>>14; d+=e; \
   f-=b; c^=e<<20; e+=f; \
   g-=c; d^=f>>17; f+=g; \
   h-=d; e^=g<<14; g+=h; \
}

void randinit(flag)
word flag;
{
   word i;
   ub8 a,b,c,d,e,f,g,h;
   aa=bb=cc=(ub8)0;
   a=b=c=d=e=f=g=h=0x9e3779b97f4a7c13LL;  /* the golden ratio */

   for (i=0; i<4; ++i)                    /* scramble it */
   {
     mix(a,b,c,d,e,f,g,h);
   }

   for (i=0; i<RANDSIZ; i+=8)   /* fill in mm[] with messy stuff */
   {
     if (flag)                  /* use all the information in the seed */
     {
       a+=randrsl[i  ]; b+=randrsl[i+1]; c+=randrsl[i+2]; d+=randrsl[i+3];
       e+=randrsl[i+4]; f+=randrsl[i+5]; g+=randrsl[i+6]; h+=randrsl[i+7];
     }
     mix(a,b,c,d,e,f,g,h);
     mm[i  ]=a; mm[i+1]=b; mm[i+2]=c; mm[i+3]=d;
     mm[i+4]=e; mm[i+5]=f; mm[i+6]=g; mm[i+7]=h;
   }

   if (flag) 
   {        /* do a second pass to make all of the seed affect all of mm */
     for (i=0; i<RANDSIZ; i+=8)
     {
       a+=mm[i  ]; b+=mm[i+1]; c+=mm[i+2]; d+=mm[i+3];
       e+=mm[i+4]; f+=mm[i+5]; g+=mm[i+6]; h+=mm[i+7];
       mix(a,b,c,d,e,f,g,h);
       mm[i  ]=a; mm[i+1]=b; mm[i+2]=c; mm[i+3]=d;
       mm[i+4]=e; mm[i+5]=f; mm[i+6]=g; mm[i+7]=h;
     }
   }

   isaac64();          /* fill in the first set of results */
   //modified by xwang
   //randcnt=RANDSIZ;    /* prepare to use the first set of results */
   randcnt=0;
}

// Get a random 64-bit value 0..MAXINT
ub8 iRandom()
{
	ub8 r = randrsl[randcnt];
	++randcnt;
	if (randcnt >RANDSIZ) {
		isaac64();
		randcnt = 0;
	}
	return r;
}
 
// Seed ISAAC with a string
// seed longer than RANDSIZ will be truncated
void iSeed(char *seed, int flag)
{
	register ub8 i,m;
	for (i=0; i<RANDSIZ; i++) mm[i]=0;
	m = strlen(seed);
	for (i=0; i<RANDSIZ; i++)
	{
	  // in case seed has less than 256 elements
          if (i>m) randrsl[i]=0;  else randrsl[i] = seed[i];
	}
	// initialize ISAAC with seed
	randinit(flag);
}

int main(int argc, char* argv[])
{

  //check arguments
  if (argc < 4) {
     printf("ERROR: Too few arguments.\n");
     printf("Usage: %s input_file outpout_file token\n", argv[0]);
     return 1;
  }
  //check file existence
  char *token = argv[3];

  //initialize random seed 
  iSeed(token, TRUE);

  //read file in the byte mode
  FILE* fi = fopen(argv[1], "rb");
  FILE* fo = fopen(argv[2], "wb");
  int fr; //file operation return value, untreated
  
  //check file size
  fseek(fi, 0L, SEEK_END);
  unsigned int size = ftell(fi);
  int cycles = size / (8*RANDSIZ), tail = size % (8*RANDSIZ) ;
  fseek(fi, 0L, SEEK_SET);

  ub8 in[RANDSIZ], out[RANDSIZ];
  //initialize buffer with zeros
  int i, j;
  for (i=0; i<RANDSIZ; i++) in[i] = 0;
  for (i=0; i<cycles; i++) {
    // block-read in 1k data, 8*RANDSIZ 
    fr = fread(in, RANDSIZ, 8, fi);
    // encode
    for (j=0; j<RANDSIZ; ++j) out[j] = in[j] ^ iRandom();
    fr = fwrite(out, RANDSIZ, 8, fo);
  }
  //handle tail
  cycles = tail / 8;
  tail = tail % 8;
  fr = fread(in, cycles+1, 8, fi);
  for (i=0; i<=cycles; ++i) out[i] = in[i] ^ iRandom();
  fr = fwrite(out, cycles, 8, fo);
  //tail of tail, shorter than 8 bytes (64 bits)
  fr = fwrite(&out[cycles], 1, tail, fo);

  fclose(fi);
  fclose(fo);
  return 0;
}
