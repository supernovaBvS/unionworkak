static float cmd_str_10[10];//定义静态float型数组用来存放10个参数
static unsigned char cmd_str_42[42];//定义静态char型数组用来存放42个字节
//下面定义的是发送两数，通过串口通信发送42个字节的数据包給机械臂
void cmd_str_42_send() {
cmd_str_42[0] = 0xA5;//定义包头
for ( char i = 0; i < 10; i++ ) {
*((float *) (cmd_str_42 + 1 + 4*i)) = float(cmd_str_10[i]);
}
cmd_str_42[41]= 0x5A;//定义包尼
//下面开始把char型数组的内容写到机械臂中去
for ( char i = 0; i < 42; i++ ) {
Serial.write( cmd_str_42[i]);
}
}


//Fits X state3
void dobot_cmd_3( float x=260, float y=0, float z=0, float r=0, float degree=0 ) {
for ( char i = 0; i < 10; i++ ){
cmd_str_10[i] = 0;
}
//设買x，y，z，x，运动校式，爪子的开合角度
cmd_str_10[0] = 3;
cmd_str_10[2] = x; //×
cmd_str_10[3] = y; //y
cmd_str_10[4] = 2; //2
cmd_str_10[5] = r; //r
cmd_str_10[7] = 1; //运动棪式
cmd_str_10[8] = degree; //i FIJJF7/00!0
cmd_str_42_send();
}


void setup() {
// Serial connected with dobot
Serial. begin (9600);
}

void loop () {
dobot_cmd_3( 260, 0, 130,0,0);//初始化机城劈的依覺
dobot_cmd_3( 260, 0, 20,0,0);//机械野沿z拾方向下降
delay(3000);//延时三秒以很让：人旅入委抓的物品(示销是徐皮）
dobot_cmd_3(260, 0, 20,0,32.5);//机城背开始抵取物品(示例是橡皮），提前用Dobot client 软dbot-cad_3( 260, 0 130,0.32.5）：//浴2抽方向，上升机城臂
delay(2000);//延时两秒，以使观众吞机战臂的动作清楚点
//以下实現旋教两圈《底盛+爪不）
for (char i=0; i<2; i++) {
dobot_cmd_3 (260, 100, 130, 90, 32.5);
dobot_cmd_3 (260, -100, 130, -90, 32.5);
}
dobot_cmd_3(260,0,130,0,32.5); //同到机械岸的原始位冥上方，爪予不松开
dobot_cmd_3(300,0,20,0,32.5);//机校片下降，同时向前效回物品(示例是橡皮）
dobot_cmd_3(300,0,20,0,0); //机械特松开瓜手，放开物品(示倒是橡皮）
delay(2500); //此处尤为重罗，经过芥干次次实验必领延时大于等于1.5秒机战臂才会国到初始位震（原因米知）
dobot_cmd_3(260, 0, 130,0,0); //机战群同归初始位
while(1);
}

