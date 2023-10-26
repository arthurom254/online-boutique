from django.contrib.sitemaps import Sitemap
from boutique.models import Item

class ItemSitemap(Sitemap):
    changefreq='daily'
    priority=0.5
    def items(self):
        return Item.objects.filter(outofstalk='False')