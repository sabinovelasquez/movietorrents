import glob
import os
import tkinter
import requests
import time

from pick import pick
from tkinter import filedialog
from bs4 import BeautifulSoup

pagination_count = 2
movies = []
options_title_ext = 'Selecciona la extensión de tus películas:'
options_ext = ['.mp4', '.avi', '.mkv', '.mov']
options_torrent_title = 'Selecciona la fuente de torrents:'
options_torrent = ['https://yts.pm/', 'https://yts.am/']

print('Selecciona ubicación de tus películas.')

root = tkinter.Tk()
root.withdraw()
def search_for_file_path ():
  currdir = os.getcwd()
  tempdir = filedialog.askdirectory(parent=root, initialdir=currdir)
  root.quit()
  return tempdir
file_path_variable = search_for_file_path()
path = file_path_variable

file_type, index_file = pick(options_ext, options_title_ext)
files = [f for f in glob.glob(path + '**/*' + file_type, recursive=True)]
for index_file, f in enumerate(files):
  fileName = files[index_file][:(len(file_type)*-1)]
  fileName = fileName[(len(path)+1):]
  files[index_file] = fileName

torrent_url, index_torrent = pick(options_torrent, options_torrent_title)

def get_movies(pagination_count):
  url = str(options_torrent[index_torrent]) + 'browse-movies?page=' + str(pagination_count)
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  prospect_movies = soup.find_all(class_ = 'browse-movie-wrap')
  for movie in prospect_movies:
    temp_rating = movie.find('h4', class_ = 'rating').string
    rating = temp_rating.split(' ')
    if(float(rating[0]) >= int(rating_filter)):
      worth_it = movie.find('a', string='1080p')
      temp_url = str(options_torrent[index_torrent] + worth_it['href'])
      movies.append(temp_url)
  pagination_count += 1
  print(movies)
  time.sleep(5)
  get_movies(pagination_count)

rating_filter = input('Ingresa rating de 1 a 10 para filtrar: ')
get_movies(pagination_count)
