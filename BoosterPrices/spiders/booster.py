# -*- coding: utf-8 -*-
import scrapy
import csv


class BoosterSpider(scrapy.Spider):
    name = "booster"
    allowed_domains = ["steamcardexchange.net"]
    start_urls = (
        'http://www.steamcardexchange.net/index.php?boosterprices',
    )

    def parse(self, response):
        total_price = 0
        total_count = 0
        with open('boosterPriceList.csv', 'w') as csvfile:  # 存成csv
            fieldnames = ['name', 'number', 'link', 'pack_price', 'card_price', 'card_trend_price', 'each_card',
                          'three_cards_price',
                          'order_price', 'ntdw_order_price']  # 設定標題
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # 寫入標題

            for cell in response.xpath('//*[@id="boosterpricelist"]/tbody/tr'):  # 抓取每一個cell
                name = cell.xpath('td[1]/a/text()').extract()[0].encode('utf-8')
                number = cell.xpath('td[1]/a/@href').re('\d+')[0].encode('utf-8')
                link = 'http://steamcommunity.com/market/listings/753/%s-%s Booster Pack' % (number, name)

                link = self.exception_handler(number, link)  # 例外處理

                pack_price = cell.xpath('td[2]/text()').re('(\d*\.\d+)')[0].encode('utf-8')
                card_price = cell.xpath('td[3]/text()').re('(\d*\.\d+)')[0].encode('utf-8')

                if not cell.xpath('td[3]/span/text()'):  # 價格走勢 0%
                    card_trend_price = int(0)
                else:
                    card_trend_price = cell.xpath('td[3]/span/text()').re('[+-]?\d+')[0].encode('utf-8')  # 價格走勢
                    card_trend_price = int(card_trend_price)

                each_card = (float(card_price) / 3) * 0.86958  # 每張卡可賣的價格
                three_cards_price = each_card * 3  # 三張卡的價格
                order_price = three_cards_price * 0.4  # 購買價格 成本4成 利潤6成
                ntdw_order_price = order_price * 30  # 台幣價格
                # print name
                # print number
                # print link
                # print pack_price
                # print card_price
                # print int(card_trend_price)
                # print each_card
                # print three_cards_price
                # print order_price
                # print ntdw_order_price

                if 15 > ntdw_order_price:  # 價格低於15台幣的才要
                    if ntdw_order_price > 3:  # 小於3台幣的也不要：卡賣不出去
                        if card_trend_price > -100:  # 走跌超過100％的不要：不隱定
                            total_price += ntdw_order_price  # 累計總價
                            total_count += 1  # 總數
                            writer.writerow(
                                {'name': name, 'number': number, 'link': link, 'pack_price': pack_price,
                                 'card_price': card_price, 'card_trend_price': card_trend_price,
                                 'each_card': "{0:.2f}".format(each_card),
                                 'three_cards_price': "{0:.2f}".format(three_cards_price),
                                 'order_price': "{0:.2f}".format(order_price),
                                 'ntdw_order_price': "{0:.2f}".format(ntdw_order_price)})

        print '總價 =', total_price
        print '總數 =', total_count

    # 例外處理  (如果字串裡有% 必須寫成%%)
    def exception_handler(self, number, link):
        if number == '370270':
            link = 'http://steamcommunity.com/market/listings/753/%s-Jim Power -The Lost Dimension  Booster Pack' % (
            number)
        if number == '423610':
            link = 'http://steamcommunity.com/market/listings/753/%s-Where\'s My Mommy%%3F Booster Pack' % (
                number)
        if number == '221040':
            link = 'http://steamcommunity.com/market/listings/753/%s-Resident Evil 6 - Biohazard 6 Booster Pack' % (
                number)
        if number == '285500':
            link = 'http://steamcommunity.com/market/listings/753/%s-Hard Truck Apocalypse - Ex Machina Booster Pack' % (
                number)
        if number == '254700':
            link = 'http://steamcommunity.com/market/listings/753/%s-resident evil 4 - biohazard 4 Booster Pack' % (
                number)
        if number == '432020':
            link = 'http://steamcommunity.com/market/listings/753/%s-What\'s under your blanket !%%3F Booster Pack' % (
                number)
        if number == '285520':
            link = 'http://steamcommunity.com/market/listings/753/%s-Sledgehammer - Gear Grinder Booster Pack' % (
                number)
        if number == '297860':
            link = 'http://steamcommunity.com/market/listings/753/%s-Split-Second Booster Pack' % (
                number)
        if number == '211500':
            link = 'http://steamcommunity.com/market/listings/753/%s-RaceRoom Racing Experience  Booster Pack' % (
                number)
        if number == '359870':
            link = 'http://steamcommunity.com/market/listings/753/%s-FINAL FANTASY X-X-2 HD Remaster Booster Pack' % (
                number)
        if number == '495010':
            link = 'http://steamcommunity.com/market/listings/753/%s-丛林守望者（Ranger of the jungle） Booster Pack' % (
                number)
        if number == '304240':
            link = 'http://steamcommunity.com/market/listings/753/%s-Resident Evil - biohazard HD REMASTER Booster Pack' % (
                number)
        if number == '417990':
            link = 'http://steamcommunity.com/market/listings/753/%s-Major-Minor Booster Pack' % (
                number)
        if number == '390340':
            link = 'http://steamcommunity.com/market/listings/753/%s-Umbrella Corps™ - Biohazard Umbrella Corps™ Booster Pack' % (
                number)
        if number == '417110':
            link = 'http://steamcommunity.com/market/listings/753/%s-Mayjasmine episode01 What is God%%3F 五月茉莉 Booster Pack' % (
                number)
        if number == '392000':
            link = 'http://steamcommunity.com/market/listings/753/%s-TRON RUN-r Booster Pack' % (
                number)
        if number == '387870':
            link = 'http://steamcommunity.com/market/listings/753/%s-Mold on Pizza 🍕 Booster Pack' % (
                number)
        if number == '384840':
            print 'can\'t find link'
        if number == '317110':
            link = 'http://steamcommunity.com/market/listings/753/%s-Uncharted Waters Online%%3A Gran Atlas Booster Pack' % (
                number)
        if number == '337680':
            link = 'http://steamcommunity.com/market/listings/753/%s-Star Hammer%%3A The Vanguard Prophecy  Booster Pack' % (
                number)
        if number == '321960':
            link = 'http://steamcommunity.com/market/listings/753/%s-Might %%26 Magic Heroes VII  Booster Pack' % (
                number)
        if number == '282800':
            link = 'http://steamcommunity.com/market/listings/753/%s-100%%25 Orange Juice Booster Pack' % (
                number)
        if number == '368640':
            link = 'http://steamcommunity.com/market/listings/753/%s-htoL%%23NiQ%%3A The Firefly Diary Booster Pack' % (
                number)
        if number == '260230':
            link = 'http://steamcommunity.com/market/listings/753/%s-Valiant Hearts%%3A The Great War™ - Soldats Inconnus %%3A Mémoires de la Grande Guerre™ Booster Pack' % (
                number)
        if number == '335190':
            link = 'http://steamcommunity.com/market/listings/753/%s-200%%25 Mixed Juice! Booster Pack' % (
                number)

        return link
