# -*- coding:utf-8 -*-

'''
权限
0: 读
1: 加
2: 改
3: 删
4: 管理
其他根据需要可在后面添加
'''
mask  = '11111'
__author__ = 'bukun'

from torlite.modules.menu import ModuleCatMenu
from torlite.modules.menu import ModuleSpecMenu
from torlite.modules.menu import TopMenu
from torlite.modules.core_modules import *
# from modules.extends import most_use

page_num = 10

core_modules = {'ModuleCatMenu': ModuleCatMenu,
                'ModuleSpecMenu': ModuleSpecMenu,
                'get_footer': get_footer,
                'previous_post_link': previous_post_link,
                'next_post_link': next_post_link,
                'the_category': the_category,
                'list_categories': list_categories,
                'topmenu': TopMenu,
                'post_most_view': post_most_view,
                'post_random': post_random,
                'post_recent': post_recent,
                'post_recent_most_view': post_recent_most_view,
                'post_cat_random': post_cat_random,
                'post_cat_recent': post_category_recent,
                'generate_abstract': generate_abstract,
                'category_menu': category_menu,
                'post_catalogs': post_catalogs,
                # 'most_use':most_use,
                }
