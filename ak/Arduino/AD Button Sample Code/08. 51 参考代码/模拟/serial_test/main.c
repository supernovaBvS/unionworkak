#include <stdio.h>
#include <reg52.h>
#include <ADC0832.h>

 
void InitUART(void) 
{
    TH1 = 0xFD;	 //??11.0592mhz ?????9600
    TL1 = TH1;
    TMOD |= 0x20;	  
    SCON = 0x50;	 
    ES = 1;			  
    TR1 = 1;		 
    TI = 1;    
		PS = 0;
	  EA = 1;	  	 
}

void delay_ms(unsigned int t)
{
    unsigned char a,b;
    while(t--)
    {
      for(b=102;b>0;b--)
      for(a=3;a>0;a--);
    }
}

int adcv = 0;

void main()
{
    InitUART(); 
		
    while(1)
    {
        delay_ms(500);
			  adcv = get_0832_AD_data(0);
        printf("Hello World222! %d\n", adcv);
    }
}