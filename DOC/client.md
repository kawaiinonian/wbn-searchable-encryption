#  客户端设计文档

## 1. 用户持有数据

| 名称                                 | 说明                                                         | 数据类型      |
| ------------------------------------ | ------------------------------------------------------------ | ------------- |
| $user\_id$                           | 唯一标识用户身份                                             | str/bytes     |
| $\lambda$                            | 安全系数                                                     | int           |
| $SKs[SK_1,SK_2,...]$                 | 作为DO的密钥组                                               | list          |
| $SK[K_1,K_2,K_3]$                    | 对某一DOC作为DO的密钥组                                      | list          |
| $K_1,K_2,K_3$                        | 对某一DOC作为DO的密钥                                        | key           |
| $DUs\{DO_1:[UD_1],...\}$             | 作为DU的数据集合                                             | dict          |
| $UD\{UK,UST\}$                       | 对某一DO作为DU的数据集合                                     | set           |
| $UK[K_u,\tilde{K_u}]$                | 对某一DO作为DU的密钥组                                       | list          |
| $K_u,\tilde{K_u}$                    | 对某一DO作为DU的密钥                                         | key           |
| $UST\{UserAuth,DocKey\}$             | 对某一DO作为DU的权限数据                                     | set           |
| $UserAuth[(uid,offtok,AList)_1,...]$ | 对某一DO作为DU向其他DU授权情况                               | hashlist/dict |
| $uid$                                | 对某一DO所授权的某个文件d作为DU的身份标识，标记DU有访问d的权限 | str/bytes     |
| $offtok$                             | 对某一DO所授权的某个文件d作为DU再向其他DU授权的搜索令牌      | element       |
| $AList[aid_1,aid_2,...]$             | 对某一DO所授权的某个文件d作为DU再向其他DU授权的情况记录表    | list          |
| $aid$                                | 对某一DO所授权的某个文件d作为DU再向其他DU授权的情况记录      | str/bytes     |
| $DocKey[(d,K_d,K_d^{enc})_1,...]$    | 对某一DO所授权的文件集合                                     | list          |
| $d$                                  | 文件标识符                                                   | file_desc     |
| $K_d$                                | 某一DO对某一文件标识符d生成搜索令牌的密钥                    | key           |
| $K_d^{enc}$                          | 某一DO对某一文件标识符d的加密密钥                            | key           |

给出下面的数据结构：

```python
from typing import List, Dict, Tuple
@dataclass
class SK:
    K1: key
    K2: key
    K3: key

@dataclass
class UK:
    Ku: key
    KuT: key
    
@dataclass
class UST:
    user_auth: List[Tuple[uid, offtok, AList]]
    doc_key: List[Tuple[d, Kd, Kdenc]]

@dataclass
class UD:
    uk: UK
    ust: UST
    
@dataclass
class User:
    user_id: str
    sks: List[SK]
    DUs: Dict[User_data.user_id, UD]
```

## 2. 用户操作

### 2.0 初始化

```python
async def init():
    await user_id, result = get_user_id() #向服务器申请一个user_id
    return user_id, result
```

### 2.1 向服务器上传数据并成为DO

```python
async def add_data(user_id, files, sk):
    FILE_DESC *d[N]
    gen_file_desc(d, fp) # 获取文件标识符
    if sk is None 
        init_sk(sk)
    enc_fp = enc_files(fp, sk.k3) # 加密文件本体，暂时认为文件的加密密钥就是K_d^enc
    ENCRYPT_DATA = enc_index_keyword(d, sk.k1, sk.k2) # 加密索引和关键词，但还没有想好用什么结构存储
    await result = communicate_server(ADD, user_id, enc_fp, data) # 向服务器提交加密文件和加密索引，并返回通讯结果
    return result
```

### 2.2 登记其他用户

```python
async def enroll_response(enroll_user_id, auth_list):
    uk = gen_user_key() # 生成授权密钥
    enroll(enroll_user_id, auth_list) # 将被授权的用户写入自己的authlist里面
    await result = communicate_user(ENROLL_RESPONSE, enroll_user_id, uk) # 向申请授权的用户发送授权密钥并返回结果
    return result
```

### 2.3 向其他用户请求登记

```python
async def enroll_request(user_id, requested_user_id):
	await result = communicate_user(ENROLL_REQUEST, user_id, requested_user_id)
    return result
```

### 2.4 作为DO向登记过的用户授权

```

```



### 2.5 作为DU向其他用户授权

### 2.6 接受DO的授权

### 2.7 接受DU的授权

### 2.8 向服务器查询

### 2.9 撤回授权

## 3. API