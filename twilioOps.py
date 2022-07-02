from twilio.rest import Client
import info as info


def notif(Message: str) -> None:
	# Account SID from twilio.com/console
	acc_sid = info.account_sid
	# Auth Token from twilio.com/console
	auth_tok = info.auth_token

	client = Client(acc_sid, auth_tok)

	message = client.messages.create(
		to=info.to,
		from_=info.from_,
		body=Message)
