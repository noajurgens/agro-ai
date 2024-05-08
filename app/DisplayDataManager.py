# -*- coding:utf-8 -*-
"""
Created on Thu Apr 25 14:03:09 2024
@author: Ian
"""

from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from app import app
from app.DataPreprocessing import DataPreprocessing
from app.ML_Class import Active_ML_Model, AL_Encoder, ML_Model
from app.SamplingMethods import lowestPercentage
from app.forms import LabelForm
from flask_bootstrap import Bootstrap
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import os
import numpy as np
import boto3
from io import StringIO

class DisplayDataManager:
    """@package DisplayDataManager
    This is responsible for handling data and methods related to the images and their dataframes, specifically for display purposes.
    """

    def __init__(self):
        # temp
        print("NOT IMPLEMENTED")
    