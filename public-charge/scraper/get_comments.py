from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from math import ceil
from xvfbwrapper import Xvfb
from scraper import Scraper
import sys

Base = declarative_base()

results_per_page = 50
comment_delay = 1

class Comment(Base):
    __tablename__ = "comments"

    uscisid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    date_posted = Column(String, nullable=False)
    date_received = Column(String, nullable=False)
    traking_number = Column(String, nullable=False)
    rin = Column(String, nullable=False)
    phase = Column(String, nullable=False)

if __name__ == "__main__":

    page_start = 1
    if len(sys.argv) > 1:
        page_start = int(sys.argv[1])

    print("Initializing ...")

    engine = create_engine('sqlite:///comments.sqlite')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance.
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Start virtual display.
    vdisplay = Xvfb()
    vdisplay.start()

    # Start scraper.
    scraper = Scraper(delay=comment_delay, results_per_page=results_per_page)

    print("Scraping ...")

    try:
        # Get the total number of comments.
        total_comments = scraper.get_comments_total()
        print("Total comments: {}".format(total_comments))
        total_pages = ceil(total_comments / results_per_page)
        print("Total pages: {}".format(total_pages))

        # Go through all pages.
        for page in range(page_start, total_pages + 1):
            # Get comment urls on given page.
            urls = scraper.get_comments_urls_on_page(page)
            print("Page {}: Urls: {}".format(page, len(urls)))

            for i, url in enumerate(urls):
                # USCIS ID.
                uscisid = url.split("=")[-1]

                comment_number = (page - 1)*results_per_page + i

                # Check if entry exists.
                exists = session.query(Comment).filter(
                    Comment.uscisid == uscisid).first()
                if exists is None:
                    print("GET {}".format(url))
                    c = scraper.scrape_comment(comment_url=url)

                    if c is None:
                        print("# Bad comment")
                    else:
                        try:
                            comment = Comment(
                                uscisid=uscisid,
                                name=c["name"],
                                comment=c["comment"],
                                date_posted=c["posted_date"],
                                date_received=c["received_date"],
                                traking_number=c["tracking_number"],
                                rin=c["rin"],
                                phase="A")
                            session.add(comment)
                            session.commit()
                            print("> ", comment_number, uscisid)
                        except IntegrityError:  # Do not commit repeated comments.
                            session.rollback()
    finally:
        scraper.shut_down()

        # Stop xvfb
        vdisplay.stop()
