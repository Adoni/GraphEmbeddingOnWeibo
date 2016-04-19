
分类的核心代码，包含grid search 用以调参
```python
def evaluate(labels, embedding):
    from collections import Counter
    uids = list(set(embedding.keys()) & set(labels.keys()))
    X = map(lambda uid: embedding[uid], uids)
    Y = map(lambda uid: labels[uid], uids)
    print('\t', dict(Counter(Y)))
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
        random_state=0
    )
    tuned_parameters = [
        {
            'kernel': ['rbf'],
            'gamma': [1e-2, 1e-3, 1e-4],
            'C': [1, 10, 100, 500, 1000]
        },
        {
            'kernel': ['linear'],
            'C': [1, 10, 100, 500, 1000]
        }
    ]
    print("# Tuning hyper-parameters for f1_weighted")
    print()

    clf = GridSearchCV(
        SVC(C=1),
        tuned_parameters,
        cv=5,
        scoring='f1_weighted',
        n_jobs=12
    )
    clf.fit(X_train, y_train)
    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in clf.grid_scores_:
        print(
            "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params)
        )
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred, digits=3))
    print()
    sys.stdout.flush()

```
