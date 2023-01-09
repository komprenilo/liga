from liga.sklearn.mlflow import _get_model_type
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeClassifier
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def test_get_model_type():
    regressor = LinearRegression()
    assert _get_model_type(regressor) == "liga.sklearn.models.regressor"

    classifier = RidgeClassifier()
    assert _get_model_type(classifier) == "liga.sklearn.models.classifier"

    pca = PCA(n_components=2)
    assert _get_model_type(pca) == "liga.sklearn.models.transformer"

    kmeans = KMeans(n_clusters=2, random_state=0)
    assert _get_model_type(kmeans) == "liga.sklearn.models.cluster"
