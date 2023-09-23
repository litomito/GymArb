#!/usr/bin/env python3
import json
import html
import requests
import datetime
import locale
import feedparser
from time import time, sleep
from flask import Flask, render_template, Markup
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

ad = ''

#x = datetime.datetime.now()

@app.route('/uppdatera', methods = ['POST'])
def login():
    global ad
    ad = request.form['nm']
    return redirect(url_for('index'))

def samlainfo(ud):
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://gettime.ga',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'DNT': '1',
    'Referer': 'https://gettime.ga/',
    'Connection': 'keep-alive',
    # Requests doesn't support trailers
    # 'TE': 'trailers', 
  }

  params = {
    'id': ud,
    'day': '0',
    'week': dt.strftime("%U"),
    'year': '2023',
    'width': '1503',
    'height': '750',
    'privateID': '0',
    'darkmode': '1',
    'darkmodesetting': '1',
    'isMobile': '0',
    'school': 'NTI södertörn',
  }
  try:
    response = requests.get('https://www.gettime.ga/API/GENERATE_HTML', params=params, headers=headers)
  except requests.exceptions.RequestException as e:
    print("FAAAAAIL!!!")
    #return "fail"

#   with open("test.txt","w") as f:
#     f.write(response.json()['result']['html'])

#ut = json.loads(response)

  ut = response.json()
  return ut['result']['html']
# nyskriv = skriv[1:]


dt = datetime.datetime.now()

#dt = datetime.now()
#now = datetime.now()

# get day of week as an integer
day = dt.weekday() + 1


a = []
timplus = str(dt.now().strftime("%H")) + str(dt.now().strftime("%M"))
dennatimme = int(timplus)
print(dennatimme)



     
#SLbuss [Avgång från Huddinge Sjukhus]

headers = {
    'authority': 'webcloud.sl.se',
    'accept': '*/*',
    'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://sl.se',
    'referer': 'https://sl.se/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

params = {
    'mode': 'departures',
    'origPlaceId': 'QT0xQE89SHVkZGluZ2Ugc2p1a2h1cyAoSHVkZGluZ2UpQFg9MTc5Mzc1NDNAWT01OTIyMjI2NUBVPTc0QEw9MzAwMTA3MDAwQEI9MUBwPTE2NzA5ODY4MTBA',
    'origSiteId': '7000',
    'desiredResults': '10',
    'origName': 'Huddinge sjukhus (Huddinge)',
}

resp = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers,verify=False)
#print(response.text)

SLbuss = []
for t in resp.json():
    params = {
        'mot': t['destination'],
        'linje': t['transport']['line'],
        'om': t['time']['displayTime'],
        'stop': t['track']
    }
    #print(params)


try: 
    for s in resp.json():
        p = f"Buss {s['transport']['line']} mot {s['destination']} om: {s['time']['displayTime']} från STOP: {s['track']}"
        print(p)
        
        SLbuss.append(p)
except:
    print("error")
pass




#SLpendel [Avgång från Flemingsberg Station]
headers = {
    'authority': 'webcloud.sl.se',
    'accept': '*/*',
    'accept-language': 'sv,en-US;q=0.9,en;q=0.8',
    'origin': 'https://sl.se',
    'referer': 'https://sl.se/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
}

params = {
    'mode': 'departures',
    'origPlaceId': 'QT0xQE89RmxlbWluZ3NiZXJncyBzdGF0aW9uIChIdWRkaW5nZSlAWD0xNzk0Nzk4OEBZPTU5MjE5MjM2QFU9NzRATD0zMDAxMDcwMDZAQj0xQHA9MTY3MzQ5MjQyMEA=',
    'origSiteId': '7006',
    'desiredResults': '3',
    'origName': 'Flemingsbergs station (Huddinge)',
}

response = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers, verify=False)
#print(response.text)

