import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# combine results of API query
def save_combined_API_results():
    csv_files = glob.glob('Data/final_tmdb_data_*.0.csv.gz')
    tmdb_results_df = pd.concat((pd.read_csv(f, lineterminator='\n') for f in csv_files),
                                ignore_index=True)
    tmdb_results_df.to_csv('Data/tmdb_results_combined.csv.gz',
                           compression="gzip")

def eda(df):
    # financial info
    num_with_budget = len(df[df['budget'] > 0])
    num_with_revenue = len(df[df['revenue']> 0])
    ## use only movies with both budget and revenue information for rest of analysis
    budget_df = df[(df['budget'] > 0) | (df['revenue'] > 0)]

    # this is needlessly complicated, but i will fix later
    basic_bar(('Total Movies', 'Movies with Budget Info', 'Movies with Revenue Info', 'Movies with Budget and Revenue'),
              (len(df), num_with_budget, num_with_revenue, len(budget_df)),
              label_rot=-45,
              save_name='img/financial_eda.png',
              title='Financial Information',
              style_name='fivethirtyeight',
              y_lab='Movies in Dataset'
              )

    # Movies in each certification category
    basic_bar(x = budget_df['certification'].unique().astype(str),
              height = budget_df['certification'].value_counts(dropna=False),
              label_rot=-45,
              save_name='img/num_movies_certification.png',
              title='Certification Categories (Ratings)',
              style_name='fivethirtyeight',
              y_lab='Movies in Dataset')

    # Budget per certification Category
    basic_bar(x = budget_df['certification'].unique().astype(str),
              height = budget_df.groupby(['certification'], dropna=False)['budget'].mean(),
              label_rot=-45,
              save_name='img/ave_bud_by_cert.png',
              title='Budget per Certification Category',
              style_name='fivethirtyeight',
              y_lab='Average Budget')

    # Revenue per certification Category
    basic_bar(x = budget_df['certification'].unique().astype(str),
              height = budget_df.groupby(['certification'], dropna=False)['revenue'].mean(),
              label_rot=-45,
              save_name='img/ave_rev_by_cert.png',
              title='Revenue per Certification Category',
              style_name='fivethirtyeight',
              y_lab='Average Revenue')

    # Profit per certification Category
    basic_bar(x = budget_df['certification'].unique().astype(str),
              height = budget_df.groupby(['certification'], dropna=False)['revenue'].mean() - budget_df.groupby(['certification'], dropna=False)['budget'].mean(),
              label_rot=-45,
              save_name='img/ave_profit_by_cert.png',
              title='Profit per Certification Category',
              style_name='fivethirtyeight',
              y_lab='Average Profit (Revenue-Budget)')



def basic_bar(x, height, title='', x_lab='', y_lab='', label_rot=0, save_name='', style_name=''):
    if style_name:
        plt.style.use(style_name)
    else:
        plt.style.use('default')
    fig = plt.figure()
    ax = plt.axes()
    ax.bar(x=x, height=height)
    if title:
        ax.set_title(title)
    if x_lab:
        ax.set_xlabel(x_lab)
    if y_lab:
        ax.set_ylabel(y_lab)
    if label_rot:
        plt.xticks(rotation=label_rot)
    if save_name:
        plt.savefig(save_name, bbox_inches='tight')

    plt.show()




if __name__ == '__main__':
    # only need to run once
    ## save_combined_API_results()
    tmdb_df = pd.read_csv('Data/tmdb_results_combined.csv.gz',
                          lineterminator='\n')
    eda(tmdb_df)

