from google.cloud.firestore_v1 import DocumentReference
from firebase_admin import firestore
import firebase_admin


def config():
	if not firebase_admin._apps:
		cred = firebase_admin.credentials.Certificate('serviceAccountKey.json')
		firebase_admin.initialize_app(cred)

	#   initialize firestore instance
	db = firestore.client()
	collection = db.collection(u'numbers')

	return collection


def toDict(references: dict, category: str) -> dict:
	"""
	Helper function for get_roster()
	:param references:
	:param category: category of a number (mega or normal)
	:return: dictionary representation of the number's map in the document
	"""
	return references[category].get().to_dict()


def formatter(time: str) -> str:
	"""
	formats the date to MM-DD-YYYY
	:param time:
	:return:
	"""
	return time[:10]


def get_date(references: dict) -> str:
	"""

	:return:
	"""
	ld_dict = references['last_update']
	return ld_dict.get().to_dict()['timestamp']


def num_update(doc: DocumentReference | dict, value: str, D: bool) -> None:
	"""
	updates the count of the number accordingly.
	:param D:
	:param doc: firebase document reference of 'numbers' document
	:param value: number that is sought to be updated
	:return: None
	"""

	doc_dict = doc if D else doc.get().to_dict()
	if value in doc_dict:
		doc_dict[value] += 1
	else:
		doc_dict[value] = 1

	if not D:
		doc.update(doc_dict)


def nums_add(references: dict, val: str, D: bool) -> None:
	"""
	O(1)
	:param D:
	:param references:
	:param val:
	:return:
	"""
	num = int(val)
	if num % 2 == 0:
		if num >= 35:
			num_update(references['he'], val, D)
		else:
			num_update(references['le'], val, D)
	else:
		if num >= 35:
			num_update(references['ho'], val, D)
		else:
			num_update(references['lo'], val, D)
