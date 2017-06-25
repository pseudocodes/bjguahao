#!/usr/bin/env python
# -*- coding: utf-8

import time
import json
import sys
import os
import inspect


reload(sys)
sys.setdefaultencoding( "utf-8" )

class Debug_level():
    debug = 1
    info = 2
    error = 3


global debug_level
global filesystemencoding

class Log(object):
    """
    日志
    """

    @staticmethod
    def load_config():
        """获取log配置"""
        global debug_level
        global filesystemencoding

        filesystemencoding = sys.getfilesystemencoding()

        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
                data = data[0]
                if data["DebugLevel"] == "info":
                    debug_level = Debug_level.info
                elif data["DebugLevel"] == "debug":
                    debug_level = Debug_level.debug
                elif data["DebugLevel"] == "error":
                    debug_level = Debug_level.error

                Log.info("DebugLevel设置为:" + str(debug_level))
                Log.debug("DebugTest" )

    	except  Exception, e:
            debug_level = Debug_level.info
            Log.error(repr(e))
            Log.error("获取Log模块配置失败，DebugLevel设置为默认值:info")


    @staticmethod
    def get_time():
        """
        获取时间
        """
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    @staticmethod
    def set_encoding(msg):
        """
        windows console didn't support utf-8
        """
        global filesystemencoding

        if filesystemencoding == 'mbcs':
            msg = msg.encode("GBK")
        if filesystemencoding== 'utf-8':
            msg = msg.encode("utf-8")
        return msg

    @staticmethod
    def info(msg):
        """
        info
        """
        global debug_level
        msg = Log.set_encoding(msg)
        if debug_level <= Debug_level.info:
            print("\033[0;37m " + Log.get_time() + " [info] " + msg + "\033[0m")

    @staticmethod
    def debug(msg):
        """
        debug
        """
        global debug_level
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        msg = Log.set_encoding(msg)
        if debug_level <= Debug_level.debug:
            # fname = os.path.basename(sys._getframe(1).co_filename)

            fname = os.path.basename(info.filename) 
            lineno = sys._getframe().f_back.f_lineno

            out = "\033[0;34m {} [debug] {}:{} {} \033[0m"
            print(out.format(Log.get_time(), fname, lineno, msg))
            # print("\033[0;34m " + Log.get_time() + " [debug] " + msg + "\033[0m")


    @staticmethod
    def error(msg):
        """
        输出错误
        """
        global debug_level
        
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
     
        msg = Log.set_encoding(msg)
        if debug_level <= Debug_level.error:
            fname = os.path.basename(info.filename)
            lineno = sys._getframe().f_back.f_lineno
            out = "\033[0;31m {} [error] {}:{} {} \033[0m"
            print(out.format(Log.get_time(), fname, lineno, msg))
            # print("\033[0;31m " + Log.get_time()  + " [error] " + msg  + "\033[0m")

    @staticmethod
    def exit(msg):
        """
        打印信息，并退出
        """
        Log.error(msg)
        Log.error("exit")
        exit(0)

