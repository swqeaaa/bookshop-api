from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS, SignatureExpired, BadData
import time

salt = "adsafergberhere"
payload = {
    "name": "dawsonenjoy",
}
tjwss = TJWSS(salt, 1)
# 实例化jwt序列化对象，设置salt和超时时间，这里设置1s后超时
token = tjwss.dumps(payload).decode()
# 编码payload数据，生成token
data = tjwss.loads(token)
# 校验和解码token
print(data)

time.sleep(2)
# 2s后让token超时
try:
    print(tjwss.loads(token))
except SignatureExpired:
    print("token超时")
except BadData:
    print("认证失败")