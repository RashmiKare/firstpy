#!/usr/bin/env python

import ctypes
import sys
import time
import ft81x_def

HW_444=1
#HW_444=0

###################### common APIs ####################

def ft81x_write(ch_instance,addr,buf):
    '''
    Writes contents of "buf" which is string type to FT81x address "addr"
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        addr            - Integer type
        buf             - string

    Return:
        None
    '''     
    ch_instance.wrstr(addr,buf)


def ft81x_read(ch_instance,addr,len):    
    '''
    Reads len bytes from addr
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        addr            - Integer type
        len             - Integer type

    Return:
        String
    '''
    return ch_instance.rdstr(addr,len)

def ft81x_readbyte(ch_instance,addr):    
    '''
    Read 1 byte from addr
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        addr            - Integer type

    Return:
        Integer
    '''
    response_str = ch_instance.rdstr(addr,1)   
    response_byte = ord(response_str)
    return response_byte


def ft81x_readhalfword(ch_instance,addr): 
    '''
    Read 2 byte from addr
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        addr            - Integer type

    Return:
        Integer
    '''    
    response_str = ch_instance.rdstr(addr,2)   
    response_2byte = (ord(response_str[0]) & 0xFF) | ((ord(response_str[1]) & 0xFF) << 8) # [0] [1] = LSB MSB   
    return response_2byte


def ft81x_readword(ch_instance,addr):    
    '''
    Read 4 byte from addr
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        addr            - Integer type

    Return:
        Integer
    '''    
    response_str = ch_instance.rdstr(addr,4)   
    # [0] [1] [2] [3] = LSB .... MSB
    response_4byte = (ord(response_str[0]) & 0xFF) | ((ord(response_str[1]) & 0xFF) << 8) | ((ord(response_str[2]) & 0xFF) << 16) | ((ord(response_str[3]) & 0xFF) << 24)
    return response_4byte


def ft81x_construct_value_string(val):
    '''
    Converts integer "val" to string that is acceptable by FT81x
    i.e LSB of val at 0th index in string
    
    Args:
        val     - Integer value
        
    Return:
        string
    '''    
    val_list = []
    while(val):
        val_list.append(val & 0xFF)
        val = val >> 8
    #print "val_list",val_list,"len(val_list)",len(val_list)
    val_string = ''.join( chr(e) for e in val_list)
    return val_string   

def ft81x_construct_fix_value_string(val,fix): 
    '''
    Converts integer "val" to fixed lenth string that is acceptable by FT81x
    Padded bytes are zeroes
    i.e LSB of val at 0th index in string
    
    Args:
        val     - Integer value
        fix     - Size to fix in the return string
        
    Return:
        string
    '''       
    val_list = []
    while(val):        
            val_list.append(val & 0xFF)
            val = val >> 8            
    #print "val_list",val_list,"len(val_list)",len(val_list)
    if (len(val_list) != fix) :
        fix -= len(val_list)
        while(fix):
            val_list.extend([0x00])     
            fix -= 1        
    val_string = ''.join( chr(e) for e in val_list)
    return val_string   

