# -*- coding:utf-8 -*-
'''
Author: Bu Kun
E-mail: bukun@osgeo.cn
CopyRight: http://yunsuan.org
'''

import datetime
import uuid
import random
import tornado
import markdown2
from docutils.core import publish_string
from bs4 import BeautifulSoup



def format_yr(indate):
    # uu = datetime.datetime.strptime(indate,'%a, %d %b %Y %H:%M:%S')
    return indate.strftime('%m-%d')

def format_date(indate):
    return indate.strftime('%Y-%m-%d %H:%M:%S')
def get_uuid():
    return(str(uuid.uuid1()))

def get_uu4d():
    sel_arr = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    slice = random.sample(sel_arr, 4)
    return( ''.join(slice))
def gen_pager(cat_slug, page_num, current):
    # cat_slug 分类
    # page_num 页面总数
    # current 当前页面
    if page_num == 1:
        return ''


    pager_shouye = '''
    <li class="first {0}">
    <a href="/category/{1}">&lt;&lt; 首页</a>
                </li>'''.format( 'hidden' if current <= 1 else '', cat_slug)

    pager_pre = '''
                <li class="previous {0}"><a href="/category/{1}/{2}">&lt; 前页</a>
                </li>
                '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
    pager_mid = ''
    for ind in range(0, page_num):
        tmp_mid = '''
                <li class="page {0}"><a href="/category/{1}/{2}">{2}</a></li>
                '''.format('selected' if ind+1 == current else '', cat_slug, ind + 1)
        pager_mid += tmp_mid
    pager_next = '''
                <li class="next {0}"><a href="/category/{1}/{2}">后页 &gt;</a>
                </li>
                '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
    pager_last = '''
                <li class="last {0}"><a href="/category/{1}/{2}">末页
                    &gt;&gt;</a>
                </li>
                '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
    pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
    return(pager)


def markdown2html( markdown_text):
    html = markdown2.markdown(markdown_text, extras=["wiki-tables"])
    return tornado.escape.xhtml_escape(html)

def rst2html(rst_text):
    html = publish_string(
        source=rst_text,
        writer_name='html',
    )
    soup = BeautifulSoup(html)
    id1_cnt = soup.find(id='id1')
    return tornado.escape.xhtml_escape(str(id1_cnt))









