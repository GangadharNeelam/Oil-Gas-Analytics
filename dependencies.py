import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib import style
from matplotlib import pyplot as plt
from itertools import permutations

from scipy.signal import hilbert
from scipy.stats import skew

from PIL import Image

import streamlit as st
from streamlit.elements import image as st_image
from streamlit_option_menu import option_menu

import plotly.express as px
import plotly.graph_objs as go
import plotly.tools as tls

import segyio

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor

import lightgbm as lgb
import xgboost as xgb

import joblib
import pickle