def ft81x_init(ch_instance):  
    '''
    Initializes FT81x
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"        

    Return:
        None
    '''   
    ft81x_reg_write(ch_instance,ft81x_def.REG_SPI_WIDTH,2)   
    print "FT81x SPI set in QUAD mode with one dummy"    
    ch_instance.switchmode(mode = 4)
    print "FT422 communication switched to QUAD mode"    
    
    n = ft81x_readbyte(ch_instance,ft81x_def.REG_ID)
    print "REG_ID = 0x%02x" %n
    while (n != 0x7C):
        n = ft81x_readbyte(ft4222,REG_ID)

    ft81x_reg_write(ch_instance,ft81x_def.REG_HCYCLE,0x3A0,2)
    ft81x_reg_write(ch_instance,ft81x_def.REG_HOFFSET,0x58)
    ft81x_reg_write(ch_instance,ft81x_def.REG_HSYNC0,0x0)
    ft81x_reg_write(ch_instance,ft81x_def.REG_HSYNC1,0x30)
    ft81x_reg_write(ch_instance,ft81x_def.REG_VCYCLE,0x20D,2)
    ft81x_reg_write(ch_instance,ft81x_def.REG_VOFFSET,0x20)
    ft81x_reg_write(ch_instance,ft81x_def.REG_VSYNC0,0x0)
    ft81x_reg_write(ch_instance,ft81x_def.REG_VSYNC1,0x3)
    ft81x_reg_write(ch_instance,ft81x_def.REG_SWIZZLE,0x0)
    ft81x_reg_write(ch_instance,ft81x_def.REG_PCLK_POL,0x1)
    ft81x_reg_write(ch_instance,ft81x_def.REG_HSIZE,0x320,2)
    ft81x_reg_write(ch_instance,ft81x_def.REG_VSIZE,0x1E0,2)
    ft81x_reg_write(ch_instance,ft81x_def.REG_CSPREAD,0x0)
    ft81x_reg_write(ch_instance,ft81x_def.REG_DITHER,0x1)
    ft81x_reg_write(ch_instance,ft81x_def.REG_GPIOX_DIR,0xFFFF,2)
    ft81x_reg_write(ch_instance,ft81x_def.REG_GPIOX,0xFFFF,2)       
    ft81x_dl_write(ch_instance,'CLEAR_COLOR_RGB',0,0,0)
    ft81x_dl_write(ch_instance,'CLEAR',1,1,1)    
    ft81x_dl_write(ch_instance,'DISPLAY')    
    ft81x_reg_write(ch_instance,ft81x_def.REG_DLSWAP,ft81x_def.DLSWAP_FRAME)
    ft81x_reg_write(ch_instance,ft81x_def.REG_PCLK,2) 
    print "FT81x initialized!"


###################### APIs interacting with RAM_REG ####################

def ft81x_reg_write(ch_instance,reg,val,val_width_in_bytes = 1): 
    '''
    Writes "val" to register "reg"
    
    Args:
        ch_instance         - SPI interface Handler obtained through "class Channel"
        reg                 - Register address in integer type
        val                 - Value in integer type
        val_width_in_bytes  - Value width in bytes integer type

    Return:
        None
    '''
    if (reg == ft81x_def.REG_DLSWAP):         
        ft81x_dl_write(0,'REG_DLSWAP',0,0,0,0)
    ch_instance.wrstr(reg,ft81x_construct_fix_value_string(val,val_width_in_bytes))   
    #print "Writing register",reg,"with value",val


###################### APIs interacting with RAM_DL ####################

def ft81x_is_dl_command(dl_cmd):
    '''
    Checks if dl_cmd is a valid DL command
    
    Args:        
        dl_cmd         - integer value

    Return:
        True or False depending on valid or invalid DL command
    '''
    existance = dl_cmd in ft81x_def.DL_COMMAND_LIST   
    return existance


