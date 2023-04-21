# 服务端设计文档

## 1 数据库

**Schema：**$S(OD_{id})$

**Table：**$XSet$

| 属性      | 说明             | 数据类型 |
| --------- | ---------------- | -------- |
| $X_{w,d}$ | 关键词陷门       | varchar  |
| $Y_{w,d}$ | 加密的文件标识符 | varchar  |

**Table：**$USet$

| 属性        | 说明           | 数据类型 |
| ----------- | -------------- | -------- |
| $uid_{u,d}$ | DO授权用户标识 | varchar  |
| $U_{u,d}$   | 检验值         | varchar  |

**Table：**$ASet$

| 属性     | 说明           | 数据类型 |
| -------- | -------------- | -------- |
| $aid$    | DU授权用户标识 | varchar  |
| $\alpha$ | 检验值         | varchar  |

## 2 服务器操作

### 2.1 更新文件

```python
async def update_xset(ADD, user_id, enc_fp, data):
    edb = get_edb(user_id) # 获取 user_id 对应的数据库
    if edb is None:
        edb = init_edb(user_id) # 没有则新建
        
    try:
        edb.xset = data.tmpset # 更新 XSet
        edb.save()
        result = "Success"
    except Exception as e:
        result = "Fail: " + str(e)
    return result
```

### 2.2 DO授权登记

```python
async def update_uset(OnlineAuth, do_id, data):
    edb = get_edb(user_id) # 获取 do_id 对应的数据库
    if edb is None:
        result = "Error: Upload encrpyted files and become DO"
        return result # 没有则返回错误，提示上传文件成为 DO
    
    try:
        edb.uset = data.tmparr # 更新 USet
        edb.save()
        result = "Success"
    except Exception as e:
        result = "Fail: " + str(e)
    return result
```

### 2.3 DU授权登记

```python
async def update_aset(OfflineAuth, do_id, data):
    edb = get_edb(do_id) # 获取 do_id 对应的数据库
    if edb is None:
        result = "Error: This user is not a DO"
        return result # 没有则返回错误
    
    try:
        edb.aset = data.tmpaset # 更新 XSet
        edb.save()
        result = "Success"
    except Exception as e:
        result = "Fail: " + str(e)
    return result
```

### 2.4 查询

```python
async def search(Search, do_id, data):
    edb = get_edb(do_id) # 获取 do_id 对应的数据库
    if edb is None:
        result = "Error: This user is not a DO"
        return result # 没有则返回错误
    
    result = []
    for touple in data.query:
        if u = edb.uset.select(uid = touple.uid) is None:
            continue
        x = pow(touple.stk_d, u)
        if touple.alist is not None: # AList 不空
            for aid in touple.alist:
                alpha = edb.aset.select(aid = aid)
                x = pow(x, alpha)
		result.append(edb.xset.select(x = x)) # 查找 XSet
	return result
```

