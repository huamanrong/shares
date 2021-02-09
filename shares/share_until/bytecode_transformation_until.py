import struct


class HexAndStr:
    # 字符串转换成为16进制字符串（小写）    LED编码是 GB2312
    def string_to_HexString(self, str_string, charset='GB2312'):
        escapeArray = ["\b", "\t", "\n", "\f", "\r"]
        flag = False
        for i in escapeArray:
            if i in str_string:
                flag = True
                break
        if flag:
            print('参数字符串不能包含转义字符！')
            exit()
        hex_array = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        sb = ''
        bs = str_string.encode(charset)
        for i in range(len(bs)):
            bit = (bs[i] & 0x0f0) >> 4
            sb += hex_array[bit]
            bit = bs[i] & 0x0f
            sb += hex_array[bit]
        return sb.lower()

    # 16进制直接转换成为字符串
    def HexString_to_string(self, hexString, charset='GB2312'):
        hexString = hexString.upper()
        hexDigital = "0123456789ABCDEF"
        hexs = list(hexString)
        list_bytes = b''
        for i in range(len(hexString)//2):
            n = hexDigital.index(hexs[2*i])*16 + hexDigital.index(hexs[2*i + 1])
            list_bytes += struct.pack('B', (n & 0xff))
        return list_bytes.decode(charset)

    # 字节数组转16进制字符串
    def bytes2HexString(self, byte_datas):
        result = ''
        for i in range(len(byte_datas)):
            sub_str = hex(byte_datas[i] & 0xFF)
            sub_str = sub_str[2:]
            if len(sub_str) == 1:
                sub_str = '0' + sub_str
            result += sub_str
        return result

    # 16进制字符串转字节数组
    def hexString2Bytes(self, hex_string):
        l = len(hex_string)//2
        ret = b''
        for i in range(l):
            ret += int(hex_string[i*2: i*2+2], 16).to_bytes(1, byteorder='big')
        return ret

    def int_to_hexString(self, num, step):
        '''
        整数转16进制字符串并补位   16进制转整数：int('1d', 16)
        :param num: 需要转换的整数
        :param step: 转换之后的16进制字符串的位数
        :return: 转换并补位之后的16进制字符串，去掉 0x
        '''
        ret = hex(num)[2:]
        ret = '0' * (step - len(ret)) + str(ret)
        return ret