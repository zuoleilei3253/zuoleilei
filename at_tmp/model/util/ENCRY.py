# -*- coding: utf-8 -*-
# @Time : 2018/6/9 16:28
# @Author : sunlin
# @File : encryption-.py
# @Software: PyCharm


from model.util.PUB_LOG import *

from Cryptodome.Cipher import AES
from binascii import b2a_hex, a2b_hex

KEY='WWW.TUANDAI.COM-'

class PrpCrypt(object):

    def __init__(self):
        self.key = KEY.encode('utf-8')
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        try:
            text = text.encode('utf-8')
            cryptor = AES.new(self.key, self.mode, b'0000000000000000')
            # 这里密钥key 长度必须为16（AES-128）,
            # 24（AES-192）,或者32 （AES-256）Bytes 长度
            # 目前AES-128 足够目前使用
            length = 16
            count = len(text)
            if count < length:
                add = (length - count)
                # \0 backspace
                # text = text + ('\0' * add)
                text = text + ('\0' * add).encode('utf-8')
            elif count > length:
                add = (length - (count % length))
                # text = text + ('\0' * add)
                text = text + ('\0' * add).encode('utf-8')
            self.ciphertext = cryptor.encrypt(text)
            # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
            # 所以这里统一把加密后的字符串转化为16进制字符串
            return b2a_hex(self.ciphertext).decode()
        except Exception as e:
            errorLog("加密失败！"+str(e))
            return

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        try:
            cryptor = AES.new(self.key, self.mode, b'0000000000000000')
            plain_text = cryptor.decrypt(a2b_hex(text.encode()))
            # return plain_text.rstrip('\0')
            return bytes.decode(plain_text).rstrip('\0')
        except Exception as e:
            # errorLog("解密失败！" + str(e))
            return


if __name__ == '__main__':
    pc = PrpCrypt()  # 初始化密钥
    # e = pc.encrypt("testtesttest") # 加密
    e='1019389ce6d9562c87c3ee42'
    d = pc.decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)