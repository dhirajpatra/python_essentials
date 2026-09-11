"""
Without using scikit-learn's metric functions,
write a Python function that takes y_true and y_pred for
a binary classification problem and returns precision, recall, and F1 score.

y_true = [1, 0, 1, 1, 0, 1]
y_pred = [1, 0, 1, 0, 0, 1]

tp = [0, 2, 5]
fp = [4]
fn = [3]
p = len(tp) / (len(tp) + len(fp)) if (len(tp) + len(fp)) > 0 else 0
r = len(tp) / (len(tp) + len(fn)) if (len(tp) + len(fn)) > 0 else 0
f1 = (p - r) / (p + r) if (p + r) > 0 else 0
"""
from typing import List, Any


def metrics(y_true: List[int], y_pred: List[int]) -> List[Any] | List[float | int]:
    n = len(y_true)
    if len(y_pred) != n:
        return []

    tp = []
    fp = []
    fn = []

    for i in range(n):
        if y_true[i] == 1 and y_pred[i] == 1:
            tp.append(i)
        elif y_true[i] == 1 and y_pred[i] == 0:
            fn.append(i)
        else:
            fp.append(i)

    p = len(tp) / (len(tp) + len(fp)) if (len(tp) + len(fp)) > 0 else 0
    r = len(tp) / (len(tp) + len(fn)) if (len(tp) + len(fn)) > 0 else 0
    f1 = (p - r) / (p + r) if (p + r) > 0 else 0

    return [p, r, f1]


if __name__ == "__main__":
    y_true = [1, 0, 1, 1, 0, 1]
    y_pred = [1, 0, 1, 0, 0, 1]
    result = metrics(y_true, y_pred)
    print(f"Precision: {result[0]:.2f}, Recall: {result[1]:.2f}, F1 Score: {result[2]:.2f}")
