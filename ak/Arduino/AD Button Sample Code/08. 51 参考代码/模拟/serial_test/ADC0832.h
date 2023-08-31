#ifndef _ADC0832_H_
#define _ADC0832_H_


sbit ADC0832_CS=P1^3;	//控制IO口
sbit ADC0832_CLK=P1^4;
sbit ADC0832_DIO=P1^5;

/****************************************
1.ADC0832 转换带返回值函数
2.参数：channel为选取位变量
3.函数返回转换后的AD值   类型为int
****************************************/
unsigned char  get_0832_AD_data(bit channel)
{
	unsigned char i;
	unsigned char dat;
	ADC0832_CS=1;   //一个转换周期开始
	ADC0832_CLK=0;  //为第一个脉冲作准备
	ADC0832_CS=0;  //CS置0，片选有效
	ADC0832_DIO=1;    //DIO置1，规定的起始信号  
	ADC0832_CLK=1;   //第一个脉冲
	ADC0832_CLK=0;   //第一个脉冲的下降沿，此前DIO必须是高电平
	ADC0832_DIO=1;   //DIO置1， 通道选择信号
	ADC0832_CLK=1;   //第二个脉冲，第2、3个脉冲下沉之前，DI必须跟别输入两位数据用于选择通道，这里选通道RH0 
	ADC0832_CLK=0;   //第二个脉冲下降沿 
	ADC0832_DIO=channel;   //DI置0，选择通道0
	ADC0832_CLK=1;    //第三个脉冲
	ADC0832_CLK=0;    //第三个脉冲下降沿 
	ADC0832_DIO=1;    //第三个脉冲下沉之后，输入端DIO失去作用，应置1
	ADC0832_CLK=1;    //第四个脉冲
	for(i=0;i<8;i++)  //高位在前
	{
		ADC0832_CLK=1;         //第四个脉冲
		ADC0832_CLK=0; 
		dat<<=1;       //将下面储存的低位数据向右移
		dat|=(unsigned char)ADC0832_DIO; 	 //将输出数据DIO通过或运算储存在dat最低位 
	}	  		        
	ADC0832_CS=1;          //片选无效 
	return dat;	 //将读书的数据返回     
}

#endif