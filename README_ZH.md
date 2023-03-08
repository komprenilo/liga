[English: Liga](README.md) | 简体中文

# 理解机: 让数据和机器学习模型一起舞动

理解机是一套扩展SQL引擎以支持使用机器学习模型处理数据的通用框架。具备以下特性：

+ 兼爱非攻：关注人类福祉的地球制造开源软件
+ 可伸缩：轻松处理任意规模数据集
+ 灵活易用：提供精心设计的 SQL 扩展语法和 [Python API](README_PYTHON.md)
+ 可扩展：通过插件机制和模型注册系统轻松集成任意机器学习模型

基于理解机框架，通过提供领域专用的
+ 自定义函数（UDF）
+ 自定义数据类型（UDT）
+ 模型类型（Model Type）

可以得到领域专用理解机解决方案：

| 领域 | PYPI | 可视化示例 | 数据处理示例 |
|-----|-----------|------------|-|
| 视觉理解机 | [ligavision](README_VISION.md) | | | |
| 听觉理解机 | | | |
| 自然语言理解机 | | | |
| 预测机 |  | | | |

## 机器学习系统集成
### 机器学习框架
+ [scikit-learn](README_SKLEARN.md)
+ [PyTorch](https://gitee.com/komprenilo/liga-pytorch)

### 模型注册系统
理解机V0.2.x支持 MLflow 这个模型注册系统，这并不意味着理解机只能用 MLflow 这个特定的模型注册系统。

## 数据处理系统集成
### SQL引擎扩展
理解机V0.2.x是基于Apache Spark实现的，这并不意味着理解机是一个基于 Apache Spark 的开源项目。Spark SQL仅仅是理解机这套框架想要适配的SQL引擎之一。

#### SQL: ML_PREDICT
``` sql
SELECT
  id,
  ML_PREDICT(yolov5, image)
FROM cocodataset
```

#### SQL：创建模型
``` sql
-- Create model
CREATE [OR REPLACE] MODEL model_name
[USING liga_plugin_name]
[FOR model_type]
[OPTIONS (key1=value1,key2=value2,...)]
```

#### SQL：管理模型
``` sql
-- Describe model
{ DESC | DESCRIBE } MODEL model_name;

-- Show all models
SHOW MODELS;

-- Delete a model
DROP MODEL model_name;
```

## 工作流
### 场景1：完整的工作流：
```
训练模型 -> 保存到模型注册中心 -> 创建模型 -> 使用模型
```
> 注意：目前只支持使用Python训练模型，不支持使用SQL训练模型。

### 场景2：如果模型已经训练完成，则可以简化为：
```
创建模型 -> 使用模型
```
创建模型有多种模式，如：
+ 从公开的预训练模型创建模型
+ 从私有的模型注册系统创建模型
+ 制定模型的位置，加载模型

### 场景3：直接使用模型
```
使用模型
```
> 注意：这种场景依赖于一个可持久化的模型目录（Model Catalog）。

## 历史
理解机源于Rikai项目。Rikai的作者是[Chang She](https://github.com/changhiskhan)和[Lei Xu](https://github.com/eddyxu)，Rikai的第一个公开版本发布于2021年4月4日。在第四次Tubi黑客马拉松中，[Darcy Shen](https://github.com/da-tubi)和[Renkai Ge](https://github.com/Renkai)将Rikai项目中扩展Spark SQL实现调用机器学习模型的部分从Rikai项目[剥离并重构](https://github.com/komprenilo/liga/issues/13)。
