from bs4 import BeautifulSoup
import requests

#function to return a dicionary object with student populations
def student_population(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source,'lxml')
    infobox_tag = soup.find('table',{'class':'infobox vcard'})

    final_dict = {}

    #loop through all tr tags in the infobox from a Wikipedia page
    for tr in infobox_tag.find_all('tr'):
        if 'Students' in tr.text:
            value = tr.find('td').text.split()[0]
            final_dict['students'] = value
        elif 'Undergraduates' in tr.text:
            value = tr.find('td').text.split()[0]
            final_dict['undergraduates'] = value
        elif 'Postgraduates' in tr.text:
            value = tr.find('td').text.split()[0]
            final_dict['postgraduates'] = value

    return final_dict

url_list = []
url_list.append('https://en.wikipedia.org/wiki/Michigan_State_University')
url_list.append('https://en.wikipedia.org/wiki/University_of_Virginia')

for url in url_list:
    print(url)
    print(student_population(url), '\n')