def ft81x_construct_dl_command(param1 = 0, param2 = 0, param3 = 0, param4 = 0, param5 = 0, param6 = 0):
    '''
    Constructs DL command with parameters in FT81x accetable format    
    
    Args:
        param1                - DL command as string
        param2 to param6      - parameters for the DL command specified in param1
        
    Return:
        String of DL command with parameters in FT81x accetable format    
        LSB of val of constructed command is located at 0th index in string    
    '''    
    if ft81x_is_dl_command(param1) == False:
        raise IOError("Invalid DL command %s" % param1)  
    else:  
        if param1 == 'BEGIN':
            # start drawing a graphics primitive
            cmd = (0x1F<<24) | (param2 & 0xF)            
        elif param1 == 'END':
            # end drawing a graphics primitive 
            cmd = (0x21<<24)            
        elif param1 == 'VERTEX2II':
            # supply a vertex with unsigned coordinates
            cmd = (0x2 << 30) | ((param2 & 0x1FF) << 21) | ((param3 & 0x1FF) << 12) | ((param4 & 0x1F) << 7)| (param5 & 0x7F)            
        elif param1 == 'VERTEX2F':
            # supply a vertex with fractional coordinates
            cmd = (0x1 << 30) | ((param2 & 0x7FFF) << 15) | ((param3 & 0x7FFF)<<0)            
        elif param1 == 'DISPLAY':
            # end the display list            
            cmd = (0x0 <<24)            
        elif param1 == 'ALPHA_FUNC':
            # set the alpha test function 
            cmd = (0x9<<24) | ((param2 & 0x7)<<8) | (param3 & 0xFF)                     
        elif param1 == 'VERTEX_FORMAT':
            # set the precision of VERTEX2F coordinates           
            cmd = (0x27 << 24) | (param2 & 0x7)
        elif param1 == 'CLEAR':
            # clear buffers to preset values 
            cmd = (0x26<<24) | ((param2 & 0x1) << 2) | (( param3 & 0x1) << 1) | (param4 & 0x1)
        elif param1 == 'CLEAR_COLOR_RGB':
            # set clear values for red, green and blue channel           
            cmd = (0x2 << 24) | ((param2 & 0xFF) << 16) | ((param3 & 0xFF) << 8)| ( param4 & 0xFF) 
        elif param1 == 'CLEAR_COLOR_A':
            # set clear value for the alpha channel
            cmd = (0x0f << 24) | (param2 & 0xFF)
        elif param1 == 'COLOR_RGB':
            # set the current color red, green and blue 
            cmd = (0x04 << 24) | ((param2 & 0xFF) << 16) | ((param3 & 0xFF) << 8) | (param4 & 0xFF)
        elif param1 == 'COLOR_A':
            # set the current color alpha
            cmd = (0x10 << 24) | (param2 & 0xFF)
        elif param1 == 'LINE_WIDTH':
            # set the line width
            cmd = (0x0E << 24) | (param2 & 0xFFF)
        elif param1 == 'POINT_SIZE':
            # set point size
            cmd = (0x0D << 24) | (param2 & 0x1FFF)
        elif param1 == 'BITMAP_HANDLE':
            # set the bitmap handle            
            cmd = (0x05 << 24) | (param2 & 0x1F)
        elif param1 == 'BITMAP_LAYOUT':
            # set the source bitmap memory format and layout for the current handle 
            cmd = (0x07 << 24) | ((param2 & 0x1F) << 19) | ((param3 & 0x3FF) << 9) | (param4 & 0x1FF)
        elif param1 == 'BITMAP_LAYOUT_H':
            # set the high bits of BITMAP_LAYOUT
            cmd = (0x28 << 24) | ((param2 & 0x3) << 2) | (param3 & 0x3)
        elif param1 == 'BITMAP_SIZE':
            # set the screen drawing of bitmaps for the current handle
            cmd = (0x08 << 24) | ((param2 & 0x1) << 20) | ((param3 & 0x1) << 19) | ((param4 & 0x1) << 18) | ((param5 & 0x1FF) << 9) | (param6 & 0x1FF)
        elif param1 == 'BITMAP_SIZE_H':
            # set the high bits of BITMAP_SIZE
            cmd = (0x29 << 24) | ((param2 & 0x3) << 2) | (param3 & 0x3)
        elif param1 == 'BITMAP_SOURCE':
            # set the source address for bitmap graphics
            cmd = (0x1 << 24) | (param2 & 0x3FFFFF)
        elif param1 == 'BITMAP_TRANSFORM_A':
            # set the components of the bitmap transform matrix
            cmd = (0x15 << 24) | (param2 & 0x1FFFF)
        elif param1 == 'BITMAP_TRANSFORM_B':
            # set the components of the bitmap transform matrix
            cmd = (0x16 << 24) | (param2 & 0x1FFFF)
        elif param1 == 'BITMAP_TRANSFORM_C':
            # set the components of the bitmap transform matrix
            cmd = (0x17 << 24) | (param2 & 0xFFFFFF)
        elif param1 == 'BITMAP_TRANSFORM_D':
            # set the components of the bitmap transform matrix
            cmd = (0x18 << 24) | (param2 & 0x1FFFF)
        elif param1 == 'BITMAP_TRANSFORM_E':
            # set the components of the bitmap transform matrix
            cmd = (0x19 << 24) | (param2 & 0x1FFFF)
        elif param1 == 'BITMAP_TRANSFORM_F':
            # set the components of the bitmap transform matrix
            cmd = (0x19 << 24) | (param2 & 0xFFFFFF)
        elif param1 == 'CELL':
            # Specify the bitmap cell number for the VERTEX2F command.
            cmd = (0x06 << 24) | (param2 & 0x7F)
        elif param1 == 'BLEND_FUNC':
            # specify pixel arithmetic
            cmd = (0x0B << 24) | ((param2 & 0x7) << 3) | (param3 & 0x7)
        elif param1 == 'CLEAR_STENCIL':
            # set clear value for stencil buffer
            cmd = (0x11 << 24) | ((param2 & 0xFF) << 3)
        elif param1 == 'SCISSOR_XY':
            # specify the top left corner of the scissor clip rectangle
            cmd = (0x1B << 24) | ((param2 & 0x7FF) << 11) | (param3 & 0x7FF)
            print cmd
        elif param1 == 'SCISSOR_SIZE':
            # specify the size of the scissor clip rectangle
            cmd = (0x1C << 24) | ((param2 & 0xFFF) << 12) | (param3 & 0xFFF)
            print cmd

        s = chr(cmd & 0xFF) + chr((cmd>>8) & 0xFF) + chr((cmd>>16) & 0xFF) + chr(((cmd>>24) & 0xFF))
        #print "\n cmd:"," ".join(hex(ord(n)) for n in s)
        return s


