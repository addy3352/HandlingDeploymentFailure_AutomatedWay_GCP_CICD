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
    pubsub_message = envelope["message"]
    if isinstance(pubsub_message, dict):
        build_id = pubsub_message["attributes"]["buildId"] ## extract build id from the message
        filter_ID ="ID="+build_id
        format_trigger = 'value(substitutions.TRIGGER_NAME)'
        try:
            outpu1=subprocess.check_output(["gcloud", "builds", "list", "--filter",filter_ID,"--format",format_trigger]) ## get trigger name from build id
        except:
            print("error in retrieving trigger id")
        else:
            output1=outpu1.decode("utf-8")
            output1 = output1.strip("\n") ##stripped \n
            trigger_name = output1  ###
            filter_trigger = "status=SUCCESS AND substitutions.TRIGGER_NAME="+trigger_name  ### Only Successful build needs to be filtered
            format_commit = "value(substitutions.COMMIT_SHA)"
            try:
                output2=subprocess.check_output(["gcloud", "builds", "list", "--filter",filter_trigger,"--format",format_commit]) ## Get Commit id from trigger name
            except:
                print("error in retriving commit_id")
            else:
                output2 =output2.decode("utf-8")
                commit_list = output2.split('\n')
                commit_id = commit_list[0]
                print("latest commit_id is {}".format(commit_id))
            if trigger_name == "<trigger_name>":
                path='./<repo_name>'
                print("Checked in")
                if os.path.exists(path):
                    try:
                        output=subprocess.check_output(["rm","-r",path])   ### delete existing directory
                    except:
                        print("error in deleting directory")
                    else:
                        print("directory deleted successfully")
                else:
                    print("path doesn't exists")    
                try:
                    output11=subprocess.check_output(["git","init"])   
                    output7= subprocess.check_output(["git","clone","-b","<branch_name>","https://<personal access token>@github.com/<user_id>/<repo_name>.git"]) 
                    output8=subprocess.check_output(["git","remote","add" ,"base","https://<personal access token>@github.com/addy3352/<repo_name>.git"])
                    output9=subprocess.check_output(["git","config","--global" ,"user.email","<user email id>"])
                    output10=subprocess.check_output(["git","config","--local" ,"-l"])   
                except:
                    print(" Error in cloning")
                else:
                    os.chdir(path)
                    try:
                        output3=subprocess.check_output(["git","checkout",commit_id,"."])
                    except:
                        print("Check out error with commit id {}".format(commit_id))
                        SUCCESS =24
                    else:
                        message="Reverting to " + commit_id
                        output4=subprocess.check_output(["git", "add","."])
                        try:
#                            output4=subprocess.check_output(["git", "add","."])
                            output5=subprocess.check_output(["git", "commit","-m",message])
                            output6=subprocess.check_output(["git", "push"])
                        except:
                            print("errorafter check out in pushing-")
                            SUCCESS =25
                        else:
                            SUCCESS =0
            else:
                print("trigger name is not present {}".format(trigger_name))
        return(",204")
    else:
        print("bad message format")
        return(",400")
