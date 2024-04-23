# -*- coding:utf-8 -*-
"""@package web
This method is responsible for the inner workings of the different web pages in this application.
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

bootstrap = Bootstrap(app)

def getData():
    """
    Gets and returns the csvOut.csv as a DataFrame.

    Returns
    -------
    data : Pandas DataFrame
        The data that contains the features for each image.
    """
    s3 = boto3.client('s3')
    path = 's3://cornimagesbucket/csvOut.csv'

    data = pd.read_csv(path, index_col = 0, header = None)
    data.columns = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','true_value']

    data_mod = data.astype({'8': 'int32','9': 'int32','10': 'int32','12': 'int32','14': 'int32', 'true_value': 'string'})
    
    truth_table = data_mod.iloc[:, -1:]
    # print(truth_table.iloc[:, :])
    session['truth'] = truth_table.to_json()    
    
    return data_mod.iloc[:, :-1]

def createMLModel(data):
    """
    Prepares the training set and creates a machine learning model using the training set.

    Parameters
    ----------
    data : Pandas DataFrame
        The data that contains the features for each image

    Returns
    -------
    ml_model : ML_Model class object
        ml_model created from the training set.
    train_img_names : String
        The names of the images.
    """
    train_img_names, train_img_label = list(zip(*session['train']))
    train_set = data.loc[train_img_names, :]
    train_set['y_value'] = train_img_label

    truth_table = pd.read_json(session['truth'])
    ml_model = ML_Model(train_set, RandomForestClassifier(), DataPreprocessing(True), truth_table)
    return ml_model, train_img_names

def renderLabel(form):
    """
    prepares a render_template to show the label.html web page.

    Parameters
    ----------
    form : LabelForm class object
        form to be used when displaying label.html

    Returns
    -------
    render_template : flask function
        renders the label.html webpage.
    """
    queue = session['queue']
    img = queue.pop()
    session['queue'] = queue
    return render_template(url_for('label'), form = form, picture = img, confidence = session['confidence'])

def initializeAL(form, confidence_break = .7):
    """
    Initializes the active learning model and sets up the webpage with everything needed to run the application.

    Parameters
    ----------
    form : LabelForm class object
        form to be used when displaying label.html
    confidence_break : number
        How confident the model is.

    Returns
    -------
    render_template : flask function
        renders the label.html webpage.
    """
    preprocess = DataPreprocessing(True)
    ml_classifier = RandomForestClassifier()
    data = getData()
    al_model = Active_ML_Model(data, ml_classifier, preprocess)
    
    session['confidence'] = 0
    session['confidence_break'] = confidence_break
    session['labels'] = []
    session['sample_idx'] = list(al_model.sample.index.values)
    session['test'] = list(al_model.test.index.values)
    session['train'] = al_model.train
    session['model'] = True
    session['queue'] = list(al_model.sample.index.values)
    

    return renderLabel(form)

def getNextSetOfImages(form, sampling_method):
    """
    Uses a sampling method to get the next set of images needed to be labeled.

    Parameters
    ----------
    form : LabelForm class object
        form to be used when displaying label.html
    sampling_method : SamplingMethods Function
        function that returns the queue and the new test set that does not contain the queue.

    Returns
    -------
    render_template : flask function
        renders the label.html webpage.
    """
    data = getData()
    ml_model, train_img_names = createMLModel(data)
    test_set = data[data.index.isin(train_img_names) == False]

    session['sample_idx'], session['test'] = sampling_method(ml_model, test_set, 5)
    session['queue'] = session['sample_idx'].copy()

    return renderLabel(form)

def prepareResults(images, labels, fromLabelsPage):
    """
    Creates the new machine learning model and gets the confidence of the machine learning model.

    Parameters
    ----------
    form : LabelForm class object
        form to be used when displaying label.html

    Returns
    -------
    render_template : flask function
        renders the appropriate webpage based on new confidence score.
    """
    session['sample'] = tuple(zip(images, labels))

    truth_table = pd.read_json(session['truth'])
    
    
    if session['train'] != None:
        session['train'] = session['train'] + session['sample']
    else:
        session['train'] = session['sample']

    data = getData()
    ml_model, train_img_names = createMLModel(data)

    session['confidence'] = np.mean(ml_model.K_fold())
    session['labels'] = []

    if session['confidence'] < session['confidence_break']:
        health_pic, blight_pic = ml_model.infoForProgress(train_img_names)
        if fromLabelsPage:
            return render_template('intermediate.html', confidence = "{:.2%}".format(round(session['confidence'],4)), health_user = health_pic, blight_user = blight_pic, healthNum_user = len(health_pic), blightNum_user = len(blight_pic))
        else:
            return jsonify({"intermediate": "yes", 'confidence': "{:.2%}".format(round(session['confidence'],4)), "health_user": health_pic, "blight_user": blight_pic, "healthNum_user": len(health_pic), "blightNum_user": len(blight_pic)})
    else:
        test_set = data.loc[session['test'], :]
        health_pic_user, blight_pic_user, health_pic, blight_pic, health_pic_prob, blight_pic_prob, health_pic_true, blight_pic_true = ml_model.infoForResults(train_img_names, test_set)
        if fromLabelsPage:
            return render_template('final.html', confidence = "{:.2%}".format(round(session['confidence'],4)), health_user = health_pic_user, blight_user = blight_pic_user, healthNum_user = len(health_pic_user), blightNum_user = len(blight_pic_user), health_test = health_pic, unhealth_test = blight_pic, healthyNum = len(health_pic), unhealthyNum = len(blight_pic), healthyPct = "{:.2%}".format(len(health_pic)/(200-(len(health_pic_user)+len(blight_pic_user)))), unhealthyPct = "{:.2%}".format(len(blight_pic)/(200-(len(health_pic_user)+len(blight_pic_user)))), h_prob = health_pic_prob, b_prob = blight_pic_prob, h_true = health_pic_true, b_true = blight_pic_true)
        else:
            return jsonify({"intermediate": "no", "confidence": "{:.2%}".format(round(session['confidence'],4)), "health_user": health_pic_user, "blight_user": blight_pic_user, "healthNum_user": len(health_pic_user), "blightNum_user": len(blight_pic_user), "health_test": health_pic, "unhealth_test": blight_pic, "healthyNum": len(health_pic), "unhealthyNum": len(blight_pic), "healthyPct": "{:.2%}".format(len(health_pic)/(200-(len(health_pic_user)+len(blight_pic_user)))), "unhealthyPct": "{:.2%}".format(len(blight_pic)/(200-(len(health_pic_user)+len(blight_pic_user)))), "h_prob": health_pic_prob, "b_prob": blight_pic_prob, "h_true": health_pic_true, "b_true": blight_pic_true})

@app.route("/", methods=['GET'])
@app.route("/index.html",methods=['GET'])
def home():
    """
    Operates the root (/) and index(index.html) web pages.
    """
    session.pop('model', None)
    return render_template('index.html')

@app.route("/label.html",methods=['GET', 'POST'])
def label():
    """
    Operates the label(label.html) web page.
    """
    form = LabelForm()
    if 'model' not in session:#Start
        return initializeAL(form, .7)

    elif session['queue'] == [] and session['labels'] == []: # Need more pictures
        return getNextSetOfImages(form, lowestPercentage)

    elif form.is_submitted() and session['queue'] == []:# Finished Labeling
        session['labels'].append(form.choice.data)
        return prepareResults(session["sample_idx"], session["labels"], True)

    elif form.is_submitted() and session['queue'] != []: #Still gathering labels
        session['labels'].append(form.choice.data)
        return renderLabel(form)


    return render_template('label.html', form = form)

@app.route("/intermediate.html",methods=['GET'])
def intermediate():
    """
    Operates the intermediate(intermediate.html) web page.
    """
    return render_template('intermediate.html')

@app.route("/intermediate/<confidence>/<health_user>/<blight_user>/<healthNum_user>/<blightNum_user>", methods=['GET'])
def intermediatepage(confidence, health_user, blight_user, healthNum_user, blightNum_user):
    health_user = health_user.split(",")
    blight_user = blight_user.split(",")
    return render_template('intermediate.html', confidence=confidence, health_user=health_user, blight_user=blight_user, healthNum_user=healthNum_user, blightNum_user=blightNum_user)

@app.route("/final/<confidence>/<health_user>/<blight_user>/<healthNum_user>/<blightNum_user>/<health_test>/<unhealth_test>/<healthyNum>/<unhealthyNum>/<healthyPct>/<unhealthyPct>/<h_prob>/<b_prob>/<h_true>/<b_true>", methods=['GET'])
def finalpage(confidence, health_user, blight_user, healthNum_user, blightNum_user, health_test, unhealth_test, healthyNum, unhealthyNum, healthyPct, unhealthyPct, h_prob, b_prob, h_true, b_true):
    health_user = health_user.split(",")
    blight_user = blight_user.split(",")
    health_test = health_test.split(",")
    unhealth_test = unhealth_test.split(",")
    healthyNum = int(healthyNum)
    unhealthyNum = int(unhealthyNum)
    h_prob = [float(x) for x in h_prob.split(",")]
    b_prob = [float(x) for x in b_prob.split(",")]
    h_true = h_true.split(",")
    b_true = b_true.split(",")
    return render_template('final.html', confidence=confidence, health_user=health_user, blight_user=blight_user, healthNum_user=healthNum_user, blightNum_user=blightNum_user, health_test=health_test, unhealth_test=unhealth_test, healthyNum=healthyNum, unhealthyNum=unhealthyNum, healthyPct=healthyPct, unhealthyPct=unhealthyPct, h_prob=h_prob, b_prob=b_prob, h_true=h_true, b_true=b_true)

@app.route("/final.html",methods=['GET', 'POST'])
def final():
    """
    Operates the final(final.html) web page.
    """
    if request.method == 'POST':
        labels = request.get_json()['labels']
        images = request.get_json()['images']
        return prepareResults(images, labels, False)

    else:
        return render_template('final.html')

@app.route("/feedback/<h_list>/<u_list>/<h_conf_list>/<u_conf_list>",methods=['GET'])
def feedback(h_list,u_list,h_conf_list,u_conf_list):
    """
    Operates the feedback(feedback.html) web page.
    """
    h_feedback_result = list(h_list.split(","))
    u_feedback_result = list(u_list.split(","))
    h_conf_result = list(h_conf_list.split(","))
    u_conf_result = list(u_conf_list.split(","))
    h_length = len(h_feedback_result)
    u_length = len(u_feedback_result)
    
    return render_template('feedback.html', healthy_list = h_feedback_result, unhealthy_list = u_feedback_result, healthy_conf_list = h_conf_result, unhealthy_conf_list = u_conf_result, h_list_length = h_length, u_list_length = u_length)

#app.run( host='127.0.0.1', port=5000, debug='True', use_reloader = False)