def ft81x_dl_write(ch_instance,dl_cmd,arg1 = 0,arg2 = 0,arg3 = 0,arg4 = 0,arg5 = 0):    
    '''
    Writes RAM_DL
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        dl_cmd          - Display List command in integer value
        arg1 to arg5    - Parameters required for dl_cmd in integer value
    Return:
        None
    ''' 
    if not hasattr(ft81x_dl_write,"ram_dl_ptr"):        
        ft81x_dl_write.ram_dl_ptr = ft81x_def.RAM_DL  # RAM_DL mem location  
    if (dl_cmd == 'REG_DLSWAP'):
        ft81x_dl_write.ram_dl_ptr = ft81x_def.RAM_DL
        #print "ram_dl_ptr reset = ",ft81x_dl_write.ram_dl_ptr
    else:
        #print "ft81x_dl_write.ram_dl_ptr = ",ft81x_dl_write.ram_dl_ptr
        while( ft81x_readhalfword(ch_instance,ft81x_def.REG_CMD_READ)!= ft81x_readhalfword(ch_instance,ft81x_def.REG_CMD_WRITE)):
            print "Co-processor engine is curretly functional"
        curr_dl_offset = ft81x_readhalfword(ch_instance,ft81x_def.REG_CMD_DL)          
        ft81x_dl_write.ram_dl_ptr += curr_dl_offset 
        if(ft81x_dl_write.ram_dl_ptr >= (ft81x_def.RAM_DL + 0x2000)): # RAM_DL is 8K
            print "Write failed !!!RAM_DL full!!! ",ft81x_dl_write.ram_dl_ptr
            return
        ch_instance.wrstr(ft81x_dl_write.ram_dl_ptr,ft81x_construct_dl_command(dl_cmd,arg1,arg2,arg3,arg4))
        #print "DL written location = ",hex(ft81x_dl_write.ram_dl_ptr)
        ft81x_dl_write.ram_dl_ptr += 4 # next word aligned location for DL command
        ft81x_dl_write.ram_dl_ptr = ((ft81x_dl_write.ram_dl_ptr + 0x3) & ~0x3 ) # force word alignmenet     


###################### APIs interacting with RAM_CMD ####################

def ft81x_ram_cmd_freespace(ch_instance):
    '''
    Returns available space in RAM_CMD
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        
    Return:
        Integer value
    ''' 
    fullness = (ft81x_readhalfword(ch_instance,ft81x_def.REG_CMD_WRITE) - ft81x_readhalfword(ch_instance,ft81x_def.REG_CMD_READ)) % 4096
    freespace = 4096 - 4 - fullness    
    return freespace


def ft81x_is_copro_command(copro_cmd):
    '''
    Checks if copro_cmd is a valid coprocessor command
    
    Args:        
        copro_cmd         - integer value

    Return:
        True or False depending on valid or invalid coprocessor command
    '''
    ex = copro_cmd in ft81x_def.COPRO_COMMAND_LIST
    return ex    

