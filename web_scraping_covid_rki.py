import bs4, requests, schedule, time 

#####################################
# country you want to search for
SEARCHED_COUNTRY = 'Italien'
# api url for your telegram group
REQUEST_TELEGRAM_URL = ''
#####################################

REQUEST_RKI_URL = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html'
CSS_SELECTOR_COUNTRIES = 'div#wrapperOuter div#wrapperInner div#wrapperDivisions div#wrapperDivisions-2 div#wrapperContent div#content div#main div.text ul' 
CSS_SELECTOR_COUNTRIES_TITLE = f'{CSS_SELECTOR_COUNTRIES} li'
NEW_LINE = '\n'

def request_rki_site():
    """
    Returns parsed text data from requested rki website.
    """
    rki_page = requests.get(REQUEST_RKI_URL)
    rki_page.raise_for_status()
    return bs4.BeautifulSoup(rki_page.text, 'html.parser')

def format_resultset_to_array(resultset):
    """
    """
    array = []
    array.extend(
        (i.text for i in resultset))
    return array

def create_covid_message(searched_country):
    """
    Create console-displayable message for the searched country as string.
    """
    result_message = 'Für dieses Land gibt es Covid Warnhinweise.' + NEW_LINE
    result_message += 'Das Land oder min. eine Region wurde als Risikogebiet deklariert:' + NEW_LINE
    result_message += f'{searched_country}'[:-1].replace(')',')' + NEW_LINE)
    return result_message

def send_message_to_telegram(result_message):
    """
    Sends the specified message to the telegram api and prints the result message to console
    based on the status code of the request.
    """
    message = result_message + '\n' + REQUEST_RKI_URL
    request = requests.get(REQUEST_TELEGRAM_URL.format(f'{message}'))
    if request.status_code == 200:
       print(f'Message {result_message} sended!')
    else:
        print(f'Telegram API not reachable for message {result_message}')

if __name__ == "__main__":
    rki_text = request_rki_site()

    selected_countries = rki_text.select(CSS_SELECTOR_COUNTRIES_TITLE)
    countries = format_resultset_to_array(selected_countries)

    filtered_countries = list(filter(lambda country: SEARCHED_COUNTRY in country, countries))

    if len(filtered_countries) > 0:
        searched_country = filtered_countries[0]

        result_message = create_covid_message(searched_country)
        send_message_to_telegram(result_message)
    else:
        result_message = f'{SEARCHED_COUNTRY} ist kein Risikogebiet.'
        send_message_to_telegram(result_message)
