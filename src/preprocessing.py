from sklearn.preprocessing import QuantileTransformer
from BlackBox.Preprocessors import FgpPreprocessor, DescriptorsPreprocessor, Preprocessor


def preprocess_X(fingerprints_columns, descriptors_columns, train_X, train_y, test_X, test_y, features, is_smrt):
    if features == "fingerprints":
        preproc = FgpPreprocessor(fgp_cols=fingerprints_columns)
    elif features == "descriptors":
        preproc = DescriptorsPreprocessor(desc_cols=descriptors_columns, adduct_cols=None if is_smrt else fingerprints_columns[-3:])
    else:
        preproc = Preprocessor(desc_cols=descriptors_columns, fgp_cols=fingerprints_columns)
    preproc_train_X = preproc.fit_transform(train_X, train_y)
    preproc_test_X = preproc.transform(test_X, test_y)
    return preproc_train_X, preproc_test_X, preproc


def preprocess_y(train_y, test_y):
    preproc_y = QuantileTransformer(n_quantiles=1000, output_distribution='normal')
    train_preproc_y = preproc_y.fit_transform(train_y.reshape(-1, 1))
    test_preproc_y = preproc_y.transform(test_y.reshape(-1, 1))
    return train_preproc_y.flatten(), test_preproc_y.flatten(), preproc_y