def ft81x_construct_copro_command(param1 = 0, param2 = 0, param3 = 0, param4 = 0, param5 = 0, param6 = 0 , param7 = 0, param8 = 0):                
    '''
    Constructs coprocessor command with parameters in FT81x accetable format    
    
    Args:
        param1                - coprocessor command as string
        param2 to param6      - parameters in integer type for the coprocessor command specified in param1
        
    Return:
        String of coprocessor command with parameters in FT81x accetable format    
        LSB of val of constructed command is located at 0th index in string    
    '''
    if ft81x_is_copro_command(param1) == False:       
        raise IOError("Invalid co-processor command %s" % param1)          
    else:
        #print "param1",param1
        if param1 == 'CMD_BUTTON':  
            # 0xffffff0d,x,y,w,h,font,options,string          
            print "called"
            assert isinstance(param8,basestring),"parameter error"          
            cmd_str = ft81x_construct_fix_value_string(0xFFFFFF0D,4)           
            cmd_str += ft81x_construct_fix_value_string(param2,2)                    
            cmd_str += ft81x_construct_fix_value_string(param3,2)            
            cmd_str += ft81x_construct_fix_value_string(param4,2)            
            cmd_str += ft81x_construct_fix_value_string(param5,2)            
            cmd_str += ft81x_construct_fix_value_string(param6,2)
            cmd_str += ft81x_construct_fix_value_string(param7,2)            
            cmd_str += param8                             
        elif param1 == 'CMD_SWAP':
            cmd_str = ft81x_construct_fix_value_string(0xFFFFFF01,4) 
        elif param1 == 'CMD_DLSTART':
            cmd_str = ft81x_construct_fix_value_string(0xFFFFFF00,4) 
 
        prt_str = " ".join(hex(ord(ele)) for ele in cmd_str)
        print prt_str
        return cmd_str

def ft81x_copro_cmd_bufwrite(ch_instance,copro_cmd,arg1 = 0, arg2 = 0, arg3 = 0, arg4 = 0, arg5 = 0, arg6 = 0, arg7 = 0):     
    '''
    Writes RAM_CMD memory region
    
    Args:
        ch_instance     - SPI interface Handler obtained through "class Channel"
        copro_cmd       - Coprocessor command as string
        arg1 to arg7    - arguments for the coprocessor command in integres
        
    Return:
        None
    '''
    if not hasattr(ft81x_copro_cmd_bufwrite,"buf_ptr"):        
        ft81x_copro_cmd_bufwrite.buf_ptr = 0 
    if not hasattr(ft81x_copro_cmd_bufwrite,"buf"):
        ft81x_copro_cmd_bufwrite.buf =  []  
    #if not hasattr(ft81x_copro_cmd_bufwrite,"wr_ram_cmd_ptr"):
        #ft81x_copro_cmd_bufwrite.wr_ram_cmd_ptr =  ft81x_def.RAM_CMD  

    if copro_cmd == 'UPDATE_RAM_CMD':
        # time to update RAM_CMD region        
        print "Buffer content being updated to RAM_CMD -> ",ft81x_copro_cmd_bufwrite.buf
        #ch_instance.wrstr(ft81x_copro_cmd_bufwrite.wr_ram_cmd_ptr,"".join(ele for ele in ft81x_copro_cmd_bufwrite.buf))        
        ch_instance.wrstr(ft81x_def.RAM_CMD,"".join(ele for ele in ft81x_copro_cmd_bufwrite.buf))        
        ft81x_reg_write(ch_instance,ft81x_def.REG_CMD_WRITE,ft81x_copro_cmd_bufwrite.buf_ptr,2)        
        while(ft81x_ram_cmd_freespace(ch_instance) != 4092):
            print 'waiting.....' 
            continue
        ft81x_copro_cmd_bufwrite.buf_ptr = 0
        return    
    if(ft81x_copro_cmd_bufwrite.buf_ptr > 4092):
        print 'BUF full , time to update RAM_CMD'
        return 
    else :    
        if ft81x_is_copro_command(copro_cmd):        
            cmd_str = ft81x_construct_copro_command(copro_cmd,arg1,arg2,arg3,arg4,arg5,arg6,arg7)
        elif ft81x_is_dl_command(copro_cmd):        
            cmd_str = ft81x_construct_dl_command(copro_cmd,arg1,arg2,arg3,arg4)
        else : 
            print 'Neither coprocessor command nor dl command....'
            return    
        #print "cmd_str",cmd_str
        cmd_len = len(cmd_str)       
        if (cmd_len):                   
            ft81x_copro_cmd_bufwrite.buf += list(cmd_str)
            pad_len = padding = 0
            if (cmd_len % 4):
                # not multiple of 4, padding needed
                padding = 4 - (cmd_len%4)
                pad_len = padding            
                while padding :
                    ft81x_copro_cmd_bufwrite.buf.append(chr(0))
                    padding -= 1            
            ft81x_copro_cmd_bufwrite.buf_ptr = ft81x_copro_cmd_bufwrite.buf_ptr + cmd_len + pad_len            
        else :
            print 'Command string empty'

