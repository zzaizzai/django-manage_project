from datetime import timedelta, datetime
from typing import Optional, List, Dict, Any, Union

from django.utils import timezone
from manage_project.settings.database import Base, session
from maintenance.models import MasterDepartment
from sqlalchemy.orm import undefer
from sqlalchemy import text, Column, Integer, String, create_engine, DateTime, Date, Sequence, Boolean, Text, func
from sqlalchemy import or_

class MyModel(Base):
    __tablename__ = 'my_model'
    id = Column(Integer, primary_key=True)


class CustomUser(Base):
    __tablename__ = 'accounts_customuser'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    last_login = Column(DateTime)
    date_joined = Column(DateTime)
    
    username = Column(String(150))
    last_name = Column(String(150))
    first_name = Column(String(150))
    email = Column(String(254))
    password = Column(String(128))
    
    is_superuser = Column(Boolean) 
    is_staff = Column(Boolean)
    is_active = Column(Boolean)
    is_manager = Column(Boolean)
    
    department_id = Column(Integer)

    
    def __str__(self):
        return self.username
    
    @property
    def name(self) -> str:
        return self.username
    
    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    def get_projects(self) -> List['Project'] :
        
        user_memebers = session.query(ProjectMember).filter_by(user_id = self.id).all()
        projects = [user_member.get_project_info() for user_member in user_memebers]
        return  projects
    
    def get_number_projects_completed(self) -> int:
        projects = self.get_projects()
        
        count_completed = 0
        for project in projects:
            if project.is_completed is True and project.is_canceled is False:
                count_completed += 1
        
        return count_completed
    
    def get_number_projects_canceled(self) -> int:
        projects = self.get_projects()
        
        count_canceled = 0
        for project in projects:
            if project.is_canceled is True:
                count_cancled += 1
        
        return count_canceled
    
    def get_number_projects(self) -> int:
        return  len(self.get_projects())
    
    @classmethod
    def get_user(cls, user_id) -> Optional['CustomUser']:
        user = session.query(CustomUser).filter_by(id=user_id).first()
        return user
    
    @classmethod
    def get_all_users(cls) -> List['CustomUser']:
        users = session.query(CustomUser).order_by(CustomUser.id.desc()).all()
        return users
    
    def get_department_info(self) -> Optional['MasterDepartment']:
        department = session.query(MasterDepartment).filter_by(id=self.department_id).first()
        return department
    
    def formatted_joined_time(self) -> str:
        return self.date_joined.strftime("%Y-%m-%d %H:%M") or "no joined time"


class PostBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_created_id = Column(Integer())
    datetime_created = Column(DateTime(timezone=True), server_default=text('NOW()'))
    datetime_updated = Column(DateTime(timezone=True), server_default=text('NOW()'))

    def show_time_created_ago(self):
        return self.formatted_time_ago(self.datetime_created)

    def formatted_time_ago(self, datetime: datetime) -> str:

        # it has timezone information
        created = datetime

        # datetime.now() does not have timezone information
        now = datetime.now(timezone.utc)

        # calculate the time diffrent
        time_difference = now - created

        if time_difference < timedelta(minutes=1):
            # under 1min
            seconds = int(time_difference.seconds)
            if seconds <= 10:
                return 'Now'
            return f'{seconds} secs'
        elif time_difference < timedelta(hours=1):
            # under 1hour
            minutes = int(time_difference.seconds / 60)
            if minutes == 1:
                return '1 min'
            return f'{minutes} mins'
        elif time_difference < timedelta(days=1):
            # under 24hours
            hours = int(time_difference.seconds / 3600)
            if hours == 1:
                return '1 hour'
            return f'{hours} hours'
        elif time_difference < timedelta(days=30):
            # under 30 days
            days = time_difference.days
            if days == 1:
                return '1 day'
            return f'{days} days'
        else:
            # over 30 days, consider it as months
            months = round(time_difference.days / 30)
            if months == 1:
                return '1 month'
            return f'{months} months'

    def get_user_info_with_id(self, id: int) -> Optional[CustomUser]:
        user = session.query(CustomUser).filter_by(id=id).first()
        session.close()
        return user

    def get_created_user_info(self):
        user = self.get_user_info_with_id(self.user_created_id)
        return user

        
    def show_time_created_with_updated(self) -> str:
        if self.formatted_datetime_updated() is None:
            return "Posted at " + self.formatted_datetime_created()
        return f"Posted at {self.formatted_datetime_created()} (Last updated at {self.formatted_datetime_updated()})"
    
    def formatted_datetime_created(self) -> str:
        return self.datetime_created.strftime("%Y-%m-%d %H:%M") or "Time Error"

    def formatted_datetime_updated(self) -> Union[str, None]:
        if self.datetime_created == self.datetime_updated or self.datetime_updated is None:
            return None
        return self.datetime_updated.strftime("%Y-%m-%d %H:%M") or None
    
    def formatted_datetime_due(self) -> str:
        if self.date_due:
            date_due = self.date_due.strftime("%Y-%m-%d")
            return f'Due by {date_due}'
        return "No due date"
    
    def show_time_duedate(self) -> str:
        return self.formatted_datetime_due()
    
    
