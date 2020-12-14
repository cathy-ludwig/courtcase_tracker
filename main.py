import datetime
import psycopg2
import pytz
import requests
from bs4 import BeautifulSoup


def insert():
    url = 'https://www.nebraska.gov/courts/calendar/index.cgi'
    myobj = {
        'court': 'C',
        'countyC': 'Douglas',
        'countyD': '',
        'selectRadio': 'date',
        'searchField': '12/14/2020',
        'submitButton': 'Submit'
    }

    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))

    response = requests.post(url, data=myobj)
    content = str(response.content, "utf-8")
    # content = content.replace('\n', '')
    # content = content.replace('\b', '')
    #
    soup = BeautifulSoup(content, features="html.parser")
    table_rows = soup.find_all('tr')
    print(dir(table_rows))



    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    for table_row in table_rows[3:]:
        try:
            cname, date, time, hearing_type, caption, case_id = [c.get_text().strip() for c in table_row.find_all("td")]

            local = pytz.timezone("America/Chicago")
            localdatetime = datetime.datetime.strptime(f"{date}T{time}", "%m/%d/%YT%I:%M%p")
            local_dt = local.localize(localdatetime, is_dst=None)
            utc_dt = local_dt.isoformat(timespec="minutes")

            cursor.execute("INSERT INTO court_cases.court_case (person_id, court_date, hearing_type, case_id, caption) VALUES (%s, %s, %s, %s, %s)", ('1', date, hearing_type, case_id, caption))
        except Exception:
            continue

        # Preparing SQL queries to INSERT a record into the database.
        # cursor.execute('INSERT INTO court_cases.court_case(person_id, court_date, hearing_type, case_id, caption) VALUES (1, {cname}, {date} {time}, {hearing_type}, {case_id}, {caption})')

    conn.commit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    insert()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