def check(f):
    if f != 0:
        names = [
            "FT_OK",
            "FT_INVALID_HANDLE",
            "FT_DEVICE_NOT_FOUND",
            "FT_DEVICE_NOT_OPENED",
            "FT_IO_ERROR",
            "FT_INSUFFICIENT_RESOURCES",
            "FT_INVALID_PARAMETER",
            "FT_INVALID_BAUD_RATE",
            "FT_DEVICE_NOT_OPENED_FOR_ERASE",
            "FT_DEVICE_NOT_OPENED_FOR_WRITE",
            "FT_FAILED_TO_WRITE_DEVICE",
            "FT_EEPROM_READ_FAILED",
            "FT_EEPROM_WRITE_FAILED",
            "FT_EEPROM_ERASE_FAILED",
            "FT_EEPROM_NOT_PRESENT",
            "FT_EEPROM_NOT_PROGRAMMED",
            "FT_INVALID_ARGS",
            "FT_NOT_SUPPORTED",
            "FT_OTHER_ERROR"]
        raise IOError("Error in MPSSE function (status %d: %s)" % (f, names[f]))


def bseq(*a):
    return "".join([chr(x) for x in a])

class DEVICE_LIST_INFO_NODE(ctypes.Structure):
    _fields_ = [("Flags",ctypes.c_uint),
                ("Type",ctypes.c_uint),
                ("ID",ctypes.c_uint),
                ("LocId",ctypes.c_uint),
                ("SerialNumber", type(ctypes.create_string_buffer(16))),
                ("Description",type(ctypes.create_string_buffer(64))),
                ("FT_HANDLE",ctypes.c_void_p) ]

