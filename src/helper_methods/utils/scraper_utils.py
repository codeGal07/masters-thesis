def get_title_and_text(scraper_instance):
    title = scraper_instance.get_article_title()
    content = scraper_instance.get_article_text()
    return title, content


def process_opening(self):
    self.click_accept()
