#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module connects to database and updates threshold based changing times."""

import json
import os
import pandas as pd
from sqlalchemy import create_engine


def initialize_database():
    """
    This function read Database configuration file

    :return: DataBase connection engine
    """
    directory = os.path.dirname(__file__)
    with open(os.path.join(directory, "config.json"), 'r') as json_data_file:
        db_config = json.load(json_data_file)
    eng = create_engine('postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'.format(user=db_config['postgresql']['user'],
                                                                                            password=db_config['postgresql']['passwd'],
                                                                                            host=db_config['postgresql']['host'],
                                                                                            port=db_config['postgresql']['port'],
                                                                                            db=db_config['postgresql']['db']),
                        client_encoding='utf8')
    return eng


def get_data_short_glvt_sorted():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  data_short_glvt_sorted"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='clu_15_pur')

def get_clu_15_averages():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  clu_15_averages"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='clu_15_pur')

def get_clu_15_demographics():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  clu_15_demographics"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='clu_15_pur')

def get_kmean15_averages():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  kmean15_averages"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='kmean15')

def get_kmean15_demographics():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  kmean15_demographics"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='kmean15')

def get_kmean15_sa_averages():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  kmean15_sa_averages"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='kmean15')

def get_x_y_clusters():
    """
    This function initialize DataBase connection, calculate new threshold and update DataBase

    :return:
    """
    engine = initialize_database()
    sql_query = """SELECT *  FROM  x_y_clusters"""
    return pd.read_sql_query(sql_query, engine).sort_values(by='clu_15_pur')

