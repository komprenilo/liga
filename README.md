English | [简体中文](README_ZH.md)

# Liga: Let Data Dance with ML Models
> 理解机：让数据和机器学习模型一起舞动！

Liga is general-purpose ML-enhanced SQL framework designed to be modular, extensible and scalable.

Liga-based domain specific abstraction:
+ Liga Vision: UDT/UDF/Liga ModelType for Computer Vision
+ Liga Audio (TODO): UDT/UDF/Liga ModelType for Audio
+ Liga NLP (TODO): UDT/UDF/Liga ModelType for NLP

## Table of Contents
* [Design](#design)
* [Live Notebooks](#live-notebooks)
* [SQL References](#sql-references)
   * [SQL: ML_PREDICT for small models](#sql-ml_predict-for-small-models)
   * [SQL: ML_TRANSFORM for big models](#sql-ml_transform-for-big-models)
   * [SQL: Model Creation](#sql-model-creation)
   * [SQL: Model Catalog](#sql-model-catalog)
* [History](#history)

## Design
<dl>
<dt><b>Spark SQL and MLflow</b></dt>
<dd>
Currently, Liga depends on Spark SQL. It does not mean Liga will always be a Apache Spark based project. Just like that MLflow registry is an optional registry in Liga, Spark SQL should and could also be an option.
<dd>
<dt><b>For Prediction but not for Training</b></dt>
<dd>
Thanks to the ML Model Registries, the training and the prediction can be separated. Liga is designed to apply ML Models via SQL syntax on datasets but not designed to train ML models via SQL syntax for now. Let us <b>focus on</b> applying and also serving ML models first!
</dd>
<dt><b>General Purpose but not Domain Specific</b></dt>
<dd>
Integration with a specific model, a specific ML framework or a specific domain like vision or audio should not be maintained in this repository. They should be maintained in separate projects depending on Liga. eg. A separate project `liga-vision` for integrating the computer vision related UDF and UDT (eg. Image, Box2d) or a separate project `liga-pytorch` for integrating the PyTorch framework. Scikit-learn integration and Spark ML integration are the reference implementation. That's why they are maintained in Liga.
</dd>
</dl>


## SQL References
### SQL: `ML_PREDICT` for small models
```
SELECT
  id,
  ML_PREDICT(my_yolov5, image)
FROM cocodataset 
```

`ML_PREDICT` is a special UDF which takes two parameters:
+ `model_name` is a special parameter look likes an identifier
+ data


### SQL: `ML_TRANSFORM` for big models
TODO (see [#9](https://github.com/liga-ai/liga/issues/16) )

### SQL: Model Creation
A Model instance is created by specifying the model flavor, type and options on the uri.

``` sql
-- Create model
CREATE [OR REPLACE] MODEL model_name
[FLAVOR flavor]
[MODEL_TYPE model_type]
[OPTIONS (key1=value1,key2=value2,...)]
USING "uri";
```
+ `flavor`: eg. `liga.sklearn` => `from liga.sklearn.codegen import codegen`
+ `model_type`: eg. `classifier` => `from liga.sklearn.models.classifier import MODEL_TYPE`


### SQL: Model Catalog
``` sql
-- Describe model
{ DESC | DESCRIBE } MODEL model_name;

-- Show all models
SHOW MODELS;

-- Delete a model
DROP MODEL model_name;
```

## Python API
see [Python API](README_PYTHON.md).

## History
Liga is the ML-enhanced SQL part of [Rikai](https://github.com/eto-ai/rikai). Rikai is created by [@changhiskhan](https://github.com/changhiskhan) and [@eddyxu](https://github.com/eddyxu) and [the first release](https://github.com/eto-ai/rikai/releases/tag/v0.0.4) of Rikai dates back to 2021/04/04. [@da-tubi](https://github.com/da-tubi) and [@Renkai](https://github.com/Renkai) created the Liga fork of Rikai as a [project](https://github.com/liga-ai/liga/issues/13) of the 4th Tubi Hackathon.
