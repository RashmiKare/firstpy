#!/usr/bin/env python

"""
On Mac, need to make sure that the VSP driver not to attach, or you'll see FT_DEVICE_NOT_OPENED.
If you see this message, try removing /System/Library/Extensions/*FTDI*
"""

import sys
import ctypes
from ctypes import *
import time
import array
#from array import *
import struct
from debugtools import *
import itertools
import ft81x_def
import ft81x_api

if __name__ == '__main__':
    print "main"
    ft4222 = ft81x_api.Channel()
    ft4222.open(4,mode = 1)
    ft4222.reset()   
    ft81x_api.ft81x_init(ft4222) 
    time.sleep(2)
    
    #ft81x_api.ft81x_dl_write(ft4222,'CLEAR_COLOR_RGB',255,255,255)
    #ft81x_api.ft81x_dl_write(ft4222,'CLEAR',1,1,1)
    #ft81x_api.ft81x_dl_write(ft4222,'COLOR_RGB',0,0,128)

    ft81x_api.ft81x_dl_write(ft4222,'CLEAR_COLOR_RGB',0,0,200)
    ft81x_api.ft81x_dl_write(ft4222,'CLEAR',1,0,0)
    #ft81x_api.ft81x_dl_write(ft4222,'COLOR_RGB',0,0,255)
    
    ft81x_api.ft81x_dl_write(ft4222,'CLEAR_COLOR_RGB',200,0,0)
    ft81x_api.ft81x_dl_write(ft4222,'SCISSOR_XY',40,30)
    ft81x_api.ft81x_dl_write(ft4222,'SCISSOR_SIZE',80,60)    
    ft81x_api.ft81x_dl_write(ft4222,'CLEAR',1,1,1)
    #ft81x_api.ft81x_dl_write(ft4222,'BEGIN',ft81x_def.BITMAPS) # BITMAPS
    #ft81x_api.ft81x_dl_write(ft4222,'VERTEX2II',40, 30, 31,0x47)
    ft81x_api.ft81x_dl_write(ft4222,'DISPLAY')
    ft81x_api.ft81x_reg_write(ft4222,ft81x_def.REG_DLSWAP,ft81x_def.DLSWAP_FRAME)

    '''
    ft81x_dl_write(ft4222,'POINT_SIZE',16)
    ft81x_dl_write(ft4222,'BEGIN',2) # POINTS
    #ft81x_dl_write(ft4222,'VERTEX2II',2,2,0,0)
    #ft81x_dl_write(ft4222,'VERTEX2II',510,479,0,0)
    ft81x_dl_write(ft4222,'VERTEX_FORMAT',4)    
    for x,y in zip(range(0,800*16,25*8),range(0,480*16,15*8)):
        ft81x_dl_write(ft4222,'VERTEX2F',x,y)        
        #ft81x_dl_write(ft4222,'CLEAR',1,1,1)        
    ft81x_dl_write(ft4222,'END')
    
    ft81x_dl_write(ft4222,'COLOR_RGB',255,100,50)
    ft81x_dl_write(ft4222,'LINE_WIDTH',255)
    ft81x_dl_write(ft4222,'BEGIN',3) # LINES
    ft81x_dl_write(ft4222,'VERTEX2F',2000,2000)
    ft81x_dl_write(ft4222,'VERTEX2F',3000,3000)
    ft81x_dl_write(ft4222,'END')
    '''
    '''
    ft81x_dl_write(ft4222,'BEGIN',1) # BITMAPS
    ft81x_dl_write(ft4222,'VERTEX_FORMAT',0)
    for blue,transparency,x,y,handle,cell in itertools.izip_longest(range(0,255,10),range(255,0,-10),range(0,800,20),range(0,480,10),range(16,31,1),range(65,90,1),fillvalue=19):
        ft81x_dl_write(ft4222,'COLOR_RGB',0,0,blue)
        ft81x_dl_write(ft4222,'COLOR_A',transparency) # 0->fully transparent 255->fully opaque
        ft81x_dl_write(ft4222,'VERTEX2II',x,y,handle,cell)   
    ft81x_dl_write(ft4222,'END')
    '''
    '''
    ft81x_dl_write(ft4222,'COLOR_RGB',0,0,255)    
    ft81x_dl_write(ft4222,'BEGIN',1) # BITMAPS   
    #ft81x_dl_write(ft4222,'VERTEX_FORMAT',0)
    #ft81x_dl_write(ft4222,'BITMAP_SOURCE',0x2F2D1C)  #WORKING
    ft81x_dl_write(ft4222,'BITMAP_SOURCE',(0x2F181c + (50 * 7 * 16 )))    
    #ft81x_dl_write(ft4222,'CELL',48)    
    #ft81x_dl_write(ft4222,'COLOR_RGB',0,0,150)
    #ft81x_dl_write(ft4222,'BITMAP_HANDLE',2)
    ft81x_dl_write(ft4222,'BITMAP_LAYOUT',2,7,16)    
    #ft81x_dl_write(ft4222,'BITMAP_SIZE',0,0,0,8,16)
    ft81x_dl_write(ft4222,'BITMAP_SIZE',0,0,0,800,480)   
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_A',24)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_B',64)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_C',0)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_D',0)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_E',24)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_F',0)
    ft81x_dl_write(ft4222,'VERTEX2F',0*16,0*16)
    ft81x_dl_write(ft4222,'VERTEX2F',10*16,10*16)
    ft81x_dl_write(ft4222,'VERTEX2F',20*16,20*16)
    ft81x_dl_write(ft4222,'END') 
    
    ft81x_dl_write(ft4222,'BEGIN',1) # BITMAPS
    ft81x_dl_write(ft4222,'VERTEX2II',150, 150, 24,65)
    ft81x_dl_write(ft4222,'END')    
    '''
    #font_table_addr_str = ft81x_read(ft4222,ROM_FONT_ADDR,4)
    #print "type(font_table_addr_str) = ",type(font_table_addr_str),"len = ",len(font_table_addr_str),"font_table_addr_str = ", " ".join(hex(ord(ele)) for ele in list(font_table_addr_str))
    #font_table_addr = ord(font_table_addr_str[3])<<24 | ord(font_table_addr_str[2])<<16 | ord(font_table_addr_str[1])<<8 | ord(font_table_addr_str[0])
    #print "font_table_addr_str :",font_table_addr_str
    #font_table_addr = ft81x_readword(ft4222,ROM_FONT_ADDR)
    #print "font_table_addr", hex(font_table_addr)

    '''
    ft81x_read(ft4222,font_table_addr,148) # handle 16
    print "\n"
    ft81x_read(ft4222,font_table_addr+1*148,148) # handle 17
    print "\n"
    ft81x_read(ft4222,font_table_addr+2*148,148) # handle 18
    print "\n"
    ft81x_read(ft4222,font_table_addr+3*148,148) # handle 19
    print "\n"
    ft81x_read(ft4222,font_table_addr+4*148,148) # handle 20
    '''
    '''
    #ft81x_dl_write(ft4222,'CLEAR',1,1,1)
    ft81x_dl_write(ft4222,'COLOR_RGB',255,255,255)
    ft81x_dl_write(ft4222,'BITMAP_SOURCE',0)
    ft81x_dl_write(ft4222,'BITMAP_LAYOUT',7,80,40)
    ft81x_dl_write(ft4222,'BITMAP_SIZE',0,0,0,40,40)    
    ft81x_dl_write(ft4222,'BEGIN',1) # BITMAPS    
    #ft81x_dl_write(ft4222,'BITMAP_HANDLE',0)
    ft81x_dl_write(ft4222,'VERTEX2II',0,0,0,0)      
    ft81x_dl_write(ft4222,'END') 
    '''
    '''
    ft81x_dl_write(ft4222,'COLOR_RGB',100,100,255)
    ft81x_dl_write(ft4222,'BEGIN',1) # BITMAPS  
    ft81x_dl_write(ft4222,'VERTEX2II',50,30,31,0x47)
    ft81x_dl_write(ft4222,'COLOR_A',128)
    ft81x_dl_write(ft4222,'VERTEX2II',60,40,31,0x47)  
    ft81x_dl_write(ft4222,'END')

    ft81x_dl_write(ft4222,'COLOR_RGB',100,100,255)
    ft81x_dl_write(ft4222,'BEGIN',1) # BITMAPS  
    ft81x_dl_write(ft4222,'BLEND_FUNC',2,0) # SRC_ALPHA , ZERO 
    ft81x_dl_write(ft4222,'VERTEX2II',100,50,31,0x47)
    ft81x_dl_write(ft4222,'COLOR_A',128)
    ft81x_dl_write(ft4222,'VERTEX2II',120,60,31,0x47)  
    ft81x_dl_write(ft4222,'END')
    
    ft81x_dl_write(ft4222,'CLEAR_COLOR_RGB',0,0,255)    
    ft81x_dl_write(ft4222,'CLEAR',1,1,1)
    ft81x_dl_write(ft4222,'COLOR_RGB',255,0,0) 
    ft81x_dl_write(ft4222,'BEGIN',7) # EDGE_STRIP_A
    ft81x_dl_write(ft4222,'VERTEX2F',50*16,50*16)
    ft81x_dl_write(ft4222,'VERTEX2F',500*16,300*16)
    ft81x_dl_write(ft4222,'VERTEX2F',630*16,500*16)
    ft81x_dl_write(ft4222,'END')
    ft81x_dl_write(ft4222,'BEGIN',8) # EDGE_STRIP_b
    ft81x_dl_write(ft4222,'VERTEX2F',60*16,60*16)
    ft81x_dl_write(ft4222,'VERTEX2F',600*16,400*16)
    ft81x_dl_write(ft4222,'VERTEX2F',700*16,600*16)
    ft81x_dl_write(ft4222,'END')

    ft81x_dl_write(ft4222,'CLEAR_COLOR_RGB',0,0,255)    
    ft81x_dl_write(ft4222,'CLEAR',1,1,1)
    ft81x_dl_write(ft4222,'COLOR_RGB',0,255,0) 
    ft81x_dl_write(ft4222,'BEGIN',5) # EDGE_STRIP_R
    ft81x_dl_write(ft4222,'VERTEX2F',50*16,50*16)
    ft81x_dl_write(ft4222,'VERTEX2F',500*16,300*16)
    ft81x_dl_write(ft4222,'VERTEX2F',630*16,500*16)
    ft81x_dl_write(ft4222,'END')
    ft81x_dl_write(ft4222,'BEGIN',6) # EDGE_STRIP_L
    ft81x_dl_write(ft4222,'VERTEX2F',60*16,60*16)
    ft81x_dl_write(ft4222,'VERTEX2F',600*16,400*16)
    ft81x_dl_write(ft4222,'VERTEX2F',700*16,600*16)
    ft81x_dl_write(ft4222,'END')
    '''
    '''
    ft81x_api.ft81x_dl_write(ft4222,'CLEAR_COLOR_RGB',0,0,255)    
    ft81x_api.ft81x_dl_write(ft4222,'CLEAR',1,1,1)
    ft81x_api.ft81x_dl_write(ft4222,'COLOR_RGB',255,0,0) 
    ft81x_api.ft81x_dl_write(ft4222,'BEGIN',9) # RECT
    ft81x_api.ft81x_dl_write(ft4222,'VERTEX2F',60*16,50*16)
    ft81x_api.ft81x_dl_write(ft4222,'VERTEX2F',100*16,62*16)  
    #ft81x_dl_write(ft4222,'VERTEX2F',600*16,800*16)
    #ft81x_dl_write(ft4222,'VERTEX2F',800*16,800*16)    
    ft81x_api.ft81x_dl_write(ft4222,'END')
    '''
    '''
    picture_str = ''.join(chr(e) for e in ft81x_def.picture)
    ft81x_api.ft81x_write(ft4222,0,picture_str)
    read_str = ft81x_api.ft81x_read(ft4222,0,len(picture_str))    
    print picture_str == read_str

    ft81x_api.ft81x_dl_write(ft4222,'COLOR_RGB',255,255,255)    
    ft81x_api.ft81x_dl_write(ft4222,'BEGIN',1) # BITMAPS       
    ft81x_api.ft81x_dl_write(ft4222,'BITMAP_SOURCE',0)           
    ft81x_api.ft81x_dl_write(ft4222,'BITMAP_LAYOUT',7,550,183)        
    ft81x_api.ft81x_dl_write(ft4222,'BITMAP_SIZE',0,0,0,275,183)   
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_A',128)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_B',383)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_C',100)
    #ft81x_api.ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_D',128)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_E',-64)
    #ft81x_dl_write(ft4222,'BITMAP_TRANSFORM_F',100) 
    ft81x_api.ft81x_dl_write(ft4222,'VERTEX2F',100*16,100*16)    
    ft81x_api.ft81x_dl_write(ft4222,'END') 
    '''
    '''
    ft81x_api.ft81x_dl_write(ft4222,'DISPLAY')
    ft81x_api.ft81x_reg_write(ft4222,ft81x_def.REG_DLSWAP,ft81x_def.DLSWAP_FRAME)
    
    ft81x_api.ft81x_copro_cmd_bufwrite(ft4222,'CMD_DLSTART')
    ft81x_api.ft81x_copro_cmd_bufwrite(ft4222,'CMD_BUTTON',10,10,100,200,31,0,'test!')
    ft81x_api.ft81x_copro_cmd_bufwrite(ft4222,'DISPLAY')
    ft81x_api.ft81x_copro_cmd_bufwrite(ft4222,'CMD_SWAP')    
    ft81x_api.ft81x_copro_cmd_bufwrite(ft4222,'UPDATE_RAM_CMD')
    '''

    
    #ft81x_reg_write(ft4222,REG_HCYCLE,0x3A0);
    # wr_src = ""
    # x,y = 0,0
    # while x < 65538:        
        # wr_src += wr_src.join("r")
        # x = x + 1
        # y = y + 1
        
    # print "len of wr_src = %d" % len(wr_src)    
    # ft4222.wrstr(0x0, wr_src)    
    # #print "wr_src = %s" % wr_src
    
    # rd_str = ft4222.rdstr(0x0,len(wr_src))
    # #print "rd_str = %s" % rd_str
    # print wr_src == rd_str    
    
    #write REG_SPIMode to Dual mode with 1 dummy 
    # ft4222.wrstr(0x302188, chr(1))    
    # ft4222.switchmode(mode = 2)
    # n = ord(ft4222.rdstr(0x302000,1)) #3153920 REG_ID address
    # print "SPI DUAL mode, read REG_ID = 0x%02x" %n

    #write REG_SPIMode to Single mode with 1 dummy 
    # ft4222.wrstr(0x302188, chr(0))    
    # ft4222.switchmode(mode = 1)
    # n = ord(ft4222.rdstr(0x302000,1)) #3153920 REG_ID address
    # print "SPI SINGLE mode, read REG_ID = 0x%02x" %n

    #while True:
        #print "REG_ID = 0x%02x" % ord(ft4222.rdstr(3153920,1)) #3153920 REG_ID address
        #time.sleep(1)