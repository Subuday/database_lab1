from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


if __name__ == '__main__':
    try:
        os.remove("task1.xml")
        os.remove("task2.xml")
        os.remove("task2.xhtml")
    except OSError:
        pass
        process = CrawlerProcess(get_project_settings())
        process.crawl('uahotels')
        process.crawl('zvetsad')
        process.start()
    while True:
        print("-" * 45)
        print("Choose 1 or 2")
        print("1")
        print("2")
        print("=: ", end='', flush=True)
        number = input()
        if number == "1":
            print("Task1")
            root = etree.parse("task1.xml")
            pages = root.xpath("//page")
            minImagePages = {}
            lastMinimal = 100
            for page in pages:
                url = page.xpath("@url")[0]
                count = page.xpath("count(fragment[@type='image'])")
                if count < lastMinimal:
                    lastMinimal = count
                    minImagePages = {url, count}

            print(minImagePages)
        elif number == "2":
            print("Task2")
            transform = etree.XSLT(etree.parse("task2.xsl"))
            result = transform(etree.parse("task2.xml"))
            result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")
            webbrowser.open('file://' + os.path.realpath("task2.xhtml"))
        else:
            break
