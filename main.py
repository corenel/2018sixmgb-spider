from bs4 import BeautifulSoup
import requests
import pdfkit
import os


def to_pdf(url, outfile='out.pdf'):
    """Save webpage as pdf file."""
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'no-outline': None,
        'no-pdf-compression': None,
        'disable-smart-shrinking': None,
        'quiet': None,
        'zoom': 4.5
    }
    pdfkit.from_url(url, outfile, options=options)


def parse_page(page, base_url):
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find_all('h3', id='page_title', limit=1)[0].string
    elements = soup.find_all('a')
    links = {e.text: get_abs_url(base_url, e.attrs['href']) for e in elements}
    return title, links


def get_html(url):
    page = requests.get(url)
    return page if page.status_code == 200 else None


def get_prefix(url):
    return os.path.dirname(url)


def get_abs_url(base_url, rel_url):
    return os.path.join(base_url, rel_url)


def main():
    urls = [
        'http://www.nosta.gov.cn/upload/2018slxmgb/zr_107/zrIndex.html',
        'http://www.nosta.gov.cn/upload/2018slxmgb/fm_309/fmIndex.html',
        'http://www.nosta.gov.cn/upload/2018slxmgb/jb_220/jbIndex.html'
    ]
    for url in urls:
        print('Processing {}'.format(url))

        page = get_html(url)
        if page is None:
            continue

        base_url = get_prefix(url)
        page_title, links = parse_page(page, base_url)

        os.makedirs(page_title)
        for link_title, link_url in links.items():
            print('-> Saving {}'.format(link_title))
            out_path = os.path.join(page_title, '{}.pdf'.format(link_title))
            if not os.path.exists(out_path):
                to_pdf(link_url, out_path)


if __name__ == '__main__':
    main()
