
from flask import Flask,render_template,request


import requests
import psycopg2


def fetch(connection,cursor, promt):
    print('fetching data')
    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            f'text': "'"+promt+ "'",
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )

    # print(r.json())
    url_image = r.json()["output_url"]
    cursor.execute("INSERT INTO images VALUES (%s, %s);",  (promt, url_image))
    connection.commit()

    return url_image

def get_data(promt):
   
      connection = psycopg2.connect(dbname='text2img', user='postgres', password='admin', host='localhost')
      cursor = connection.cursor()
      
      try:
         cursor.execute(f"SELECT image_url FROM Images WHERE prompt = '" + promt + "';")
         record = cursor.fetchall()
         
         if record == []:
               return fetch(promt)
         else:
               for row in record:
                  return row[0]
         

      except:
         return fetch(connection,cursor, promt)   


      cursor.close()
      connection.close()
      print("PostgreSQL connection is closed")
 
app = Flask(__name__)
 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form

        data = form_data.to_dict(flat=False)

        image_url = get_data(data["Your photo"][0])

        return render_template('data.html',form_data = form_data, image_url=image_url)
 

app.run(host='0.0.0.0', port=5000)
