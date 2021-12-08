import funcs # import our functions
import os # filesystem and environment variables
import datetime # system time for record keeping

import smtplib # sending and formatting email    - | 
from email.mime.multipart import MIMEMultipart # - |
from email.mime.text import MIMEText #  -  -  -  - |

from dotenv import load_dotenv # load environment variables  - |
load_dotenv() #   -   -   -   -   -   -   -   -   -   -   -  - |


def main():
    now = datetime.datetime.now()
    content = ""

    cnt = funcs.extract_news(input("Enter URL: ") or os.environ["DEFAULT_NEWS_URL"])
    content += cnt
    content += ("<br>------<br>")
    content += ("<br><br>End of Message")

    """
    send the email
    """
    msg = MIMEMultipart()
    msg["Subject"] = f"Top News Stories [Automated Email] {str(now.month)}-{str(now.day)}-{str(now.year)}"
    msg["From"] = os.environ["FROM"]
    msg["To"] = os.environ["TO"]

    msg.attach(MIMEText(content, "html"))

    print("Initializing Server...")

    server = smtplib.SMTP(os.environ["MAIL_SERVER"], os.environ["MAIL_PORT"])
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(os.environ["FROM"], os.environ["MAIL_PW"])
    server.sendmail(os.environ["FROM"], os.environ["TO"], msg.as_string())

    print("Email Sent...")

    server.quit()

    """
    get text from target url
    """
    text = funcs.get_only_text( \
        input("Enter URL: ") or \
        os.environ["DEFAULT_TARGET_URL"]) # use default url from env variables if no input

    """
    display link text and text length
    """ 
    print(len(text)) # length of tuple
    print(len(str.split(text[1]))) # number of words in link text, aside from title
    print(text) # full text of link

    """
    summarize text
    """
    txt_summ = funcs.summ(text) # call summarizer
    print(txt_summ) # view output

    """
    produce keywords from summary
    """
    k_words = funcs.get_keyword_lemmas(text) # get lemmatized keywords
    print(k_words) # view output


if __name__ == "__main__":
    main()
