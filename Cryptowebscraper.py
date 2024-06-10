from playwright.sync_api import sync_playwright
import psycopg2
from psycopg2.extras import execute_values

def main():
    with sync_playwright() as p:
        ### scrape data
        browser = p.chromiuim.launch(headless=False)
        page= browser.new_page()
        page.goto('https://coinmarketcap.com/')
        
        # scrolling down
        for i in range(5):
            page.mouse,wheel(0, 2000)
            page.wait_for_timeout(1000)
        
        trs_xpath="//table[@class='h7vnx2-2 czTsgW cmc-table  ']/tbody/tr"
        trs_list = page.query_selector_all(trs_xpath)
        master_list=[]
        for tr in trs_list:
            coin_dict ={}

            tds = tr.query_selector_all('//td')

            coin_dict['id'] = tds[1].inner_text()
            coin_dict['Name'] = tds[2].query_selector("//p[@color='text']"), inner_text()
            coin_dict['Symbol'] = tds[3].query_selector("//p[@color='text3']"), inner_text()
            coin_dict['Price']=float(tds[3].inner_text().replace('$','').replace(',',''))
            coin_dict['Market_cap_usd']=int(tds[7].inner_text().replace('$','').replace(',',''))
            coin_dict['Volume_24h_usd']= int(tds[8].query_selector('//p[@color="text"]').inner_text().replace('$','').replace(',',''))

            master_list.append(coin_dict)

        
        # tuples
        list_of_tuples = [tuple(dic.values()) for dic in master_list]

        ### save data

        # connect to db
        pgconn = psycopg2.connect(
            host= 'localhost',
            database = 'test',
            user = 'win',
            password = ''
        )
        
        # create cursor
        pgcursor=pgconn.cursor()

        execute_values(pgcursor,
                       "INSERT INTO crypto (id, name, symbol, price_usd, market_cap_usd, volume_24h_usd) VALUES %s" ,
                       list_of_tuples)
        # commit 
        pgconn.commit()

        #close connection
        pgconn.close()



        browser.close()


if __name__=='__main__':
    main()
   