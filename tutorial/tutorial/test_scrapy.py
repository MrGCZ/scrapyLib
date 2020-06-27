import scrapy


class Person(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()


class A:
    b = 1

    def test1(self):
        print("test1")


person = Person()
print(123)

