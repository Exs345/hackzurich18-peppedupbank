#!/usr/bin/env python3

import sys
import argparse

try:
	import cognitive_face as CF
except ImportError:
	 sys.stderr.write("Couldn't import cognitive_face. Try running 'pip install cognitive_face'\n")

try:
	import config
except ImportError:
	 sys.stderr.write("Couldn't import config. Please create a config.py'\n")


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('--name')
	parser.add_argument('--image')
	parser.add_argument('action', nargs=1)
	return parser.parse_args()

def list_persons():
	persons = CF.large_person_group_person.list(config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID)
	for person in persons:
		print(person)

def delete_person(name):
	personId = get_person_id(name)
	if personId == None:
		print('Person is not existent.')
		return

	CF.large_person_group_person.delete(config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID, personId)

def get_person_id(name):
	# Get all persons
	persons = CF.large_person_group_person.list(config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID)
	for person in persons:
		if person['name'] == name:
			return person['personId']

	return None

def create_person(name):
	personId = get_person_id(name)
	if personId != None:
		print('Person already exists!')
		return

	CF.large_person_group_person.create(config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID, name)

def update_person(name, image):
	personId = get_person_id(name)
	if personId == None:
		print('Person is not existent.')
		return

	CF.large_person_group_person_face.add(image, config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID, personId)

	# train model
	CF.large_person_group.train(config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID)

def get_person(personId):
	return CF.large_person_group_person.get(config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID, personId)


def identify_person(image):
	res = []

	faces = CF.face.detect('IMG_6909.jpg')
	faces = CF.face.identify([face['faceId'] for face in faces], large_person_group_id=config.COGNITIVE_FACE_LARGE_PERSON_GROUP_ID)

	for face in faces:
		for candidate in face['candidates']:
			#print(candidate)
			candidate.update(get_person(candidate['personId']))

	return faces

def most_likely_person(faces):
	if len(faces) > 0:
		if 'candidates' in faces[0]:
			if len(faces[0]['candidates']) > 0:
				return faces[0]['candidates'][0]['name']

	return None

def main():
	args = parse_arguments()

	CF.Key.set(config.COGNITIVE_FACE_KEY)
	CF.BaseUrl.set(config.COGNITIVE_FACE_BASE_URL)

	if (args.action[0] == 'create'):
		create_person(args.name)
	elif (args.action[0] == 'list'):
		list_persons()
	elif (args.action[0] == 'delete'):
		delete_person(args.name)
	elif (args.action[0] == 'update'):
		update_person(args.name, args.image)
	elif (args.action[0] == 'identify'):
		print(most_likely_person(identify_person(args.image)))
	else:
		print('Unknown action: {}'.format(args.action[0]))

if __name__ == "__main__":
    main()


