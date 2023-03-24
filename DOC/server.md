# 服务端设计文档

## 1 数据库

Schema：__________________

**Table：XSet**

| 属性      | 说明             | 数据类型 |
| --------- | ---------------- | -------- |
| $X_{w,d}$ | 关键词陷门       | varchar  |
| $Y_{w,d}$ | 加密的文件标识符 | varchar  |

**Table：USet**

| 属性        | 说明           | 数据类型 |
| ----------- | -------------- | -------- |
| $uid_{u,d}$ | DO授权用户标识 | varchar  |
| $U_{u,d}$   | 检验值         | varchar  |

**Table：ASet**

| 属性     | 说明           | 数据类型 |
| -------- | -------------- | -------- |
| $aid$    | DU授权用户标识 | varchar  |
| $\alpha$ | 检验值         | varchar  |

## 2 服务器操作

### 2.1 更新

```python
async def add(ADD, user_id, enc_fp, data):
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

