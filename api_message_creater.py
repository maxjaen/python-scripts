import requests, json, smtplib
from email.mime.text import MIMEText
from email.header    import Header

#####################################
# PLEASE FILL IN THE FOLLOWING INFORMATION
TOKEN = ''
CHAT_ID = 0
SMTP_HOST = 'mail.gmx.net'
USER_MAIL_ADDRESS = ''
USER_PASSWORD = ''
RECIPIENTS_EMAILS = [USER_MAIL_ADDRESS]
#####################################

class ApiRequest:
    DOGS = 1
    AFFIRMATION = 2
    DADJOKE = 3

def request_api(api_url):
    """
    Return the content for the requested url.
    """
    r = requests.get(api_url)
    r.raise_for_status()
    return json.loads(r.content)

def retrieve_dog_picture_data():
    """
    Return dog pictures url as data from 'thedogapi.com'.
    """
    json_object = request_api("https://api.thedogapi.com/v1/images/search")
    # more information about the dog available in json object
    return json_object[0]["url"]

def retrieve_affirmation_data():
    """
    Return affirmation json as data from 'affirmations.dev'.
    """
    json_object = request_api("https://www.affirmations.dev/")
    return json_object["affirmation"]

def retrieve_dadjoke_data():
    """
    Return attachments json as data from 'icanhazdadjoke.com'.
    """
    json_object = request_api("https://icanhazdadjoke.com/slack")
    return json_object["attachments"][0]["text"]

# will not be used in the future, only used for bot setup to get the chat id 
def get_chat_id(token):
    """
    Request telegram chat id with the specified token.
    """
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    print(requests.post(url).json())

def send_data_via_telegram(chat_id, token, msg):
    """
    Send a message to the specified telegram chat with a authorization token.
    https://medium.com/@wk0/send-and-receive-messages-with-the-telegram-api-17de9102ab78
    """
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': {chat_id}, 'text': msg}
    requests.post(url, data).json()

def send_data_via_email(user_mail_address, user_password, recipients_emails, mail_body):
    """
    Send message to email address with authorization parameters for your email provider.
    """
    msg = MIMEText(mail_body, 'plain', 'utf-8')
    msg['Subject'] = Header('Neue Nachricht', 'utf-8')
    msg['From'] = user_mail_address
    msg['To'] = ", ".join(recipients_emails)

    connection = smtplib.SMTP(SMTP_HOST, 587, timeout=10)
    connection.set_debuglevel(1)
    try:
        connection.starttls()
        connection.login(user_mail_address, user_password)
        connection.sendmail(msg['From'], recipients_emails, msg.as_string())
    finally:
        connection.quit()

def retrieve_data_from_api(api_request):
    """
    Choose api request based on the input.
    """
    if (api_request == ApiRequest.DOGS):
        return retrieve_dog_picture_data()
    elif (api_request == ApiRequest.AFFIRMATION):
        return retrieve_affirmation_data()
    elif (api_request == ApiRequest.DADJOKE):
        return retrieve_dadjoke_data()
    raise NotImplementedError()

if __name__ == "__main__":  
    data = retrieve_data_from_api(ApiRequest.DOGS)

    send_data_via_telegram(CHAT_ID, TOKEN, data)
    # send_data_via_email(USER_MAIL_ADDRESS, USER_PASSWORD, RECIPIENTS_EMAILS, msg)
