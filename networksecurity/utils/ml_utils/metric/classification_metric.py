import sys

from networksecurity.entity.artifacts_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score


def get_classification_score(y_true,y_pred) ->ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true,y_pred)
        precision= precision_score(y_true,y_pred)
        recall = recall_score(y_true,y_pred)

        ClassificationMetric = ClassificationMetricArtifact(f1,precision,recall)
        return ClassificationMetric
    except Exception as e :
        raise NetworkSecurityException(e,sys)