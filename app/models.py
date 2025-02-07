from dataclasses import dataclass


@dataclass
class PersonBase:
    role: str


@dataclass
class Contact:
    vorname: str
    nachname: str
    email: str
    linkedin: str
    github: str
    profile_image: str

    @property
    def name(self) -> str:
        return f"{self.vorname} {self.nachname}"


@dataclass
class About(PersonBase):
    greeting: str
    bio: str


@dataclass
class Project:
    title: str
    shortDescription: str
    rolle: str
    description: str
    aufgaben: list[str]
    technologien: str
    von: str
    bis: str
    logo: str
    link: str


@dataclass
class GitHubProject:
    title: str
    shortDescription: str
    description: str
    link: str
    technologien: str
    logo: str
    wip: bool


@dataclass
class Skill:
    name: str
    level: str
    icon: str
    info: str
    description: str
    link: str


@dataclass
class Certification:
    name: str
    description: str
    date: str
    link: str
    image: str
