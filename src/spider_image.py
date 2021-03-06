# -*- coding:utf-8 -*-
"""
@Author:jiaxinchen
@Email:jiaxinchen@njust.edu.cn
@Institution:NJUST.PCALab
"""
import urllib2
import json
import demjson
import sys
import os
import time
# print sys.getdefaultencoding()
# exit()
from  bs4 import BeautifulSoup as soup
UserAgent=["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"]
prefix = "https://www.thefacewemake.com/"
pages = [ prefix+ "page/{}/".format(i+1) for i in range(16)]
pages[0] = prefix
driver = webdriver.Chrome("C:/Users/80566/Downloads/chromedriver_win32/chromedriver.exe")
# global UA_index
UA_index = 1

def check_file(f):
    return os.path.isfile(f)
def check_path(path):
    if os.path.exists(path)==False:
        os.makedirs(path)

# def getBody(url,index):
#     """
#     index: the index for prepared UserAgent
#     """
#     body=""
#     drive.get(url)
#     doc = driver.page_source
#     try:
#       request=urllib2.Request(url)
#       request.add_header("User-Agent",UserAgent[index%2])
#       response=urllib2.urlopen(request)
#       body=response.read()
#       if response:
#           response.close()
#           print "response status:close"
#     except urllib2.URLError as e:
#       if(hasattr(e,"reason")):
#           print "failed reach the server!"
#           print "reason:", e.reason
#       elif(hasattr(e,"code")):
#           print  "The server couldn't fulfill the request"
#           print  "Error code:", e.code
#           print "Return content:", e.read()
#       return 'false'
#     return body
def getBody(url):
    """
    index: the index for prepared UserAgent
    """
    body=""
    drive.get(url)
    body = driver.page_source
    return body

def transfertodic(body):
     body=demjson.decode(body,'utf-8')
     return body

def get_subjects_IOP_urls(url, index=0):
    """
        get subject url in One pages
    """
    # f = open("test.txt", 'a+')
    body = getBody(url, index%2)
    # UA_index += 1
    if body == 'false':
        return 'false'
    elif body == None:
        return "false"
    html = soup(body,'html.parser')
    # print(html.original_encoding)
    div_content = html.find(id="content")
    a_elems = div_content.find_all("a", recursive=True, class_="entry-image-post-link".encode('utf-8'))
    hrefs = []
    for a in a_elems:
        hrefs.append(a["href"])
    return hrefs

def get_subject_images_urls(url, index=0):
    body = getBody(url, index%2)
    if body=='false':
        return 'false'
    elif body==None:
        return "false"
    html = soup(body, 'html.parser')
    div_content = html.find(id="gallery-container")
    img_blocks = div_content.find_all('span', class_="entry-image")
    img_hrefs = []
    for block in img_blocks:
        href = block.img['src']
        img_hrefs.append(href)


def get_All_subjects(urls, index_seed=0, url_f="subjects_url.txt"):
    sub_hrefs = []
    # collect the subject urls
    print "collect the subject urls...."
    if check_file(url_f)==False:
        retry = 0
        i=0 
        while i<len(urls):
            print(urls[i])
            hrefs = get_subjects_IOP_urls(urls[i], index_seed)
            index_seed +=1
            if type(hrefs)==str:
                time.sleep(60*1)
                retry += 1
                if retry > 10:
                    i += 1
                    retry = 0
                else:
                    continue
            i+=1
            sub_hrefs.extend(hrefs)
        f = open(url_f, 'a+')
        for h in sub_hrefs:
            print >> f, h.strip()
        f.close()
    else:
        f = open(url_f,'r')
        lines = f.readlines()
        for l in lines():
            sub_hrefs.append(l.strip())
        f.close()



    print "collect the imgs urls...."
    imgs_group = {}
    i = 0
    retry = 0
    while i < len(sub_hrefs):
        h = sub_hrefs[i]
        imgurl_list = []
        name = h.strip().split('/')[-2]
        print "images of :" + name
        path = "../data/" + name
        check_path(path)
        if check_file(os.path.join(path, "image_urls.txt"))==False:
            hrefs = get_subject_images_urls(h, index_seed)
            if type(hrefs)==str:
                time.sleep(60*1)
                retry += 1
                if retry > 10:
                    i += 1
                    retry = 0
                else:
                    continue
            imgurl_list.extend(hrefs)
            index_seed += 1
            img_file= open(os.path.join(path, "image_urls.txt"), 'a+')
            for l in imgurl_list:
                print >> img_file, l.strip()
            img_file.close()
        else:
            img_file = open(os.path.join(path, "image_urls.txt"), 'r')
            lines = img.readlines()
            for l in lines:
                imgurl_list.append(l.strip())
            img_file.close()
        imgs_group[name] = imgurl_list

    return imgs_group


if __name__=="__main__":
    # hrefs = get_subjects_IOP(pages[1], 1)
    # print(hrefs[0].strip().split('/')[-2])
    get_All_subjects(pages, index_seed=0, url_f="subjects_url.txt")
    print imgs_group