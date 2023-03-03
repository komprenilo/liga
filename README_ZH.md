[English](README.md) | 简体中文

# 理解机: 让数据和机器学习模型一起舞动
> Liga: Let Data Dance with ML Models!

理解机（英文名为 Liga，是 “理解” 的汉语吴音）是一个在 SQL 引擎中集成机器学习模型能力的通用框架。

理解机的设计目标是：模块化、可扩展、面向任意规模数据。

基于理解机框架的领域专用抽象接口：
+ 视觉理解机: 提供计算机视觉这个领域的用户自定义数据类型、用户自定义函数、理解机模型类型
+ 听觉理解机: TODO
+ 自然语言理解机: TODO

## 理解机的设计理念
<dl>
<dt><b>关于Spark SQL和MLflow</b></dt>
<dd>
理解机 V0.2.x 是基于 Apache Spark 实现的，这并不意味着理解机是一个基于 Apache Spark 的开源项目。Spark SQL 仅仅是理解机这套框架想要适配的 SQL 引擎之一。同样，理解机 V0.2.x 支持 MLflow 这个模型注册系统，这并不意味着理解机只能用 MLflow 这个特定的模型注册系统。
<dd>
<dt><b>用于预测而不是训练</b></dt>
<dd>
理解机 V0.2.x 支持使用 SQL 语法将机器学习应用于大规模的数据集。由于模型注册系统可以将模型的训练和预测解耦。当下，我们专注于实现基于理解机框架的模型预测和服务化。
<dd>
<dt><b>通用框架而不是领域专用</b></dt>
<dd>
理解机是一个通用框架，并不限定具体的领域。视觉理解机是基于理解机框架实现的专注于计算机视觉领域的解决方案。未来，我们还会实现听觉、自然语言处理等领域的专用理解机解决方案。
<dd>
</dl>


## 理解机SQL扩展参考
### SQL：创建模型
```
-- Create model
CREATE [OR REPLACE] MODEL model_name
[FLAVOR flavor]
[MODEL_TYPE model_type]
[OPTIONS (key1=value1,key2=value2,...)]
USING "uri";
```

### SQL：管理模型
```
-- Describe model
{ DESC | DESCRIBE } MODEL model_name;

-- Show all models
SHOW MODELS;

-- Delete a model
DROP MODEL model_name;
```

## 历史
理解机源于 ETO 公司的 Rikai 项目，在第四次Tubi黑客马拉松中，理解机的作者们将Rikai项目中扩展Spark SQL实现调用机器学习模型的部分从Rikai项目剥离并重构。
