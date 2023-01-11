# Liga: the ML-Enhanced Spark SQL
## Design
Liga is general-purpose ML-enhanced SQL framework designed to be modular, extensible and scalable.

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
Integration with a specific model, a specific ML framework or a specific domain like vision or audio should not be maintained in this repository. They should be maintained in separate projects depending on Liga. eg. A separate project `liga-vision` for integrating the computer vision related UDF and UDT (eg. Image, Box2d) or a separeate project `liga-pytorch` for integrating the PyTorch framework. Scikit-learn integration and Spark ML integration are the reference implementation. That's why they are maintained in Liga.
</dd>
</dl>


## Live Notebooks
<dl>
<dt><b>Latest Notebook</b></dt>
<dd>
Latest Notebook is the in-repo Jupyter notebook, it depends on the latest code in this repo. You need to clone this repo and then launch the Jupyter Notebooks locally. You can also click the link below to preview it on Github.
</dd>
<dt>Google Colab Notebook</dt>
<dd>
Google Colab Notebook is the notebook depends on the latest stable release of Liga. The link below helps you open the notebook under the latest stable release of Liga in Google Colab. You can try the live Google Colab notebooks just using a web browser.
</dd>
</dl>

Try the latest notebooks:
```
git clone https://github.com/liga-ai/liga.git
bin/lab
```

Preview the notebooks on Github or Try the live notebook on Google Colab:

| Model | Model Type | Official Documentation | Preview Latest Notebook | Try Google Colab Notebook |
|-------|---------|-----|-----------|--------|
| LinearRegression | regressor | [Linear Models Ordinary Least Squares](https://scikit-learn.org/1.1/modules/linear_model.html#ordinary-least-squares)        | [Demo](notebooks/1.1.1%20LinearRegression.ipynb) | |
| LogisticRegression | classifier | [Logistic regression](https://scikit-learn.org/1.1/modules/linear_model.html#logistic-regression) | [Demo](notebooks/1.1.11%20LogisticRegression.ipynb) | |
| Ridge | regressor | [Ridge regression and classification](https://scikit-learn.org/1.1/modules/linear_model.html#ridge-regression-and-classification) | [Demo](notebooks/1.1.2%20Ridge.ipynb) | |
| RidgeClassifier | classifier | | [Demo](notebooks/1.1.2.2%20RidgeClassifier.ipynb) | |
| SVC/NuSVC/LinearSVC | classifier | [Support Vector Machines](https://scikit-learn.org/1.1/modules/svm.html) | [Demo](notebooks/1.4.1%20SVC.ipynb) | |
| SVR/NuSVR/LinearSVR | regressor | | [Demo](notebooks/1.4.2%20SVR.ipynb) | |
| RandomForestClassifier | classifier | [Forests of randomized trees](https://scikit-learn.org/1.1/modules/ensemble.html#forests-of-randomized-trees) | [Demo](notebooks/1.11.2%20RandomForestClassifier.ipynb) ||
| RandomForestRegressor | regressor | | [Demo](notebooks/1.11.2%20RandomForestRegressor.ipynb) ||
| ExtraTreesClassifier | classifier | | [Demo](notebooks/1.11.2%20ExtraTreesClassifier.ipynb) ||
| ExtraTreesRegressor | regressor | | [Demo](notebooks/1.11.2%20ExtraTreesRegressor.ipynb) |
| KMeans | cluster | [Clustering](https://scikit-learn.org/1.1/modules/clustering.html#k-means) | [Demo](notebooks/2.3.2%20KMeans.ipynb) ||
| PCA | transformer | [Decomposing signals in components (matrix factorization problems)](https://scikit-learn.org/1.1/modules/decomposition.html#decomposing-signals-in-components-matrix-factorization-problems) | [Demo](notebooks/2.5.1%20PCA.ipynb) ||


## Liga SQL References
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
TODO (see #9 )

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
### Model Type
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
### Model Flavor
A Flavor describes the framework upon which the model was built.

A Liga model flavor should provide:
<dl>
<dt><b>generate_udf</b></dt>
<dd>to construct a Pandas UDF to run flavor-specific models. The special UDF `ML_PREDICT` will be translated into the generated pandas udf per flavor.</dd>
<dt><b>load_model_from_uri</b></dt>
<dd>to load models from filesystem URI for `FileSystemRegistry`. Because there are different ways to load a model from a filesystem URI for different ML frameworks. Model Registries like MLflow unify the way to load a model from the registry. That's why for those model registries, a URI (eg. `mlflow:///yolov5`) is sufficient.</dd>
</dl>


Supported flavors:
+ [sklearn](https://github.com/liga-ai/liga/blob/main/python/liga/sklearn/codegen.py) (provided by `liga-sklearn`)
+ pytorch (provided by `liga-pytorch`)
+ ...

### Model Registry
A model registry specifies where and how to load a model.

| Name | Pypi | URI |   |
|----------|-------------------------|-------|---|
|  [DummyRegistry](https://github.com/liga-ai/liga/blob/main/python/liga/registry/fs.py)  | `liga` | | A special registry without URI provided. How and where to load model is hard-coded in model types, eg. `torchvision.models.resnet50()`. |
| [FileSystemRegistry](https://github.com/liga-ai/liga/blob/main/python/liga/registry/fs.py) | `liga` | `http:///`,`file:///`,`s3:///`,... | |
|  [MLflowRegistry](https://github.com/liga-ai/liga/blob/main/python/liga/mlflow/registry.py) | `liga-mlflow` | `mlflow:///` | MLflowRegistry is the recommended production-ready model registry. |

### Model Catalog
Currently, only a in-memory model catalog is available in Liga. Via Model Catalog, ML enhanced-SQL users only needs focus on how to apply ML-enhanced SQL on datasets at scale. Models are carefully maintained by Data/ML Engineers or Data Scientists.

> WARNING: Python API to customize the Model Catalog is not yet provided!


## History
Liga is the ML-enhanced SQL part of [Rikai](https://github.com/eto-ai/rikai). Rikai is created by @changhiskhan and @eddyxu and [the first release](https://github.com/eto-ai/rikai/releases/tag/v0.0.4) of Rikai dates back to 2021/04/04. @da-tubi and @Renkai created the Liga fork of Rikai as a project of the 4th Tubi Hackathon (#4).
