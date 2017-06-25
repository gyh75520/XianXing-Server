#coding=utf8
__author__ = 'buren'

#资源不存在
RES_NOT_EXIST = 100

# 用户权限不够
PERMISSIONS_DENIED = 101

# 资源的状态不允许被操作
STATE_ERROR = 102

# 丢失参数
MISSING_ARGS = 103

# 参数存在，但是格式错误或者值不允许
ARGS_ERROR = 104

# 相关资源不存在或者错误，检查参数中的外键是否正确
RELATE_RES_ERROR = 105

# 进行某操作频率过快
FREQUENCY_ERROR = 106

# 没有更多了
MO_MORE = 107

# 其他错误
OTHER_ERROR = 108

# 身份错误
AUTHORITY_ERROR = 109