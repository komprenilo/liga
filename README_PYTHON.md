# Liga Python API
## Model Type
A Model Type encaptures the interface and schema of a concrete ML model. It acts as an adaptor between the raw ML model input/output Tensors and Spark / Pandas.

Here is the key code snippet of the sklearn `classifier` model type ([`liga.sklearn.models.classifier`](https://github.com/liga-ai/liga/blob/main/python/liga/sklearn/models/classifier.py)):
``` python
class Classifier(SklearnModelType):
    """Classification model type"""

    def schema(self) -> str:
        return "int"

    def predict(self, *args: Any, **kwargs: Any) -> List[int]:
        assert self.model is not None
        assert len(args) == 1
        return self.model.predict(args[0]).tolist()
```
## Model Flavor
A Flavor describes the framework upon which the model was built.

A Liga model flavor should provide:
<dl>
<dt><b>generate_udf</b></dt>
<dd>to construct a Pandas UDF to run flavor-specific models. The special UDF `ML_PREDICT` will be translated into the generated pandas udf per flavor.</dd>
<dt><b>load_model_from_uri</b></dt>
<dd>to load models from filesystem URI for `FileSystemRegistry`. Because there are different ways to load a model from a filesystem URI for different ML frameworks. Model Registries like MLflow unify the way to load a model from the registry. That's why for those model registries, a URI (eg. `mlflow:///yolov5`) is sufficient.</dd>
</dl>


Supported flavors:
+ [sklearn](https://github.com/liga-ai/liga/blob/main/python/liga/sklearn/codegen.py) (provided by [`liga-sklearn`](https://pypi.org/project/liga-sklearn/))
+ [pytorch](https://github.com/liga-ai/liga-pytorch/blob/main/python/liga/pytorch/codegen.py) (provided by [`liga-pytorch`](https://pypi.org/project/liga-pytorch/))
+ ...

## Model Registry
A model registry specifies where and how to load a model.

| Name | Pypi | URI |   |
|----------|-------------------------|-------|---|
|  [DummyRegistry](https://github.com/liga-ai/liga/blob/main/python/liga/registry/fs.py)  | `liga` | | A special registry without URI provided. How and where to load model is hard-coded in model types, eg. `torchvision.models.resnet50()`. |
| [FileSystemRegistry](https://github.com/liga-ai/liga/blob/main/python/liga/registry/fs.py) | `liga` | `http:///`,`file:///`,`s3:///`,... | |
|  [MLflowRegistry](https://github.com/liga-ai/liga/blob/main/python/liga/mlflow/registry.py) | `liga-mlflow` | `mlflow:///` | MLflowRegistry is the recommended production-ready model registry. |

## Model Catalog
Currently, only a in-memory model catalog is available in Liga. Via Model Catalog, ML enhanced-SQL users only needs focus on how to apply ML-enhanced SQL on datasets at scale. Models are carefully maintained by Data/ML Engineers or Data Scientists.

> WARNING: Python API to customize the Model Catalog is not yet provided!
