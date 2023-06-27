from scipy.stats import pearsonr
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def getCorrTable(df):
    # get df with only numeric columns
    df = df.select_dtypes(include=np.number)
    rho = df.corr()
    pval = df.corr(method=lambda x, y: pearsonr(x, y)[1]) - np.eye(*rho.shape)
    p = pval.applymap(lambda x: ''.join(
        ['*' for t in [0.1, 0.05, 0.1] if x <= t]))
    return rho.round(2).astype(str) + p


def get_round_index(num):
    i = 0
    while (num < 1 and num != 0):
        i += 1
        num *= 10
    return i


def plot_two_columns_with_regression_line_and_color(df, x, y, color):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    current_df = pd.DataFrame()
    current_df = df.copy()[[x, y, color]]
    current_df.dropna(inplace=True)
    scatter = ax.scatter(
        current_df[x], current_df[y], c=current_df[color], cmap='viridis')
    legend1 = ax.legend(*scatter.legend_elements(num=3),
                        title=color)
    ax.add_artist(legend1)
    try:
        p_value = pearsonr(current_df[x], current_df[y])[1]
        round_index = get_round_index(p_value)
        p_value_str = str(
            round(pearsonr(current_df[x], current_df[y])[1], round_index))
    except:
        p_value_str = "null"
    ax.set_title('P value: ' + p_value_str + " Corr: " + str(
        round(current_df[x].corr(current_df[y]), 4)) + " N: " + str(len(current_df)), fontsize=20)
    X = current_df[x].values.reshape(-1, 1)
    Y = current_df[y].values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    plt.plot(X, Y_pred, color='red')
    plt.show()


def get_normelaized_df(df_origin, x, y, sd=2.5):
    df = df_origin.copy()
    x_mean = df[x].mean()
    x_sd = df[x].std()
    y_mean = df[y].mean()
    y_sd = df[y].std()
    df = df[(df[x] > (x_mean - (sd * x_sd))) &
            (df[x] < (x_mean + (sd * x_sd)))]
    df = df[(df[y] > (y_mean - (sd * y_sd))) &
            (df[y] < (y_mean + (sd * y_sd)))]
    return df


def add_regression_line(df, ax, x, y, color='red'):
    X = df[x].values.reshape(-1, 1)
    Y = df[y].values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    ax.plot(X, Y_pred, color=color)


def plot_multiple_two_columns_with_regression_line(plots, in_line=3, add_normelaized_title=False):
    import math

    def add_title(ax, x, y, fix_outliers, dataset_name):
        try:
            p_value = pearsonr(current_df[x], current_df[y])[1]
            round_index = get_round_index(p_value)
            p_value_str = str(
                round(pearsonr(current_df[x], current_df[y])[1], round_index))
        except:
            p_value_str = "null"

        try:
            corr = str(round(current_df[x].corr(current_df[y]), 4))
        except:
            corr = "null"

        title = dataset_name
        
        if add_normelaized_title:
            title += ", Normalized: " + str(fix_outliers) 
            
        title += "\n" + \
                'P value: ' + p_value_str + \
                " Corr: " + corr + \
                " N: " + str(len(current_df))
            
        
            
        ax.set_title(title)

    cols = in_line
    rows = math.ceil(len(plots) / in_line)
    fig, axis = plt.subplots(rows, cols, figsize=(20, 8 * rows))
    for i in range(len(plots)):
        df, x, y, fix_outliers, dataset_name = plots[i]

        if fix_outliers:
            df = get_normelaized_df(df, x, y)

        x_axis = math.floor(i / in_line)
        y_axis = i % in_line

        current_df = pd.DataFrame()

        current_df = df.copy()[[x, y]]
        current_df.dropna(inplace=True)
        if current_df[x].shape[0] == 0 or current_df[y].shape[0] == 0:
            continue
        if rows == 1:
            axis[y_axis].set_xlabel(x)
            axis[y_axis].set_ylabel(y)
            axis[y_axis].scatter(
                current_df[x], current_df[y])
            add_title(axis[y_axis], x, y, fix_outliers, dataset_name)
            add_regression_line(current_df, axis[y_axis], x, y)
        else:
            axis[x_axis, y_axis].set_xlabel(x)
            axis[x_axis, y_axis].set_ylabel(y)
            axis[x_axis, y_axis].scatter(current_df[x], current_df[y])
            add_title(axis[x_axis, y_axis], x, y, fix_outliers, dataset_name)
            add_regression_line(current_df, axis[x_axis, y_axis], x, y)

    plt.show()


def plot_two_cols_with_regression_line(df, x, y, x_label, y_label):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    current_df = pd.DataFrame()
    current_df = get_normelaized_df(df.copy()[[x, y]], x, y)
    current_df.dropna(inplace=True)
    ax.scatter(
        current_df[x], current_df[y], cmap='viridis')
    try:
        p_value = pearsonr(current_df[x], current_df[y])[1]
        round_index = get_round_index(p_value)
        p_value_str = str(
            round(pearsonr(current_df[x], current_df[y])[1], round_index))
    except:
        p_value_str = "null"
    ax.set_title('P value: ' + p_value_str + " Corr: " + str(
        round(current_df[x].corr(current_df[y]), 4)) + " N: " + str(len(current_df)), fontsize=20)
    add_regression_line(current_df, ax, x, y)
    plt.show()
