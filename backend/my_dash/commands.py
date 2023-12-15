"""Flask app commands."""
import os
import pandas as pd

from .models import db


def load_csv_from_folder():
    """CSV file loading from folder."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    path_to_csv = os.path.join(basedir, 'human_data/result.csv')

    if (os.path.exists(path_to_csv) and
            os.path.isfile(path_to_csv) and
            os.access(path_to_csv, os.R_OK)):
        add_csv_to_db(path_to_csv)
    else:
        print('Путь не существует, объект не является файлом'
              'или к нему нет доступа.')


def add_csv_to_db(path_to_csv):
    """Pandas CSV file loading and adding to db."""
    df = pd.read_csv(path_to_csv)
    df.to_sql('human_data', con=db.engine, if_exists='append', index=False)
