from app import create_app, db
from app.auth.models import User
from app.data import load_data, load_data_list
from app.models import About, Certification, Contact, GitHubProject, Project, Skill
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    with db.engine.connect() as connection:
        if (
            db.engine.dialect.has_table(connection, "about")
            or db.engine.dialect.has_table(connection, "contact")
            or db.engine.dialect.has_table(connection, "project")
            or db.engine.dialect.has_table(connection, "task")
            or db.engine.dialect.has_table(connection, "skill")
            or db.engine.dialect.has_table(connection, "git_hub_project")
            or db.engine.dialect.has_table(connection, "certification")
        ):
            db.drop_all()
    db.create_all()
    about_instance = load_data(About, "about.json")
    contact_instance = load_data(Contact, "contact.json")
    project_instances = load_data_list(Project, "projects.json")
    skills_instances = load_data_list(Skill, "skills.json")
    github_project_instances = load_data_list(GitHubProject, "github_projects.json")
    certification_instances = load_data_list(Certification, "certs.json")

    user = User(
        username="Psychoorc", password=generate_password_hash("P422w0rd4Schottel23")
    )
    db.session.add(user)
    db.session.add(about_instance)
    db.session.add(contact_instance)
    db.session.add_all(skills_instances)
    db.session.add_all(project_instances)
    db.session.add_all(github_project_instances)
    db.session.add_all(certification_instances)

    db.session.commit()
    print("Datenbank wurde erfolgreich initialisiert.")
