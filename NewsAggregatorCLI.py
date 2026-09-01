import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import json
from datetime import datetime


# Database file
DB = "news.db"


# ---------------- CREATE DATABASE ----------------

def create_database():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            source TEXT,
            link TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- SCRAPE NEWS ----------------

def get_news(url, source, base_url):

    news = []

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find headings
        headings = soup.find_all(["h2", "h3"])

        for heading in headings:

            title = heading.get_text(
                " ",
                strip=True
            )

            if len(title) < 10:
                continue

            # Find link
            link_tag = heading.find("a")

            if link_tag:

                link = link_tag.get("href")

            else:

                link = ""

            # Convert relative URL
            if link and link.startswith("/"):

                link = base_url + link

            news.append({
                "title": title,
                "source": source,
                "link": link,
                "date": datetime.now().strftime("%Y-%m-%d")
            })

    except Exception as e:

        print("Error while fetching", source)
        print(e)

    return news


# ---------------- COLLECT NEWS ----------------

def collect_news():

    print("\nCollecting news...\n")

    all_news = []

    # BBC
    bbc_news = get_news(
        "https://www.bbc.com/news",
        "BBC",
        "https://www.bbc.com"
    )

    print("BBC:", len(bbc_news), "headings found")

    all_news += bbc_news


    
    unique_news = {}

    for item in all_news:

        unique_news[item["title"]] = item

    all_news = list(unique_news.values())


    # Save to database
    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    new_articles = 0

    for item in all_news:

        try:

            cursor.execute(
                """
                INSERT INTO news
                (title, source, link, date)
                VALUES (?, ?, ?, ?)
                """,
                (
                    item["title"],
                    item["source"],
                    item["link"],
                    item["date"]
                )
            )

            new_articles += 1

        except sqlite3.IntegrityError:

            # Article already exists
            pass


    conn.commit()
    conn.close()


    print("\nTotal unique articles:", len(all_news))
    print("New articles saved:", new_articles)


# ---------------- SHOW NEWS ----------------

def show_news():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, source, date, link
        FROM news
        ORDER BY id DESC
    """)

    news = cursor.fetchall()

    conn.close()


    if not news:

        print("\nNo news available.")

        return


    print("\n" + "=" * 70)
    print("                    NEWS")
    print("=" * 70)


    for title, source, date, link in news:

        print("\nTitle :", title)
        print("Source:", source)
        print("Date  :", date)
        print("Link  :", link)

        print("-" * 70)


# ---------------- SEARCH BY KEYWORD ----------------

def search_news():

    keyword = input(
        "\nEnter keyword: "
    )


    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title, source, date, link
        FROM news
        WHERE title LIKE ?
        """,
        ("%" + keyword + "%",)
    )

    results = cursor.fetchall()

    conn.close()


    if not results:

        print("\nNo matching news found.")

        return


    print(
        "\nFound",
        len(results),
        "matching articles."
    )


    for title, source, date, link in results:

        print("\nTitle :", title)
        print("Source:", source)
        print("Date  :", date)
        print("Link  :", link)

        print("-" * 60)


# ---------------- FILTER SOURCE ----------------

def filter_source():

    source = input(
        "\nEnter source (BBC / The Guardian): "
    )


    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title, source, date, link
        FROM news
        WHERE source LIKE ?
        """,
        ("%" + source + "%",)
    )

    results = cursor.fetchall()

    conn.close()


    if not results:

        print("\nNo news found.")

        return


    for title, source, date, link in results:

        print("\nTitle :", title)
        print("Source:", source)
        print("Date  :", date)
        print("Link  :", link)

        print("-" * 60)


# ---------------- FILTER DATE ----------------

def filter_date():

    date = input(
        "\nEnter date (YYYY-MM-DD): "
    )


    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title, source, date, link
        FROM news
        WHERE date = ?
        """,
        (date,)
    )

    results = cursor.fetchall()

    conn.close()


    if not results:

        print("\nNo news found for this date.")

        return


    for title, source, date, link in results:

        print("\nTitle :", title)
        print("Source:", source)
        print("Date  :", date)
        print("Link  :", link)

        print("-" * 60)


# ---------------- EXPORT NEWS ----------------

def export_news():

    conn = sqlite3.connect(DB)

    df = pd.read_sql_query(
        "SELECT * FROM news",
        conn
    )

    conn.close()


    if df.empty:

        print("\nNo news available to export.")

        return


    print("\n")
    print("1. JSON")
    print("2. CSV")
    print("3. Excel")


    choice = input(
        "\nChoose format: "
    )


    if choice == "1":

        with open(
            "news.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                df.to_dict(
                    orient="records"
                ),
                file,
                indent=4,
                ensure_ascii=False
            )


        print("\nNews saved as news.json")


    elif choice == "2":

        df.to_csv(
            "news.csv",
            index=False
        )


        print("\nNews saved as news.csv")


    elif choice == "3":

        df.to_excel(
            "news.xlsx",
            index=False
        )


        print("\nNews saved as news.xlsx")


    else:

        print("\nInvalid choice.")


# ---------------- MAIN MENU ----------------

def main():

    # Create database before doing anything
    create_database()


    while True:

        print("\n")
        print("=" * 40)
        print("          NEWS AGGREGATOR")
        print("=" * 40)

        print("1. Collect News")
        print("2. Show All News")
        print("3. Search by Keyword")
        print("4. Filter by Source")
        print("5. Filter by Date")
        print("6. Export News")
        print("7. Exit")


        choice = input(
            "\nEnter your choice: "
        )


        if choice == "1":

            collect_news()


        elif choice == "2":

            show_news()


        elif choice == "3":

            search_news()


        elif choice == "4":

            filter_source()


        elif choice == "5":

            filter_date()


        elif choice == "6":

            export_news()


        elif choice == "7":

            print(
                "\nThank you for using News Aggregator!"
            )

            break


        else:

            print(
                "\nInvalid choice. Try again."
            )


# ---------------- START PROGRAM ----------------

if __name__ == "__main__":

    main()