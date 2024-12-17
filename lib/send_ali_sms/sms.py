import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
try:
    from .settings import *
except ImportError:
    from settings import *


def send_sms_by_phone(phone=None, name=None, airline=None, time=None):
    # 配置阿里云AccessKey ID和AccessKey Secret，这两个值是在阿里云账户管理中获取的，用于验证API请求的身份 【更换这两个】
    # ACCESS_KEY_ID = 'LTA......'
    # ACCESS_KEY_SECRET = '775......'

    # 创建AcsClient实例，用于发送请求到阿里云服务，参数包括AccessKey ID和Secret，以及服务区域（这里是杭州）
    client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-hangzhou')

    # 生成一个4位随机验证码，随机从0-9数字中,选择4个数字组合成字符串
    code = ''.join(random.sample('0123456789', 4))

    # 创建一个CommonRequest实例，用于设置发送到阿里云短信API的具体参数  [请求参数]   [固定模板无需更改]
    request = CommonRequest()
    request.set_accept_format('json')  # 设置API的响应格式为json
    request.set_domain('dysmsapi.aliyuncs.com')  # 设置调用的短信API的域名
    request.set_method('POST')  # 设置请求方式为POST
    request.set_protocol_type('https')  # 设置请求协议为HTTPS
    request.set_version('2017-05-25')  # 设置API的版本号
    request.set_action_name('SendSms')  # 设置调用的操作接口名为SendSms

    # 以下是短信API所需的参数 [短信参数] 【更换中间三个】
    request.add_query_param('RegionId', "cn-hangzhou")  # 设置服务区域，与客户端实例保持一致
    request.add_query_param('PhoneNumbers', phone)  # 设置接收短信的手机号码
    request.add_query_param('SignName', SIGN_NAME)  # 设置短信签名，这在阿里云短信服务中预设
    request.add_query_param('TemplateCode', TEMPLATE_ID)  # 设置短信模板ID，这在阿里云短信服务中预设

    # request.add_query_param('TemplateParam', f'用户${name}已经成功预定${airline}航空${time}的机票，请及时联系付款。')  # 设置短信模板中的变量，这里是验证码
    # 用户${name}已经成功预定${airline}航空${time}的机票，请及时联系付款。
    request.add_query_param("TemplateParam", '{"name": "%s", "airline": "%s", "time":"%s"}' % (name, airline, time))

    # 发送请求，并获取响应
    response = client.do_action_with_exception(request)

    # 短信结果
    print(response)


if __name__ == '__main__':
    # send_sms_by_phone(phone='19567693108', name="4612450814", airline="FlightNH011", time="2024-12-25")
    # send_sms_by_phone(phone='19567693108', name="4612450814", airline="NH011", time="2024-12-25")
    # send_sms_by_phone(phone='19567693108', name="Tom", airline="FlightNH011", time="2024-12-25")
    # send_sms_by_phone(phone='19567693108', name="Tom", airline="NH011", time="2024-12-25") #成功的
    # send_sms_by_phone(phone='19567693108', name="李琴123", airline="NH011", time="2024-12-25") #成功的
    # send_sms_by_phone(phone='19567693108', name="4612450814", airline="NH011", time="2024-12-25")
    send_sms_by_phone(phone='19567693108', name="T4612450814", airline="NH011", time="2024-12-25")
    # send_sms_by_phone(phone='18973194769', name="T50814", airline="NH011", time="2024-12-25") #成功的



    '''
    当前用户名： 4612450814
    第一班日期： 2024-12-25
    第一班班次： FlightNH011
    第二班日期： 2024-12-29
    第二班班次： FlightNH182
    '''
