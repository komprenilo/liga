from liga.sklearn.mlflow import _get_model_type


def test_get_model_type():
    from sklearn.linear_model import LinearRegression

    regressor = LinearRegression()
    assert _get_model_type(regressor) == "liga.sklearn.models.regressor"

    from sklearn.linear_model import RidgeClassifier

    classifier = RidgeClassifier()
    assert _get_model_type(classifier) == "liga.sklearn.models.classifier"

    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)
    assert _get_model_type(pca) == "liga.sklearn.models.transformer"

    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=2, random_state=0)
    assert _get_model_type(kmeans) == "liga.sklearn.models.cluster"
