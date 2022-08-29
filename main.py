
from concurrent.futures import process
from distutils.command.build import build
from doctest import OutputChecker
from importlib.resources import path
from sre_constants import SUCCESS
from flask import Flask, request, render_template,session
import os
import time
import numpy as np
import pandas as pd 
import subprocess
from datetime import datetime 
import pytz
import json
# initializing Flask app
app = Flask(__name__)
############################################################################################
##############################################################################################
#############################################################################
#############################################################################
### Connecting to Web interface
############################################################################
@app.route('/',methods=['post'])
def index():
    envelope = request.get_json()
    print("envelope is {} and type is {}".format(envelope,type(envelope)))
    pubsub_message = envelope["message"]
    print("message is {} and type is {}".format(pubsub_message,type(pubsub_message)))
#        error_message=json.loads(envelope)
    if isinstance(pubsub_message, dict):
        build_id = pubsub_message["attributes"]["buildId"]
        filter_ID ="ID="+build_id
        format_trigger = 'value(substitutions.TRIGGER_NAME)'
        try:
            outpu1=subprocess.check_output(["gcloud", "builds", "list", "--filter",filter_ID,"--format",format_trigger])
        except:
            print("error in retrieving trigger id")
        else:
            output1=outpu1.decode("utf-8")
            trigger_name = output1  ###
            print("trigger name is {}".format(trigger_name))
            filter_trigger = "status=SUCCESS AND substitutions.TRIGGER_NAME="+trigger_name 
            format_commit = "value(substitutions.COMMIT_SHA)"
            try:
                output2=subprocess.check_output(["gcloud", "builds", "list", "--filter",filter_trigger,"--format",format_commit])
            except:
                print("error in retriving commit_id")
            else:
                output2 =output2.decode("utf-8")
                commit_list = output2.split('\n')
                commit_id = commit_list[0]
                print("latest commit_id is {}".format(commit_id))
            if trigger_name == "cloud-mad-terraform":    
                path='/app/cloud-mad-terraform'
                os.chdir(path)
                try:
                    output3=subprocess.check_output(["git", "checkout",commit_id,"."])
                except:
                    print("Check out error with commit id {}".format(commit_id))
                    SUCCESS =24
                else:
                    message="Reverting to " + commit_id
                    try:
                        output4=subprocess.check_output(["git", "add","."])
                        output5=subprocess.check_output(["git", "commit","-m",message])
                        output6=subprocess.check_output(["git", "push"])
                    except:
                        print("errorafter check out in pushing ")
                        SUCCESS =25
                    else:
                        SUCCESS =0
        return(",204")
    else:
        print("bad message format")
        return(",100")
#    return render_template('alerts&notification.html',message)