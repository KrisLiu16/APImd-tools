# GPU 资源配额接口文档

GPU 资源配额的创建、释放以及查询接口示例。

## 1. 资源配额修改接口（新接口）

用于修改某配额

- **请求方式**: `PUT`
- **请求路径**: `/api/v1/quotas/:tenant`
- **请求头**:
  - `Content-type`: application/json
  - `Authorization`: Bearer {token}

#### 请求体参数

| 字段名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `region` | `string` | 是 | 资源选区 |
| `tenant` | `string` | 是 | 租户名 |
| `quota_source` | `string` | 是 | 配额来源<br>可选值: purchase/assign |
| `gpu_model` | `string` | 是 | gpu类型 |
| `num` | `int` | 是 | 修改后的数量，如果将num设置为0,则等同于是强制释放操作 |
| `expired_at` | `string` | - | 过期时间 |
| `id` | `int` | - | 如果对应的配额有,则传递 |

#### 请求示例

```JSON
PUT /api/v1/quotas/gpu-operator

{
    "region": "TW",
    "quota_source": "purchase",
    "gpu_model": "nvidia.com/gpu",
    "num": 1,
    "expired_at": "2025-12-03",
    "id": 212
}
```

#### 响应示例

```JSON
{
  "code": 0
}
```


## 2. 资源配额释放接口（新接口）

用于释放某配额

- **请求方式**: `DELETE`
- **请求路径**: `/api/v1/quotas/:tenant`
- **请求头**:
  - `Content-type`: application/json
  - `Authorization`: Bearer {token}

#### 请求体参数

| 字段名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `region` | `string` | 是 | 资源选区 |
| `tenant` | `string` | 是 | 租户名 |
| `quota_source` | `string` | 是 | 配额来源<br>可选值: purchase/assign |
| `gpu_model` | `string` | 是 | gpu类型 |
| `id` | `int` | - | 如果对应的配额有,则传递 |

#### 请求示例

```JSON
DELETE /api/v1/quotas/gpu-operator

{
    "region": "TW",
    "quota_source": "purchase",
    "gpu_model": "nvidia.com/gpu",
    "id": 212
}
```


## 3. 资源配额查询接口

获取所有配额信息

- **请求方式**: `GET`
- **请求路径**: `/api/v1/quota/user-quotas`
- **请求头**:
  - `Authorization`: Bearer {token}

#### 请求体参数

支持按照配额来源和类型过滤。

| 字段名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
| `quota_source` | `string` | - | 参数和响应对应调整,支持枚举值为:"purchase" 或 "assign" |
| `quota_type` | `string` | - | 参数和响应对应调整,支持枚举值为:"flexible" or "dedicated" or "mig" or "vgpu" |

#### 响应示例

```JSON
{
  "code": 0,
  "data": {
    "total": 3,
    "page": 1,
    "page_size": 10,
    "items": [
      {
        "tenant_name": "platform-operator",
        "quota_source": "purchase",
        "gpu_model": "nvidia.com/gpu",
        "quota_types": [
          {
            "quota_type": "flexible",
            "quota_details": [
              {
                "region": "US",
                "gpu_model": "nvidia.com/gpu",
                "count": 1
              }
            ],
            "used_count": 0,
            "total_count": 1
          }
        ]
      },
      {
        "tenant_name": "platform-operator",
        "quota_source": "purchase",
        "gpu_model": "nvidia.com/mig-1c10g",
        "quota_types": [
          {
            "quota_type": "mig",
            "quota_details": [
              {
                "region": "US",
                "gpu_model": "nvidia.com/mig-1c10g",
                "count": 1
              }
            ],
            "used_count": 0,
            "total_count": 1
          }
        ]
      },
      {
        "tenant_name": "test1015",
        "quota_source": "assign",
        "gpu_model": "tyui-3",
        "region": "US",
        "quota_types": [
          {
            "quota_type": "vgpu",
            "quota_details": [
              {
                "region": "US",
                "id": 212,
                "gpu_model": "tyui-3",
                "count": 2,
                "expire_time": "2026-01-02T15:04:05Z07:00"
              }
            ],
            "used_count": 1,
            "total_count": 2
          }
        ]
      },
      {
        "tenant_name": "zjw1029",
        "quota_source": "assign",
        "region": "US",
        "quota_types": [
          {
            "quota_type": "dedicated",
            "gpu_model": "nvidia.com/gpu",
            "quota_details": [
              {
                "region": "US",
                "id": 214,
                "gpu_model": "nvidia.com/gpu",
                "node_name": [
                  "gpu02"
                ],
                "count": 1
              }
            ],
            "used_count": 0,
            "total_count": 1
          }
        ]
      }
    ]
  }
}
```
