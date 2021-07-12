'''
Author: 大碗豆汁儿
Date: 2021-06-14 14:33:07
LastEditTime: 2021-07-12 15:25:16
Description: collimator
'''
import win32gui
import win32api
import win32con
import time
import json


def RGB_to_Hex(rgb):
    """[summary]

    Args:
        rgb ([list]): [3色rgb]

    Returns:
        [int]: [16进制rgb]
    """
    RGB = rgb
    color = ''
    for i in RGB:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return int(color, 16)


def drawCollimator(collimatorColorRGB, collimatorMapList=[]):
    """[summary]用于绘画准星

    Args:
        collimatorColorRGB ([list]): [3色rgb]
        collimatorMapList ([list[list]]): [2维列表，准星图案]
    """
    desktopWindow = win32gui.GetDesktopWindow()  # 桌面窗体
    windowDC = win32gui.GetWindowDC(desktopWindow)
    screenX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
    screenY = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
    collimatorColor = RGB_to_Hex(collimatorColorRGB)  # 获取准星颜色
    collimatorMapListRange = len(collimatorMapList)
    while True:
        if collimatorMapList != []:
            for x in range(-int(collimatorMapListRange/2), int(collimatorMapListRange/2)):
                for y in range(-int(collimatorMapListRange/2), int(collimatorMapListRange/2)):
                    if collimatorMapList[x+int(collimatorMapListRange/2)][y+int(collimatorMapListRange/2)] == 1:
                        win32gui.SetPixel(windowDC, int(screenX/2)+x, int(screenY/2)+y, collimatorColor)
        else:
            for x in range(-3, 3):
                for y in range(-3, 3):
                    win32gui.SetPixel(windowDC, int(screenX/2)+x, int(screenY/2)+y, collimatorColor)
        time.sleep(0.01)  # 这行决定CPU负载 数值高了准星会闪烁，低了会占用CPU
    win32gui.ReleaseDC(desktopWindow, windowDC)


try:
    settingJson = open("collimatorSetting.json", "r", encoding="utf-8")
    settingContent = settingJson.read()
    setting = json.loads(settingContent)
    collimatorMapList = setting['collimatorMapList']
    collimatorColorRGB = setting['collimatorColorRGB']
    print('''
================================================================================================
辅助准星
作者：bilibili.大碗豆汁儿

使用教程：
1.请保证游戏以窗口化或无边框窗口化运行，全屏状态可能无法显示准星
2.collimatorSetting.json为设置文件，请与本exe文件放置于同一路径下
3.请勿使用分辨率缩放，会导致准星位置错误
4.若发现cpu占用高，请关闭本软件并购买新cpu
5.已经过测试，游戏封禁与本软件无关
6.打包软件版本暂时只支持Windows系统，其他系统请使用python自行编译运行
7.有任何问题请联系作者--->https://space.bilibili.com/175397396

collimatorSetting.json设置：
1.collimatorMapList为准星图像，可自定义准星大小和形状；整体二维列表也可修改大小，默认为20*20，为保证准星位置正确建议设置二维列表宽高均为偶数。
  当collimatorMapList为[]时，软件默认使用6*6方形准星。
2.collimatorColorRGB为准星颜色，请使用正确RGB值

开源链接：https://github.com/RelaxJH-DouZhiR/DouZhiRcollimator
致谢：TheIronMe

██████╗  ██████╗ ██╗   ██╗███████╗██╗  ██╗██╗██████╗
██╔══██╗██╔═══██╗██║   ██║╚══███╔╝██║  ██║██║██╔══██╗
██║  ██║██║   ██║██║   ██║  ███╔╝ ███████║██║██████╔╝
██║  ██║██║   ██║██║   ██║ ███╔╝  ██╔══██║██║██╔══██╗
██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║██║██║  ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
================================================================================================
          ''')
    drawCollimator(collimatorColorRGB, collimatorMapList)
except Exception as e:
    print(f'''
███████╗██████╗ ██████╗  ██████╗ ██████╗
██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
█████╗  ██████╔╝██████╔╝██║   ██║██████╔╝
██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗
███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
{e}
          ''')
