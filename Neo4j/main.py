import json
import neomodel
from typing import List
import time
from typing import TypedDict

neomodel.config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

class Person(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    member_profile = neomodel.StringProperty()
    name = neomodel.StringProperty()
    email = neomodel.StringProperty()
    phone = neomodel.StringProperty()
    url = neomodel.StringProperty()
    location = neomodel.StringProperty()
    headline = neomodel.StringProperty()
    summary = neomodel.StringProperty()
    is_open_to_work = neomodel.BooleanProperty()
    industry = neomodel.StringProperty()
    address = neomodel.StringProperty()
    twitter = neomodel.StringProperty()
    skills: list = neomodel.StringProperty()
    tag: list = neomodel.StringProperty()
    given_recommendations = neomodel.StringProperty()
    received_recommendations = neomodel.StringProperty()
    sent_by = neomodel.StringProperty()
    connections_count = neomodel.StringProperty()
    followers_count = neomodel.StringProperty()
    updated_at = neomodel.StringProperty()

    instant_message_service = neomodel.RelationshipTo(
        'InstantMessageService', 'INSTANT_MESSAGE_SERVICE')
    attachments = neomodel.RelationshipTo('Attachment', 'ATTACHMENT')
    websites = neomodel.RelationshipTo('Website', 'WEBSITE')
    educations = neomodel.RelationshipTo('Education', 'EDUCATION')
    experiences = neomodel.RelationshipTo('Experience', 'EXPERIENCE')
    certifications = neomodel.RelationshipTo('Certification', 'CERTIFICATE')
    courses = neomodel.RelationshipTo('Course', 'COURSE')
    honors = neomodel.RelationshipTo('Honor', 'HONOR')
    languages = neomodel.RelationshipTo('Language', 'LANGUAGE')
    organizations = neomodel.RelationshipTo('Organization', 'ORGANIZATION')
    patents = neomodel.RelationshipTo('Patent', 'PATENT')
    projects = neomodel.RelationshipTo('Project', 'PROJECT')
    publications = neomodel.RelationshipTo('Publication', 'PUBLICATION')
    test_scores = neomodel.RelationshipTo('TestScore', 'TEST_SCORE')
    volunteer_experiences = neomodel.RelationshipTo(
        'VolunteerExp', 'VOLUNTEER_EXPERIENCE')
    sources = neomodel.RelationshipTo('Source', 'SOURCE')



class TimePeriod:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def return_(self) -> str:
        if self.end == None:
            return str(self.start["year"]) + "/" + str(self.start["month"]) + " - " + "till date"
        else:
            return str(self.start["year"]) + "/" + str(self.start["month"]) + " - " + str(self.end["year"]) + "/" + str(self.end["month"])


class InstantMessageService(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    id_ = neomodel.StringProperty()
    provider = neomodel.StringProperty()


class Attachment(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    title = neomodel.StringProperty()
    page_count = neomodel.StringProperty()


class Website(neomodel.StructuredNode):
    url = neomodel.StringProperty()
    member_id = neomodel.UniqueIdProperty()
    category = neomodel.StringProperty()


class Experience(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    title = neomodel.StringProperty()
    time_period = neomodel.StringProperty()
    company_name = neomodel.StringProperty()
    location = neomodel.StringProperty()
    emp_type = neomodel.StringProperty()


class Education(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    grade = neomodel.StringProperty()
    activities = neomodel.StringProperty()
    degree_name = neomodel.StringProperty()
    field = neomodel.StringProperty()
    institution_name = neomodel.StringProperty()
    time_period: TimePeriod
    description = neomodel.StringProperty()


class Certification(neomodel.StructuredNode):
    name = neomodel.StringProperty()
    # member_id = neomodel.UniqueIdProperty()
    url = neomodel.StringProperty()
    authority = neomodel.StringProperty()
    time_period: TimePeriod
    license_num = neomodel.StringProperty()


class Course(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    name = neomodel.StringProperty()
    num = neomodel.StringProperty()


class Honor(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    title = neomodel.StringProperty()
    issuer = neomodel.StringProperty()
    issued_on = neomodel.StringProperty()
    description = neomodel.StringProperty()


class Organization(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    name = neomodel.StringProperty()
    time_period: TimePeriod
    description = neomodel.StringProperty()
    position_held = neomodel.StringProperty()


class Patent(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    url = neomodel.StringProperty()
    title = neomodel.StringProperty()
    issuer = neomodel.StringProperty()
    filed_on = neomodel.StringProperty()
    pending = neomodel.BooleanProperty()
    issued_on = neomodel.StringProperty()
    description = neomodel.StringProperty()
    patent_num = neomodel.StringProperty()
    appl_num = neomodel.StringProperty()


class Project(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    url = neomodel.StringProperty()
    title = neomodel.StringProperty()
    time_period: TimePeriod
    description = neomodel.StringProperty()


class Publication(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    url = neomodel.StringProperty()
    name = neomodel.StringProperty()
    publisher = neomodel.StringProperty()
    description = neomodel.StringProperty()
    published_on = neomodel.StringProperty()


class Language(neomodel.StructuredNode):
    language = neomodel.StringProperty()
    # member_id = neomodel.UniqueIdProperty()
    proficiency = neomodel.StringProperty()


class TestScore(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    name = neomodel.StringProperty()
    score = neomodel.StringProperty()
    date_on = neomodel.StringProperty()
    description = neomodel.StringProperty()


class VolunteerExp(neomodel.StructuredNode):
    member_id = neomodel.UniqueIdProperty()
    role = neomodel.StringProperty()
    cause = neomodel.StringProperty()
    time_period: TimePeriod
    company_name = neomodel.StringProperty()
    description = neomodel.StringProperty()


class Source(neomodel.StructuredNode):
    member_profile_id = neomodel.StringProperty()
    # member_id = neomodel.UniqueIdProperty()
    connected_at = neomodel.StringProperty()
    is_connected = neomodel.BooleanProperty()
    was_connected = neomodel.BooleanProperty()


class ExpRelation(neomodel.StructuredRel):
    # must have no UniqueIDProperty :)
    title = neomodel.StringProperty()
    time_period = neomodel.StringProperty()
    company_name = neomodel.StringProperty()
    location = neomodel.StringProperty()
    emp_type = neomodel.StringProperty()


class Company(neomodel.StructuredNode):
    company_name = neomodel.UniqueIdProperty()
    exp_rel = neomodel.RelationshipTo(
        'Person', 'EXPERIENCE', model=ExpRelation)


class CompDict(TypedDict):
    name: str
    comp_node: Company

def add_data():

    data = []
    with open('profiles.json') as f:
        temp = f.read()
        if temp:
            data = json.loads(temp)

    companies: CompDict = {}
    companies_count = {}
    start = time.time()

    # 250 records
    # 16164 nodes ☠⚰
    # To increase node view count in graph display, go to Settings and increase initial node display value.

    for profile in data:
        member_id = profile['member_id']
        member_profile_id = profile['member_profile_id']
        name = profile['firstName'] + ' ' + profile['lastName']
        email = profile['email']
        phone = profile['phone']
        url = profile['url']
        location = profile['location'] if profile['location'] else ''
        headline = profile['headline']
        summary = profile['summary']
        is_open_to_work = profile['is_open_to_work']
        industry = profile['industry']
        address = profile['address']
        instant_message_service = profile['instant_message_service']
        twitter = profile['twitter'] if profile['twitter'] else ''
        attachments = profile['attachments']
        websites = profile['websites']
        birthday = profile['birthday']
        experiences = profile['experiences']
        educations = profile['educations']
        certifications = profile['certifications']
        courses = profile['courses']
        honors = profile['honors']
        languages = profile['languages']
        organizations = profile['organizations']
        patents = profile['patents']
        projects = profile['projects']
        publications = profile['publications']
        test_scores = profile['test_scores']
        volunteer_experiences = profile['volunteer_experiences']
        given_recommendations = profile['given_recommendations'] if profile['given_recommendations'] else ''
        received_recommendations = profile['received_recommendations'] if profile['received_recommendations'] else ''
        skills = " ".join(profile['skills'])
        sent_by = profile['sent_by']
        tag = " ".join(profile['tag'])
        connections_count = profile['connections_count']
        followers_count = profile['followers_count']
        updated_at = profile['updated_at']
        sources: List[dict] = profile['sources']

        person = Person(
            member_id=member_id,
            member_profile_id=member_profile_id,
            name=name,
            email=email,
            phone=phone,
            url=url,
            location=location,
            headline=headline,
            summary=summary,
            is_open_to_work=is_open_to_work,
            industry=industry,
            address=address,
            twitter=twitter,
            skills=" ".join(skills),
            tag=" ".join(tag),
            given_recommendations=given_recommendations,
            received_recommendations=received_recommendations,
            sent_by=sent_by,
            connections_count=connections_count,
            followers_count=followers_count,
            updated_at=updated_at,
        ).save()
        for instant_message_service in instant_message_service:
            person.instant_message_service.connect(InstantMessageService(
                member_id=member_id, id_=instant_message_service["id"], provider=instant_message_service["provider"]).save())
        for website in websites:
            person.websites.connect(Website(
                member_id=member_id,
                url=website["url"],
                category=website["category"] if "category" in website else ""
            ).save())

        try:
            for attachment in attachments:
                person.attachments.connect(Attachment(
                    member_id=member_id, title=attachment["title"], page_count=attachment["page_count"]).save())
        except:
            person.attachments.connect(Attachment(
                member_id=member_id, title="", page_count="").save())
        try:
            for experience in experiences:
                comp_name = experience["companyName"]
                if comp_name not in companies_count:
                    companies_count[comp_name] = 1
                else:
                    companies_count[comp_name] += 1
                if comp_name not in companies:
                    companies[comp_name] = Company(company_name=comp_name).save()
                companies[comp_name].exp_rel.connect(person, {
                    "member_id": member_id, "title": experience["title"], "time_period": TimePeriod(experience["timePeriod"]["startDate"], experience["timePeriod"]["endDate"]).return_() if "timePeriod" in experience else "", "company_name": comp_name, "location": experience["locationName"] if "locationName" in experience else "", "emp_type": experience["employmentType"] if experience["employmentType"] else "",
                })
                person.experiences.connect(Experience(member_id=member_id,
                                                    title=experience["title"],
                                                    time_period=TimePeriod(experience["timePeriod"]["startDate"], experience["timePeriod"]["endDate"]).return_(
                                                    ) if "timePeriod" in experience else "",
                                                    company_name=comp_name, location=experience["locationName"] if "locationName" in experience else "", emp_type=experience["employmentType"] if experience["employmentType"] else "").save())
        except Exception as e:
            pass

        try:
            for education in educations:
                person.educations.connect(Education(
                    member_id=member_id,
                    grade=education["grade"] if education["grade"] else "",
                    activities=education["activities"] if education["activities"] else "",
                    degree_name=education["degreeName"],
                    school_name=education["schoolName"],
                    time_period=TimePeriod(education["timePeriod"]["startDate"], education["timePeriod"]["endDate"]).return_(
                    ) if education["timePeriod"] else "",
                    description=education["description"] if education["description"] else "",
                    field_of_study=education["fieldOfStudy"],
                ).save())
        except Exception as e:
            pass

        try:
            for certification in certifications:
                person.certifications.connect(Certification(
                    # member_id=member_id,
                    url=certification["url"],
                    name=certification["name"],
                    authority=certification["authority"],
                    time_period=certification["timePeriod"],
                    license_num=certification["licenseNumber"],
                ).save())
        except Exception as e:
            pass

        try:
            for course in courses:
                person.courses.connect(Course(
                    member_id=member_id,
                    name=course["name"],
                    num=course["number"] if course["number"] else "",
                ).save())
        except Exception as e:
            pass

        try:
            for honor in honors:
                person.honors.connect(Honor(
                    member_id=member_id,
                    title=honor["title"],
                    issuer=honor["issuer"],
                    issued_on=str(honor["issuedOn"]),
                    description=honor["description"] if honor["description"] else "",
                ).save())
        except Exception as e:
            pass

        for language in languages:
            person.languages.connect(Language(
                # member_id=member_id,
                name=language["name"],
                proficiency=language["proficiency"],
            ).save())

        try:
            for organization in organizations:
                person.organizations.connect(Organization(
                    member_id=member_id,
                    name=organization["name"],
                    time_period=organization["timePeriod"] if organization["timePeriod"] else "",
                    description=organization["description"] if organization["description"] else "",
                    position_held=organization["positionHeld"],
                ).save())
        except Exception as e:
            pass

        try:
            for patent in patents:
                person.patents.connect(Patent(
                    member_id=member_id,
                    url=patent["url"],
                    title=patent["title"],
                    issuer=patent["issuer"],
                    filed_on=patent["filedOn"] if patent["filedOn"] else "",
                    pending=True if patent["pending"].lower() == "true" else False,
                    # {"day": 24, "year": 2015, "month": 11}
                    issued_on=str(patent["issuedOn"]),
                    description=patent["description"] if patent["description"] else "",
                    patent_number=patent["patentNumber"],
                    appl_number=patent["applicationNumber"] if patent["applicationNumber"] else "",
                ).save())
        except Exception as e:
            pass

        try:
            for project in projects:
                person.projects.connect(Project(
                    member_id=member_id,
                    url=project["url"] if project["url"] else "",
                    title=project["title"],
                    time_period=project["timePeriod"],
                    description=project["description"] if project["description"] else "",
                ).save())
        except Exception as e:
            pass

        try:
            for publication in publications:
                person.publications.connect(Publication(
                    member_id=member_id,
                    url=publication["url"] if publication["url"] else "",
                    name=publication["name"],
                    publisher=publication["publisher"],
                    description=publication["description"] if publication["description"] else "",
                    # {"year": 2015, "month": 11}
                    published_on=str(
                        publication["publishedOn"]) if publication["publishedOn"] else "",
                ).save())
        except Exception as e:
            pass

        try:
            for test_score in test_scores:
                person.test_scores.connect(TestScore(
                    member_id=member_id,
                    name=test_score["name"],
                    score=test_score["score"],
                    # {"day": 24, "year": 2015, "month": 11}
                    date_on=test_score["dateOn"],
                    description=test_score["description"] if test_score["description"] else "",
                ).save())
        except Exception as e:
            pass

        try:
            for volunteer_exp in volunteer_experiences:
                person.volunteer_experiences.connect(VolunteerExp(
                    member_id=member_id,
                    role=volunteer_exp["role"],
                    cause=volunteer_exp["cause"] if volunteer_exp["cause"] else "",
                    time_period=volunteer_exp["timePeriod"] if volunteer_exp["timePeriod"] else "",
                    company_name=volunteer_exp["companyName"],
                    description=volunteer_exp["description"] if volunteer_exp["description"] else "",
                ).save())
        except Exception as e:
            pass

        try:
            for source in sources:
                person.sources.connect(Source(
                    # member_id=member_id,
                    connected_at=source["connected_at"],
                    is_connected=source["is_connected"],
                    was_connected=source["was_connected"],
                    member_profile_id=source["member_profile_id"],
                ).save())
        except Exception as e:
            pass

        person.save()
    print(time.time() - start)
    # Print the company with max count from the companies_count dict
    print(max(companies_count, key=companies_count.get))
    # Print the dict
    print(companies_count)

def delete_all():
    neomodel.db.cypher_query("MATCH (n) DETACH DELETE n")

def max_company_jumps():
    pass

if __name__ == "__main__":
    print("Started..")
    add_data()
    # delete_all()