class Channel(object):
    ftd2xx_path = r"C:\\projects\\FT4222\\ft4222evm\\CDM v2.10.00.FT4222.B11\\CDM v2.10.00.FT4222.B11\\i386\\ftd2xx.dll"
    ft4222_path = r"C:\\projects\\FT4222\\ft4222evm\\ft4222_example\\example\\imports\\LibFT4222\\lib\\LibFT4222.dll"

    #mode = 1 for Single , 2 for Dual, 4 for Quad
    def open(self, speed, mode):
        if sys.platform.startswith('linux'):
            self.d2xx = ctypes.cdll.LoadLibrary("libftd2xx.so")
        elif sys.platform.startswith('darwin'):
            self.d2xx = ctypes.cdll.LoadLibrary("libftd2xx.1.1.0.dylib")
        else:
            self.d2xx = ctypes.windll.LoadLibrary("ftd2xx")

        numdevs = ctypes.c_int(0)               
        sstat = self.d2xx.FT_CreateDeviceInfoList(ctypes.byref(numdevs))
        if sstat == 0:            
            print "Number of D2XX devices detected are:", numdevs.value
        else:
            print "FT_CreateDeviceInfoList failed with status:", sstat

        curr_d2xx_info_list_type = DEVICE_LIST_INFO_NODE * 2
        curr_d2xx_info_list = curr_d2xx_info_list_type()
        sstat = self.d2xx.FT_GetDeviceInfoList(ctypes.pointer(curr_d2xx_info_list),ctypes.byref(numdevs))
        for i in curr_d2xx_info_list:
            print i,"th deatils"
            print "Flags",i.Flags
            print "Type",i.Type
            print "ID",i.ID
            print "LocId",i.LocId
            print "SerialNumber",i.SerialNumber
            print "Description",i.Description
            print "FT_HANDLE",i.FT_HANDLE
            print "\n"
        
        self.speed = speed   #will be overwritten later with hardcoded value 
        self.mode = mode    
        self.ftHandle = ctypes.c_void_p()
        self.ftHandle2 = ctypes.c_void_p()

        #open the device in first location ID (for HW_368 UMFT4222EV module, prototype version 1.0)
        #check(self.d2xx.FT_OpenEx(0, 4,ctypes.byref(self.ftHandle)))
        #open the device in first interface named "FT4222" (for ME81x modules, 2 FT4222 interface)
        check(self.d2xx.FT_OpenEx("FT4222 A",  2, ctypes.byref(self.ftHandle)))
        check(self.d2xx.FT_OpenEx("FT4222 B",  2, ctypes.byref(self.ftHandle2)))
        
        self.ft4222 = ctypes.CDLL("LibFT4222")  
        #For HW_443 ME812/ME813 5" module, GPIO0=PD#(output), GPIO1=INT#(input), GPIO2/GPIO3=NC
        #For HW_444 ME810/ME811 7" module, GPIO0=PD#(output), GPIO1=CS#(output), GPIO2=INT#(input), GPIO3=NC
        pl=[0,1,1,1] # HW_443
        if HW_444:
            pl=[0,0,1,1]
        pa=(ctypes.c_uint * len(pl))(*pl)
        check(self.ft4222.FT4222_GPIO_Init(self.ftHandle2, pa)) #pa=GPIO_Dir[0,1,2,3], '0'means output, '1'means input
        self.ft4222.FT4222_GPIO_Write(self.ftHandle2,0,1)   #set PD# = High        
        #self.reset()        
        self.assert_reset(1) #Toggle PD#
        time.sleep(0.010)
        self.assert_reset(0)
        time.sleep(0.010) 
       
        # setting FT4222 internal clock to SYS_CLK_80
        check(self.ft4222.FT4222_SetClock(self.ftHandle, 3))
            
        #hardcoding divider to CLK_DIV_4 as SYS_CLK_80/CLK_DIV_4 = 20MHz is giving highest throughput
        self.speed = 2 
        check(self.ft4222.FT4222_SPIMaster_Init(self.ftHandle, self.mode,self.speed, 0, 0, 0x1))
        #SPI Single mode, Clock = 15MHz, SPI mode(0,0), Slave Select Pin = SS0O

        self.s = ctypes.create_string_buffer(65535)

    def addr(self, a):
        return chr(a >> 16) + chr((a >> 8) & 255) + chr(a & 255)

    def cs(self, level):
        self.ft4222.FT4222_GPIO_Write(self.ftHandle2,1,level)   #level=0: set CS# = Low; level=1: set CS# = High
        n=1

    def write(self, s):
        dwNumBytesSent = ctypes.c_uint()
        if self.mode == 4 or self.mode == 2:                          
            status = self.ft4222.FT4222_SPIMaster_MultiReadWrite(self.ftHandle,0, s, 0, len(s),0,ctypes.byref(dwNumBytesSent))                
            check(status)            
            print "Wr -> "," mode:",self.mode,", #bytes:",len(s),", Content :"," ".join(hex(ord(n)) for n in s)
            
        if self.mode == 1:          
            status = self.ft4222.FT4222_SPIMaster_SingleWrite(self.ftHandle,s, len(s),ctypes.byref(dwNumBytesSent), True)
            check(status)
            assert len(s) == dwNumBytesSent.value
            print "Wr -> "," mode:",self.mode,", #bytes",dwNumBytesSent.value,", Content:"," ".join(hex(ord(n)) for n in s)                    

    def wrstr(self, a, s):        
        if not isinstance(s, str):
            assert False
        n = len(s) 
        #print "len(s)=",len(s)       
        blk = 65532 # max is 65535 , but address needs 3 bytes
        if n > blk:
            self.wrstr(a, s[:blk])
            self.wrstr(a + blk, s[blk:])
            return        
        msg = self.addr((2**23) | a) + s        
        self.write(msg)        
        return 0    
    
    def read(self, n):
        dwNumBytesRead = ctypes.c_uint()
        if self.mode == 1:            
            status = self.ft4222.FT4222_SPIMaster_SingleRead(self.ftHandle,self.s, n,ctypes.byref(dwNumBytesRead),True)              
        if (self.mode == 4 or self.mode == 2): 
            assert False          
            status = self.ft4222.FT4222_SPIMaster_MultiReadWrite(self.ftHandle,self.s, 0,0,0,n,ctypes.byref(dwNumBytesRead))           
        check(status)        
        assert n == dwNumBytesRead.value
        return list(self.s)[:n] 

    def rdstr(self, a, n):
        if n == 0:
            return ""        
        if n > 65534: # 1 byte reserved for dummy in SPI QUAD mode            
            return self.rdstr(a, 65534) + self.rdstr(a + 65534, n - 65534)         
        s = self.addr(a)
        s = s + str(0x0) # add dummy byte as is configured for Quad SPI
        dwNumBytesSent = ctypes.c_uint()
        if self.mode == 1:            
            status = self.ft4222.FT4222_SPIMaster_SingleWrite(self.ftHandle,s, len(s),ctypes.byref(dwNumBytesSent), False)
            check(status)            
            print " Read from address = ",s, "Address length in bytes = ",dwNumBytesSent.value                            
            response = self.read(n)           
            print "Read bytes:",response            
            return "".join(response[:])
        if self.mode == 2 or self.mode == 4:
            dwNumBytesRead = ctypes.c_uint()            
            status = self.ft4222.FT4222_SPIMaster_MultiReadWrite(self.ftHandle,self.s, s,
                                                        0,len(s),n,ctypes.byref(dwNumBytesRead))             
            response = list(self.s)[:n]               
            print "Rd -> ", " mode:",self.mode," [address] = "," ".join(hex(ord(p)) for p in list(s)[0:(len(s)-1)]),"#bytes = ",dwNumBytesRead.value,", Content:"," ".join(hex(ord(n)) for n in response)                            
            print "Returning ....... ","".join(response[:])             
            return "".join(response[:])             
            
    def silent(self, s): # send a silent command - one that expects no response
        self.write(s)
        if self.npending() != 0:
            print "Error - MPSSE receive buffer should be empty, but contains", hexdump(self.read(self.npending()))          
 
    def npending(self):
        dwNumBytesToRead = ctypes.c_uint()
        check(self.d2xx.FT_GetQueueStatus(self.ftHandle, ctypes.byref(dwNumBytesToRead)))
        return dwNumBytesToRead.value    

    def close(self):    
        self.ft4222.FT4222_UnInitialize(self.ftHandle)
        self.d2xx.FT_Close(self.ftHandle)
        self.ft4222.FT4222_UnInitialize(self.ftHandle2)
        self.d2xx.FT_Close(self.ftHandle2)
        return 0

    def assert_reset(self, sense):
        n = 1
        if sense:
            #self.silent(bseq(0x80, 0x00, 0x1b))
            self.ft4222.FT4222_GPIO_Write(self.ftHandle2,0,0)   #set PD# = Low
            #print "Set GPIO0 to Low"
        else:
            self.ft4222.FT4222_GPIO_Write(self.ftHandle2,0,1)   #set PD# = High
            #print "Set GPIO0 to High"

    def reset(self):
        # print 'RESET!'
        self.assert_reset(1) 
        time.sleep(0.010)
        self.assert_reset(0)
        time.sleep(0.010)   

        msg = chr(0) + chr(0) + chr(0)
        self.write(msg) # SCU wake
        time.sleep(.1)
        
        msg = chr(0x68) + chr(0) + chr(0)
        self.write(msg) # core reset
        msg = chr(0) + chr(0) + chr(0)
        self.write(msg) # SCU wake
        msg = chr(0) + chr(0) + chr(0)
        self.write(msg) # SCU wake
        time.sleep(.5)    
        return

    def frob(self):
        while True:
            for s in (0,1):
                print s
                self.assert_reset(1 - s)
                time.sleep(1)

    def switchmode(self,mode):
        self.mode = mode
        check(self.ft4222.FT4222_SPIMaster_SetLines(self.ftHandle,self.mode))