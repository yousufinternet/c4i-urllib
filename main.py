import ssl
import email
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import getpass
import argparse
import urllib.parse, urllib.request

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.230 Safari/537.36"
SMTP_SERVER = 'smtp.gmail.com'
PORT = 587


# example wikipedia search url
# https://en.wikipedia.org/w/index.php?search=linux+foundation&title=Special%3ASearch&go=Go&ns0=1
def wikipedia_search(search_term):
    params = {'search': search_term, 'title': 'Special',
              'go': 'Go', 'ns0': '1'}
    query_str = urllib.parse.urlencode(params)
    full_url = urllib.parse.urljoin('https://www.wikipedia.org/w/',
                                    'index.php?' + query_str)
    print('You can open this search URL in a browser:\n'+full_url)
    header = {}
    # we use a custom user agent just in case the page decides
    # to block bots in future
    header['User-Agent'] = USER_AGENT
    req = urllib.request.Request(full_url, headers=header)
    response = urllib.request.urlopen(req)
    print(response.code, response.headers)
    page = response.read()
    print(page.decode('utf-8')[:500])
    return response.headers, page


def format_email(frm, to, search_term, headers, page):
    message = MIMEMultipart()
    message['Subject'] = f'"{search_term}" results in wikipedia'
    message['From'] = frm
    message['To'] = to

    body = ("Attached is the html of the results, "
            "below are the headers of the search results page:\n" +
            str(headers))

    # Adding an attachment to the message
    message.attach(MIMEText(body, "plain"))
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(page)
    email.encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {'_'.join(search_term.split())+'.html'}")
    message.attach(attachment)
    text = message.as_string()
    return text


def send_to_email(frm, to, search_term, headers, page):
    message = format_email(**locals())
    password = getpass.getpass(
        f'Please enter your ({frm}) email password and press enter:\n')
    try:
        context = ssl.create_default_context()
        smtp_server = smtplib.SMTP(SMTP_SERVER, PORT)
        smtp_server.ehlo()
        smtp_server.starttls(context=context)
        smtp_server.ehlo()
        smtp_server.login(frm, password)
        smtp_server.sendmail(frm, to, message)
    except Exception as e:
        print(f'The following error occured while trying to login:\n{e}')
    finally:
        smtp_server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=("Simple script to send the results of a"
                     " wikipedia search to an email"))
    parser.add_argument('-s', '--search-term', required=True)
    parser.add_argument('-e', '--email', required=True)
    parser.add_argument('-f', '--from-email',
                        default='yousufinternet@gmail.com')
    args = parser.parse_args()
    headers, page = wikipedia_search(args.search_term)
    send_to_email(args.from_email, args.email, args.search_term, headers, page)
