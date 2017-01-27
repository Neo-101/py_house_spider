from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.shell import inspect_response
import scrapy
from sf_house_spider.items import URLItem
from sf_house_spider.items import CommunityItem

class CommunitySpider(scrapy.Spider):
    name = 'community_spider'
    # 限制爬取的域名范围
    # allowed_domains = ['esf.nanjing.fang.com']
    base_url = 'http://esf.nanjing.fang.com/housing/'
    # community = [u'鼓楼', u'江宁', u'浦口', u'玄武', u'建邺', u'栖霞', u'雨花',
    #              u'秦淮', u'六合', u'溧水', u'高淳', u'南京周边']
    community = [u'鼓楼', u'江宁']
    community_code = {u'鼓楼': '265', u'江宁': '268', u'浦口': '270', u'玄武': '264',
                      u'建邺': '267', u'栖霞': '271', u'雨花': '272', u'秦淮': '263',
                      u'六合': '269', u'溧水': '274', u'高淳': '275', u'南京周边': '13046'}
    community_url_num = {u'鼓楼': 0, u'江宁': 0, u'浦口': 0, u'玄武': 0, u'建邺': 0, u'栖霞': 0,
                         u'雨花': 0, u'秦淮': 0, u'六合': 0, u'溧水': 0, u'高淳': 0, u'南京周边': 0}


    def start_requests(self):
        for one_community in self.community:
            code = self.community_code[one_community]
            region_url = self.base_url + code + '__0_0_0_0_1_0_0/'
            yield Request(region_url, callback=self.parse, meta={'region': one_community})

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        # 获得每个区域的小区列表的页数
        page_str = soup.find('span', attrs={'class': 'fy_text'}).get_text()
        max_page = int(page_str[(page_str.find('/')+1):])
        for i in range(1, 3):
        # for i in range(1, max_page+1):
            region_page_url = str(response.url).replace('1_0_0', str(i)+'_0_0')
            yield Request(region_page_url, callback=self.get_community_url,
                          meta={'region': response.meta['region']})

    def get_community_url(self, response):
        # lxml不能正确解析页面,采用html5lib作为解码器
        soup = BeautifulSoup(response.body, 'html5lib')
        community_list = soup.find_all(attrs={'class': 'list rel'})
        for community_item in community_list:
            community_url = community_item.find('a', attrs={'class': 'plotTit'})['href']
            community_type = community_item.find('span', attrs={'class': 'plotFangType'}).get_text()
            if community_url.find('http://') != -1:
                if community_type == u'住宅' or community_type == u'别墅':

                    # Get priceAverage and ratio
                    meta_request = {'region': response.meta['region']}
                    price_tag = community_item.find('p', attrs={'class': 'priceAverage'})
                    ratio_tag = community_item.find('p', attrs={'class': 'ratio'})
                    if price_tag is None:
                        meta_request['priceAverage'] = 0
                        meta_request['ratio'] = 0.00
                    else:
                        meta_request['priceAverage'] = int(price_tag.find('span').get_text())
                        if ratio_tag is None:
                            meta_request['ratio'] = 0.00
                        else:
                            ratio_tag =ratio_tag.find('span')
                            class_list = ratio_tag['class']
                            if class_list.count('red') == 1:
                                meta_request['ratio'] = float((ratio_tag.get_text())[1:-1])
                            elif class_list.count('green') == 1:
                                meta_request['ratio'] = -1*float((ratio_tag.get_text())[1:-1])
                    # 得到详情页的地址,根据是否是别墅采取不同的地址编址方式
                    if community_url.find('/villa/') == -1:
                        community_url = community_url[:community_url.find('.com')] +'.com/xiangqing/'
                    else:
                        community_url = community_url[:community_url.find('/villa/')] +'/villa/xiangqing/'
                    # print(community_url)
                    yield Request(community_url, callback=self.get_community_info, meta=meta_request)
                elif community_type == u'商铺' or community_type == u'写字楼':
                    pass

    def get_community_info(self, response):
        inspect_response(response, self)
        info = CommunityItem()
        soup = BeautifulSoup(response.body, 'lxml')
        info['name'] = soup.find('a', attrs={'class': 'tt'}).get_text()
        info['region'] = response.meta['region']
        info['page_url'] = response.url
        info['price_cur'] = response.meta['priceAverage']
        info['ratio_month'] = response.meta['ratio']
        box_list = soup.find_all('div', attrs={'class': 'box'})
        for box in box_list:
            box_title = ''
            if box.find('h3') == None:
                continue
            else:
               box_title = box.find('h3').get_text()
            if box_title == '基本信息':
                info_dict = self.get_info_dict(box)
                info['address'] = info_dict.get('小区地址', 'null')
                info['character'] = info_dict.get('项目特色', 'null')
                info['property'] = info_dict.get('产权描述', 'null')
                info['manage_type'] = info_dict.get('物业类别', 'null')
                info['done_time'] = info_dict.get('竣工时间', 'null')
                info['build_company'] = info_dict.get('开发商', 'null')
                info['building_type'] = info_dict.get('建筑类别', 'null')
                info['building_area'] = info_dict.get('建筑面积', 'null')
                info['cover_area'] = info_dict.get('占地面积', 'null')
                info['house_num_cur'] = info_dict.get('当前户数', 'null')
                info['house_num_sum'] = info_dict.get('总户数', 'null')
                info['green_rate'] = info_dict.get('绿化率', 'null')
                info['volum_rate'] = info_dict.get('容积率', 'null')
                info['manage_price'] = info_dict.get('物业费', 'null')
                info['info_add'] = info_dict.get('附加信息', 'null')
                pass
            elif box_title == '配套设施':
                info_dict = self.get_info_dict(box)
                info['water_price'] = info_dict.get('供水', 'null')
                info['electric_price'] = info_dict.get('供电', 'null')
                info['gas_price'] = info_dict.get('燃气', 'null')
                info['network'] = info_dict.get('通讯设备', 'null')
                info['elector'] = info_dict.get('电梯服务', 'null')
                info['security'] = info_dict.get('安全管理', 'null')
                info['sanitation'] = info_dict.get('卫生服务', 'null')
                info['parking'] = info_dict.get('停车位', 'null')
                pass
            elif box_title == '交通状况':
                info_dict = self.get_info_dict(box)
                info['metro'] = info_dict.get('地铁', 'null')
                info['bus'] = info_dict.get('公交', 'null')
                info['car'] = info_dict.get('自驾', 'null')
                pass
            elif box_title == '周边信息':
                info_dict = self.get_info_dict(box)
                info['kindergarten'] = info_dict.get('幼儿园', 'null')
                info['school'] = info_dict.get('中小学', 'null')
                info['university'] = info_dict.get('大学', 'null')
                info['shop_mall'] = info_dict.get('商场', 'null')
                info['hospital'] = info_dict.get('医院', 'null')
                info['post_office'] = info_dict.get('邮局', 'null')
                info['bank'] = info_dict.get('银行', 'null')
                info['other_facility'] = info_dict.get('其他', 'null')
                pass
            else:
                continue
        yield info

    def get_info_dict(self, box):
        dd_list = box.find('dl').find_all('dd')
        result_dict = {}
        for dd in dd_list:
            # 去掉字符串中的空格
            text = ''.join((dd.get_text()).split())
            if text.find('...') == -1:
                result_dict[text[:text.find('：')]] = text[text.find('：')+1:]
            else:
                result_dict[text[:text.find('：')]] = dd['title']
        return result_dict