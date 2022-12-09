import pandas as pd
import catboost as cb
from sklearn.model_selection import train_test_split


class GenderPredictor:
    def __init__(self) -> None:
        pass

    def __preprocess(self, surname: str, name: str):
        surname_n = surname[-2:]
        name_n = name[-2:]

        num_let_sur = len(surname)
        num_let_nam = len(name)

        has_m_surend = int(surname[-2:].upper() in set(['OV', 'IN', 'AN']))
        last_let_name = int(name[-1].upper() == 'A')

        return pd.Series([
            surname,
            name,
            surname_n,
            name_n,
            has_m_surend,
            num_let_sur,
            num_let_nam,
            last_let_name
        ])

    def prepare_data(self):
        df_train = pd.read_csv('name_gender_features.csv')

        X = df_train.drop(['target'], axis=1)
        y = df_train.target

        return X, y

    def train(self):
        model = cb.CatBoostClassifier(depth=8, custom_loss=['AUC', 'Accuracy'])
        cat_features = [0, 1, 2, 3]

        X, y = self.prepare_data()
        X_train_w, X_test_w, y_train, y_test = train_test_split(
            X, y, test_size=0.2)

        model.fit(X_train_w, y_train, cat_features, eval_set=(
            X_test_w, y_test), use_best_model=True, plot=True)

        model.save_model('gender_predictor.cbm')

        return model

    def predict(self, df_name='correct_df.csv', model_name='gender_predictor.cbm'):
        model = cb.CatBoostClassifier()
        model.load_model(model_name)
        df_test = pd.read_csv(df_name)
        data_test = df_test[['LAST_NAME', 'NAME']].apply(
            lambda x: self.__preprocess(x['LAST_NAME'], x['NAME']), axis=1)

        df_test['gender'] = model.predict(data_test)

        df_test.to_csv('database.csv', index=False)

        return df_test


def make_predict(df_name='correct_df.csv'):
    gp = GenderPredictor()
    return gp.predict(df_name)
