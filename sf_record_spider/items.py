import scrapy
class SellItem(scrapy.Item):
    community_id = scrapy.Field()
    code = scrapy.Field()
    release_time = scrapy.Field()
    price_all = scrapy.Field()
    price_per = scrapy.Field()
    first_pay = scrapy.Field()
    month_pay = scrapy.Field()
    floor = scrapy.Field()
    area_build = scrapy.Field()
    direction = scrapy.Field()
    decoration = scrapy.Field()
    house_model = scrapy.Field()
    build_time = scrapy.Field()
    house_structure = scrapy.Field()
    house_type = scrapy.Field()
    property_type = scrapy.Field()
    page_url = scrapy.Field()
    building_type = scrapy.Field()

class RentItem(scrapy.Item):
    community_id = scrapy.Field()
    code = scrapy.Field()
    update_time = scrapy.Field()
    price = scrapy.Field()
    rate = scrapy.Field()
    pay_type = scrapy.Field()
    house_type = scrapy.Field()
    house_model = scrapy.Field()
    area_build = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    decoration = scrapy.Field()
    support_bed = scrapy.Field()
    support_furniture = scrapy.Field()
    support_gas = scrapy.Field()
    support_warm = scrapy.Field()
    support_network = scrapy.Field()
    support_tv = scrapy.Field()
    support_condition = scrapy.Field()
    support_fridge = scrapy.Field()
    support_wash = scrapy.Field()
    support_water = scrapy.Field()
    page_url = scrapy.Field()
    rent_type = scrapy.Field()

class RecordSellItem(scrapy.Item):
    community_id = scrapy.Field()
    house_model = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    area_build = scrapy.Field()
    sell_time = scrapy.Field()
    price_all = scrapy.Field()
    price_per = scrapy.Field()

class RecordRentItem(scrapy.Item):
    community_id = scrapy.Field()
    house_model = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    area_build = scrapy.Field()
    sell_time = scrapy.Field()
    price = scrapy.Field()

