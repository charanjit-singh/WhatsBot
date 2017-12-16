
def download_file(initialurl):

    import requests
    global downloading
    downloading=0
    from html.parser import HTMLParser
    result = requests.get(initialurl)
    if result.status_code==200:
        c = result.content
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(c, 'html.parser')
        link = soup.find_all("a", "btn btn-default hvr-shrink downloadButton")
        link=str(link)
        links=link.find('href')
        print(links)
        print(link.find('/">'))
        mm=link.split('=')
        mm=str(mm[2])
        mm=mm.split('"')
        url='https://nofile.io'+mm[1]
        import shutil
        response = requests.get(url, stream=True)
        if response.status_code==200:
            downloading=1
            with open('contacts.csv', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            downloading=0
        else:
            print('Error in url')
    else:
        print('Error in url')
 
if __name__=='__main__':
    x = input()
    download_file(x)
