import json


class DataManager:
    def __init__(self):
        self.persons_json: dict = json.load(open('./persons.json', 'r', encoding='utf-8'))

    def get_cleansed_persons(self):
        persons = {}
        for person_isu in self.persons_json:
            person_json = self.persons_json[person_isu]['data']
            person = {}

            if 'bio' in person_json:
                for activity in (person_json['bio']['jobs'] or []) + (person_json['bio']['duties'] or []):
                    person['bio'] = (f"{person.get('bio', '')} {activity['position']['name']}"
                                     f" {activity['department']['name']}").strip()

                education = person_json['bio']['education']
                person['education'] = (f"{education['year']} {education['faculty']['name']} "
                                       f"{education['study']} "
                                       f"{education['program']['name'] if education['study'] == 'std' else ''}"
                                       ).strip() if education else ''

            for publication in (person_json['publications'] or []) + (person_json['rids'] or []):
                person['publications'] = (f"{person.get('publications', '')} {publication['type']} "
                                          f"{publication['title']} {publication['year']}").strip()

            for project in person_json['projects'] or []:
                person['publications'] = (f"{person.get('publications', '')} {project['type']} "
                                          f"{project['title']} {' '.join(project['key_words'])} {project['role']} "
                                          f"{project['customer']} {project['date_start']} {project['date_end']}")

            for event in person_json['events'] or []:
                person['publications'] = (f"{person.get('publications', '')} {event['rank']} "
                                          f"{event['title']} {event['type']} {event['role']}"
                                          f" {event['year']} {event['date_start']} {event['date_end']}")
            persons[person_isu] = person
        return persons


if __name__ == '__main__':
    dw = DataManager()
    print(dw.get_cleansed_persons())