class Project(PostBaseModel):

    __tablename__ = 'projects'

    title = Column(String(255))

    user_completed_id = Column(Integer, nullable=True)
    text = Column(Text)

    datetime_completed = Column(DateTime, nullable=True)
    date_due = Column(Date, nullable=True)
    datetime_canceled = Column(DateTime, nullable=True)

    is_canceled = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)

    def __str__(self):
        return self.title

    @classmethod
    def get_project(cls, project_id: int) -> Optional['Project']:
        project = session.query(Project).filter_by(id=project_id).first()
        return project
    
    @classmethod
    def get_projects(cls) -> List['Project']:
        projects = session.query(Project).order_by(Project.id.desc()).all()
        return projects
    
    @classmethod
    def create_project(cls) -> None:
        return

    @classmethod
    def get_projects_with_options(cls, search_word=None, sort_by=None, page=None) -> List['Project']:
        query = (
            session.query(Project)
            .join(CustomUser, Project.user_created_id == CustomUser.id)
            )

        if search_word:
            query = query.filter(
                or_(
                    Project.title.ilike(f"%{search_word}%"),
                    CustomUser.username.ilike(f"%{search_word}%")
                )
            )
            
        if sort_by:
            if sort_by == 'created':
                query = query.order_by(Project.datetime_created.desc())
            elif sort_by == 'id':
                query = query.order_by(Project.id.desc())
            else:
                pass
            
        query = query.order_by(Project.id.desc())

        projects = query.all()
        return projects
    
    @classmethod
    def get_demo_proejct(
        cls, 
        id:int = 999999, 
        datetime_created = datetime.now(timezone.utc),
        datetime_updated = datetime.now(timezone.utc)
        ) -> 'Project':
        return Project(
            id=id,
            title="DEMO PROJECT" , 
            text = "DEMO PROJECT",
            datetime_created = datetime_created,
            datetime_updated = datetime_updated
                    )
    
    def get_status_color(self) -> str:
        if self.is_canceled is True:
            return 'gray'
        if self.is_completed is True:
            return 'blue'
        return 'black'
    
    def get_status_str(self) -> str:
        if self.is_canceled is True:
            return "Cancled"
        if self.is_completed is True:
            return "Completed"
        return "Proceeding"
    
    def show_number_comments(self) -> str:
        return f'[{len(self.get_comments())}]'
    
    def get_comments(self) -> List['ProjectComment']:
        try:
            comments = session.query(ProjectComment).filter_by(
                project_id=self.id).all()
        except:
            comments = []
        finally:
            session.close()
            return comments
        
    def get_members(self) -> List['ProjectMember']:
        members = session.query(ProjectMember).filter_by(project_id=self.id).all()
        # session.close()
        return members
    
    def get_members_not_manager(self) -> List['ProjectMember']:
        all_members = self.get_members()
        members_not_manager = [member for member in all_members if not member.is_manager]
        return members_not_manager
        
    def get_members_is_manager(self) -> List['ProjectMember']:
        all_members = self.get_members()
        members_is_manager = [member for member in all_members if member.is_manager]
        return members_is_manager
    
    @classmethod
    def get_project_instance(cls, title: str, text: str, user_created_id: int) -> 'Project':
        project = Project(title=title, text=text, user_created_id=user_created_id)
        return  project
        
    
class ProjectComment(PostBaseModel):
    __tablename__ = 'project_comment'

    project_id = Column(Integer)
    text = Column(Text)


class ProjectMember(Base):

    __tablename__ = 'project_member'

    id = Column(Integer, primary_key=True, autoincrement=True)

    project_id = Column(Integer)
    user_id = Column(Integer)
    is_manager = Column(Boolean, default=False)
    
    def get_user_info(self) -> Optional[CustomUser]:
        user = session.query(CustomUser).filter_by(id=self.user_id).first()
        # session.close()
        return user
    
    def get_project_info(self) -> Optional[Project]:
        projects = session.query(Project).filter_by(id=self.project_id).first()
        # session.close()
        return projects
        
        
class DummyData():
    
    def get_project_dummy(self) -> Dict[str, Any]:
        
        from faker import Faker
        import random
        
        fake = Faker()
        
        business_sentence_1 = fake.sentence(nb_words=15, variable_nb_words=True, ext_word_list=None)
        business_sentence_2 = fake.sentence(nb_words=20, variable_nb_words=True, ext_word_list=None)
        business_sentence_3 = fake.sentence(nb_words=25, variable_nb_words=True, ext_word_list=None)

        # 3줄 합치기
        combined_business_sentences = f"{business_sentence_1} {business_sentence_2} {business_sentence_3}"
        
        start_date = datetime.strptime('2022-01-01', '%Y-%m-%d')
        end_date = datetime.today()

        random_date = fake.date_between(start_date=start_date, end_date=end_date)
        due_date = random_date + timedelta(days=random.randint(10, 60))
        
        fake_data = {
            'user_created_id' : random.randint(1,4),
            'title': fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None),
            'datetime_created': random_date,
            'due_date': due_date,
            'text': combined_business_sentences
        }
        
        return fake_data
    
    def add_proejct_dummy(self):
        
        dummy_data = self.get_project_dummy()
        dummy_project = Project().get_project_instance(
            user_created_id=dummy_data['user_created_id'],
            title=dummy_data['title'],
            text=dummy_data['text']
            )
        dummy_project.datetime_created=dummy_data['datetime_created']
        dummy_project.date_due=dummy_data['due_date']
        
        session.add(dummy_project)
        session.commit()
        
        return 
    
    def add_proejct_dummys(self, number: int) -> None:
        for _ in range(10):
            self.add_proejct_dummy()
        return 
