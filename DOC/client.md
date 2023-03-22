# 客户端设计文档

## 1.用户持有数据

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

## 2.用户操作

### 2.0 初始化

### 2.1 向服务器上传数据并成为DO

### 2.2 接收其他用户的登记

### 2.3 向其他用户登记

### 2.4 作为DO向登记过的用户授权

### 2.5 作为DU向其他用户授权

### 2.6 接受DO的授权

### 2.7 接受DU的授权

### 2.8 向服务器查询

### 2.9 撤回授权