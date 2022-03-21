from urllib.parse import parse_qs
"""
Twilio response example:
{
    "AccountSid": ["..."],
    "ApiVersion": ["2010-04-01"],
    "Body": ["Hey"],
    "From": ["whatsapp:+5491122520361"],
    "MessageSid": ["..."],
    "NumMedia": ["0"],
    "NumSegments": ["1"],
    "ProfileName": ["Alberto Rincones"],
    "SmsMessageSid": ["..."],
    "SmsSid": ["..."],
    "SmsStatus": ["received"],
    "To": ["whatsapp:+14155238886"],
    "WaId": ["5491122520361"]
}
"""

def _parse_twilio_message(raw_body):
    return parse_qs(raw_body.decode('utf-8'))


def get_twilio_message(raw_body):
    body = _parse_twilio_message(raw_body)
    message = {
        "MessageSid": body.get("MessageSid")[0],
        "Sender": {
            "Name": body.get("ProfileName")[0],
            "Number": body.get("From")[0]
        },
        "Receiver": body.get("To")[0],
        "Body": body.get("Body")[0],
        "Status": body.get("SmsStatus")
    }
    return message

