import pickle

import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen

import sklearn
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import LinearRegression

from sklearn.svm import SVR
import xgboost as xgb
import pandas as pd


class FirstPlace:
    def __init__(self, path: str, date: str = 'Начало нед') -> None:
        self.path = path
        self.date = date
        self.maxlag = 28
        self.test = 'ssr_chi2test'
        df = pd.read_excel(self.path, parse_dates=[self.date], index_col=self.date, skiprows=5)
        df.drop(columns=['год'], axis=1, inplace=True)
        df.drop(columns=['Unnamed: 147'], axis=1, inplace=True)
        df = df.iloc[:244]
        object_columns = list(df.select_dtypes(['object']).columns)
        for col in object_columns:
            df[col] = df[col].replace(' ', 0)
        for col in object_columns:
            df[col] = df[col].astype(float)
        self.df = df.fillna(0)

    def fit_stacking(self, interval: int = 28):
        df_pred = self.df
        df_pred['quarter'] = df_pred.index.quarter
        df_pred['month'] = df_pred.index.month
        df_pred['year'] = df_pred.index.year
        df_pred['dayofyear'] = df_pred.index.dayofyear
        df_pred['dayofmonth'] = df_pred.index.day
        self.nobs = interval
        df_train = df_pred[0:-self.nobs]
        df_test = df_pred[-self.nobs:]

        self.X_train, self.y_train = df_train.drop('Продажи, рубли', axis=1), df_train['Продажи, рубли']
        self.X_test, self.y_test = df_test.drop('Продажи, рубли', axis=1), df_test['Продажи, рубли']
        self.xgb_model = pickle.load(open('fv_bb_package/model_1.pkl', 'rb'))
        # self.xgb_model = pickle.load(open('./model_1.pkl', 'rb'))
        estimators = [
            ('xgb', self.xgb_model),
            ('svr', SVR()),
            ('lr', LinearRegression())
        ]
        self.reg = StackingRegressor(
            estimators=estimators,
            final_estimator=RandomForestRegressor(n_estimators=700, min_samples_split=12, min_samples_leaf=2,
                                                  max_features='sqrt', max_depth=13, random_state=42))

        self.reg.fit(self.X_train, self.y_train)
        return self.reg.score(self.X_test, self.y_test)

    def get_predict(self):
        return list(self.reg.predict(self.X_test))

    def get_indexes(self):
        return list(self.df.index.strftime('%Y-%m-%d'))

    def get_history_value(self):
        return list(self.y_train)

    def get_heatmap(self):
        m = self.df.corr()[['Продажи, рубли']]
        m = m.dropna()
        m = m[m['Продажи, рубли'] >= 0]
        m = m.sort_values(by='Продажи, рубли', ascending=False)
        column_names = ['Продажи, рубли']
        top = m.loc[m['Продажи, рубли'] > 0.4]
        top = top.iloc[2:]
        column_names += top.index.tolist()
        return m.iloc[2:].to_dict().get(column_names[0])

    def _get_corr_stat(self):
        m = self.df.corr()[['Продажи, рубли']]
        m = m.dropna()
        m = m[m['Продажи, рубли'] >= 0]
        m = m.sort_values(by='Продажи, рубли', ascending=False)
        column_names = ['Продажи, рубли']
        top = m.loc[m['Продажи, рубли'] > 0.4]
        top = top.iloc[2:]
        column_names += top.index.tolist()
        return column_names

    def _grangers_causation_matrix(self, data, variables, test='ssr_chi2test', verbose=False):
        df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
        for c in df.columns:
            for r in df.index:
                test_result = grangercausalitytests(data[[r, c]], maxlag=self.maxlag, verbose=False)
                p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(self.maxlag)]
                if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
                min_p_value = np.min(p_values)
                df.loc[r, c] = min_p_value
        df.columns = [var + '_x' for var in variables]
        df.index = [var + '_y' for var in variables]
        return df.to_dict()

    def granger_test(self):
        return self._grangers_causation_matrix(self.df[self._get_corr_stat()],
                                               variables=self.df[self._get_corr_stat()].columns)

    def _adfuller_test(self, series, signif=0.05, name='', verbose=False):
        r = adfuller(series, autolag='AIC')
        output = {'test_statistic': round(r[0], 4), 'pvalue': round(r[1], 4), 'n_lags': round(r[2], 4), 'n_obs': r[3]}
        p_value = output['pvalue']

        if p_value <= signif:
            return {name: 'is stationary'}
        else:
            return {name: 'is not stationary'}

    def get_adfuller_test(self):
        total_data = {}
        df_train = self.df[self._get_corr_stat()][0:-self.nobs]
        for name, column in df_train.items():
            total_data.update(self._adfuller_test(column, name=column.name))
        return total_data

# ahh = FirstPlace('train.xlsx')
# print(ahh.fit_stacking())
# print(ahh.get_predict_indexes())
# print(ahh.get_predict())
# print(ahh.get_heatmap())
# print(ahh.granger_test())
# print(ahh.get_adfuller_test())
