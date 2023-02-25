#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //ensure proper usage
    if(argc!=2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }
    // open input file (forensic image)
    FILE*inptr=fopen(argv[1], "r");
    if(inptr==NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }
    //set outfile pointer to NULL
    FILE* outptr = NULL;
   //create an array of 512 elements to store 512 bytes from the memory card
    BYTE buffer[512];
    //count amount of jpeg files found
    int jpeg=0;
    //string to hold a filename
    char filename[8]={0};
    //read memory card until the end of file
    while(fread(buffer, sizeof(BYTE)*512, 1, inptr)==1)
    {
        //check if jpeg is found
        if(buffer[0]==0xFF&&buffer[1]==0xD8&&buffer[2]==0xFF&&(buffer[3]&0xF0)==0xE0)
        {
            //close outptr
            if(outptr != NULL)
            {
                fclose(outptr);
            }
                sprintf(filename, "%03d.jpg", jpeg++);

                //open a new outptr
                outptr = fopen(filename, "w");
        }
       //writing to jpeg file if new jpeg not found
       if(outptr != NULL)
       {
            fwrite(buffer, sizeof(BYTE)*512, 1, outptr);
       }
    }
    // close out file
     if (outptr != NULL)
     {
      fclose(outptr);
     }
    //close in file
      fclose(inptr);
    return 0;
}