SLpendel = []
for o in response.json():
    params = {
        'linje': o['transport']['line'],
        'mot': o['destination'],
        'om': o['time']['displayTime'],
        'transportType': o['transport']['transportType'],
        'spår': o['track']
    }
    for key, value in params.items():
        if key == "transportType" and value == "Train":
            z = f"Pendel linje {params['linje']} mot {params['mot']} om: {params['om']} från spår: {params['spår']}"
            print(z)
            SLpendel.append(z)

SLpendel = SLpendel



#Week
week_number_new = dt.isocalendar().week
print ("Vecka: " + str(week_number_new))
week = week_number_new


#Gets current date in format: Monday, 1 January. 
#ddm = datetime.datetime.now()
locale.setlocale(locale.LC_TIME, "sv_SE") # swedish
print(dt.strftime("%A, %d %B"))
date = dt.strftime("%A, %d %B")



@app.route("/")
def index():
  if ad == '':
    return render_template("indexfail.html")
  else:
    return render_template("index.html", output=Markup(samlainfo(ad)))

@app.route("/sl")
def sl():
        
  #SLbuss [Avgång från Huddinge Sjukhus]

  headers = {
      'authority': 'webcloud.sl.se',
      'accept': '*/*',
      'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
      'origin': 'https://sl.se',
      'referer': 'https://sl.se/',
      'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
  }

  params = {
      'mode': 'departures',
      'origPlaceId': 'QT0xQE89SHVkZGluZ2Ugc2p1a2h1cyAoSHVkZGluZ2UpQFg9MTc5Mzc1NDNAWT01OTIyMjI2NUBVPTc0QEw9MzAwMTA3MDAwQEI9MUBwPTE2NzA5ODY4MTBA',
      'origSiteId': '7000',
      'desiredResults': '10',
      'origName': 'Huddinge sjukhus (Huddinge)',
  }

  resp = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers,verify=False)
  #print(response.text)

  SLbuss = []
  for t in resp.json():
      params = {
          'mot': t['destination'],
          'linje': t['transport']['line'],
          'om': t['time']['displayTime'],
          'stop': t['track']
      }
      #print(params)


  try: 
      for s in resp.json():
          p = f"Buss {s['transport']['line']} mot {s['destination']} om: {s['time']['displayTime']} från STOP: {s['track']}"
          print(p)
          
          SLbuss.append(p)
  except:
      print("error")
  pass

  #SLpendel [Avgång från Flemingsberg Station]
  headers = {
      'authority': 'webcloud.sl.se',
      'accept': '*/*',
      'accept-language': 'sv,en-US;q=0.9,en;q=0.8',
      'origin': 'https://sl.se',
      'referer': 'https://sl.se/',
      'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile': '?1',
      'sec-ch-ua-platform': '"Android"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
  }

  params = {
      'mode': 'departures',
      'origPlaceId': 'QT0xQE89RmxlbWluZ3NiZXJncyBzdGF0aW9uIChIdWRkaW5nZSlAWD0xNzk0Nzk4OEBZPTU5MjE5MjM2QFU9NzRATD0zMDAxMDcwMDZAQj0xQHA9MTY3MzQ5MjQyMEA=',
      'origSiteId': '7006',
      'desiredResults': '3',
      'origName': 'Flemingsbergs station (Huddinge)',
  }

  response = requests.get('https://webcloud.sl.se/api/v2/departures', params=params, headers=headers, verify=False)
  #print(response.text)

  SLpendel = []
  for o in response.json():
      params = {
          'linje': o['transport']['line'],
          'mot': o['destination'],
          'om': o['time']['displayTime'],
          'transportType': o['transport']['transportType'],
          'spår': o['track']
      }
      for key, value in params.items():
          if key == "transportType" and value == "Train":
              z = f"Pendel linje {params['linje']} mot {params['mot']} om: {params['om']} från spår: {params['spår']}"
              print(z)
              SLpendel.append(z)

  SLpendel = SLpendel
  return render_template('index2.html', week=week, datum=date, SLbuss=SLbuss, SLpendel=SLpendel)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)