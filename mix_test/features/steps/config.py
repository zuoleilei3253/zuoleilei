# 设置邮箱
MAIL_INFO = {
    'user': 'xxxx@126.com',
    'password': 'xxxxxx',
    'host': 'smtp.126.com',
    # 'smtp_ssl': True,  # 发件箱是qq邮箱的话，改成True
}

TO = ['xxx@vista.com']

# 日志的配置
log_level = 'info'

# 数据库配置
host = 'xxx.com'
port = 3306
user = 'xxx'
password = 'xxx'
db = 'mix'
charset = 'utf-8'

# 用户配置
login_api = "https://api.mp.one/common/user/passport/login"
user_info = {"leilei": {"email": "xxx@163.com", "password": "xxx"}}

# 测试服域名配置
HOSTS = {
    # 'QA': 'http://api.zhp.cn',  # 测试环境
    # 'DEV': 'http://dev.zhp.cn',  # 开发环境
    'PRE': 'https://xx.xmp.one'  # 预生产环境
}
domain = HOSTS.get('PRE')  # 默认测试环境的地址
