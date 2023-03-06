English | [简体中文：理解机](README_ZH.md)

# Liga: Let Data Dance with ML Models
Liga is a general-purpose framework to extend any SQL engine with ML Models with the following features:
+ Scalable: Processing data at any scale
+ User Friendly: Well-designed SQL extension syntax and [Python API](README_PYTHON.md)
+ Extensible: Integrated with any ML system via Liga Plugin and Model Registry

Based on the Liga framework, with:
+ User Defined Functions
+ User Defined Types
+ Model Types

we can provide domain specific Liga solution:

| Domain | PYPI | Visualization Demo | Liga SQL Demo |
|-----------------|------|--------------------|---------------|
| [Liga Vision](README_VISION.md) | ligavision | TODO | TODO |

## Integration with Machine Learning
### Machine Learning Framework
+ [scikit-learn](README_SKLEARN.md)
+ [PyTorch](https://github.com/komprenilo/liga-pytorch)

### Model Registry
Liga v0.2.x supports MLflow. It does not mean it is bound to MLflow.

## Integration with SQL Engine
Liga v0.2.x extends Spark SQL. It does not mean it is bound to Spark SQL.

### SQL References
#### SQL: `ML_PREDICT`
``` sql
SELECT
  id,
  ML_PREDICT(my_yolov5, image)
FROM cocodataset 
```

`ML_PREDICT` is a special UDF which takes two parameters:
+ `model_name` is a special parameter look likes an identifier
+ data

#### SQL: Model Creation
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


#### SQL: Model Catalog
``` sql
-- Describe model
{ DESC | DESCRIBE } MODEL model_name;

-- Show all models
SHOW MODELS;

-- Delete a model
DROP MODEL model_name;
```

## Workflow
### Case 1: The Complete Workflow
```
Train -> Log to Model Registry -> Create a model -> Apply the model
```
> WARNING: Please use Python to train a model, currently, Liga does not provide the SQL way to train a model.

### Case 2: Without training
```
Create a model -> Apply the model
```
There are several ways to create a model:
+ Load public pretrained model
+ Load from private Model Registry
+ Load from a URI


### Case 3: Apply model directly
```
Apply the model
```
> WARNING: it depends on a persistent Model Catalog

## History
Liga is the ML-enhanced SQL part of [Rikai](https://github.com/eto-ai/rikai). Rikai is created by [@changhiskhan](https://github.com/changhiskhan) and [@eddyxu](https://github.com/eddyxu) and [the first release](https://github.com/eto-ai/rikai/releases/tag/v0.0.4) of Rikai dates back to 2021/04/04. [@da-tubi](https://github.com/da-tubi) and [@Renkai](https://github.com/Renkai) created the Liga fork of Rikai as a [project](https://github.com/liga-ai/liga/issues/13) of the 4th Tubi Hackathon.
