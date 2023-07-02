import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
import numpy as np

ulke = gp.read_file("countries.geojson")

url = "https://www.topuniversities.com/student-info/choosing-university/worlds-top-100-universities"

# Tarayıcı başlatma
driver = webdriver.Chrome("C:\DRIVERS\chromedriver_win32\chromedriver.exe")
driver.get(url)
driver.implicitly_wait(10)
element=[]
ulkelist=[]
for i in range(3,104):
    element.append(driver.find_elements(By.XPATH,f'//*[@id="block-tu-d8-content"]/div/article/div/div[2]/div[2]/div[5]/div/div/table/tbody/tr[{i}]/td[3]/p'))
    for value in element[i-3]:
        try:
            ulkelist.append(value.text)
        except:
            print("j")
ulkelist = [element.strip() for element in ulkelist]
element_counts = Counter(ulkelist)

df = pd.DataFrame.from_dict(element_counts, orient='index', columns=['ADET'])
df.index.name = 'ADMIN'
df = df.rename(index={'Mainland China': 'China', 'Hong Kong SAR': 'Hong Kong',"United States":"United States of America"})
ulke = ulke.merge(df, on='ADMIN', how='left')
print(df)
# Fill missing occurrence numbers with 0
ulke['Occurrence_Count'] = ulke['ADET'].fillna(0)
cmap = plt.cm.get_cmap('Set1')
fig, ax = plt.subplots(figsize=(10, 6))

#0 üni olan ülkeler için siyah renk kullanacağız.
color_for_zero = 'black'
#diğerleri için ise viridis paketini kullanalım.
cmap_positive = plt.cm.get_cmap('viridis')
ulke.loc[ulke['Occurrence_Count'] == 0].plot(color=color_for_zero, ax=ax)
ulke.loc[ulke['Occurrence_Count'] > 0].plot(column='Occurrence_Count', cmap=cmap_positive, linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
ax.set_title('Dünyada ilk 100 üniversite sıralamasında üniversitesi olan Ülkeler[Mert Taşdemir]')
plt.show()
