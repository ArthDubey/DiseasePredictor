import os
from flask import Flask, flash, render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_bootstrap import Bootstrap
import csv
import pandas as pd
import operator
import math
import time

reader=pd.read_csv('static/CSV/dataset_clean.csv')
df=pd.DataFrame(reader)
s=df['Target'].unique()

#print(len(s))

def get_in(d):
    m=0
    if(d=='High'):
        m=8
    if(d=='Medium'):
        m=5
    if(d=='Low'):
        m=3
    if(d=='Dont know'):
        m=5.3
    return m

def predict(s=[],ins=[]):
    res={}
    ls=len(s)
    os.remove("static/CSV/user.csv")
    reader=pd.read_csv("static/CSV/df_pivoted.csv")
    df=pd.DataFrame(reader)
    #df.to_csv("static/CSV/user.csv",index=False,encoding='utf8')
    for i in range(len(s)):
        for cn in df.columns:
            if(cn==s[i]):
                f=0
                for k in df[cn]:
                    g=get_in(ins[i])
                    if(k==1):
                        k=k*g
                    if(k!=1 and k!=0):
                        k=1
                        k=k*g
                        #print(k)
                    df[cn].values[f]=k
                    f=f+1
                    #ic=ic+1
    df.to_csv("static/CSV/user.csv",index=False,encoding='utf8')
    dc={}
    dnb={}
    rows=[]
    with open(r'static/CSV/user.csv') as csvfile:
        csvreader=csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)
    
    #dp={}
    #res={}
    for row in rows[1:148]:              #naive bayes algorithm
        cs=0
        ts=0
        for col in row:
            if(col!='0' and col!='1'):
                cs=cs+1
            elif(col=='1'):
                ts=ts+1
        nbs=((cs/ls)*(1/147))/(ls/405)
        nbs=math.sqrt(nbs)
        #nbs=math.sqrt(nbs)
        nbs=nbs-0.15
        dnb[row[1]]=nbs                 #naive bayes dictionary
            
    for row in rows[1:148]:
        sm=0
        for col in row:
            if(col=='0' or col=='5.3' or col=='3' or col=='5' or col=='8'):
                sm=sm+int(col)
            dc[row[1]]=sm
    for di in dnb:
        if(dnb[di]==dc[di]):
            dnb[di]*dc[di]
    sorted_dnb=sorted(dnb.items(), key=operator.itemgetter(1), reverse=True)
    res=sorted_dnb[0:4]
    res=res+sorted_dnb[15:16]
    res=res+sorted_dnb[100:101]
    res=res+sorted_dnb[400:401]
    return res    
            

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def main():
    return render_template('mainw.htm')

@app.route('/intro',methods=['GET','POST'])
def intro():
    if request.method == 'POST':
        return redirect(url_for('main'))
    return render_template('intro.html')

@app.route('/interview',methods=['GET','POST'])    #
def interview():
    time.sleep(5)
    return render_template('interview.html')

@app.route('/symp',methods=['GET','POST'])
def symp():
    if request.method == 'POST':
        return render_template(url_for('main'))
    return render_template('symp.html',symptoms=s)

@app.route('/results',methods=['GET','POST'])
def results():
    l=[]
    ins=[]
    d={}
    r=[]
    result={}
    if request.method == 'POST':
        symp1=request.form['symp1']
        l.append(symp1)
        symp2=request.form['symp2']
        l.append(symp2)
        symp3=request.form['symp3']
        l.append(symp3)
        symp4=request.form['symp4']
        l.append(symp4)
        symp5=request.form['symp5']
        l.append(symp5)
        ins1=request.form['ins1']
        ins.append(ins1)
        ins2=request.form['ins2']
        ins.append(ins2)
        ins3=request.form['ins3']
        ins.append(ins3)
        ins4=request.form['ins4']
        ins.append(ins4)
        ins5=request.form['ins5']
        ins.append(ins5)
        for a in range(0,5):
            d[l[a]]=ins[a]
        r=predict(l,ins)
        for i in r:
            result[i[0]]=i[1]
        print(result)
    return render_template('results.html',symptoms=d, results=result)
        #for rp in result:
        #    resultf=rp[0]
        #    level=rp[1]  
         

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)


