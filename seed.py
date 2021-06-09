from app import app
from models import db, connect_db, User, Feedback


db.drop_all()
db.create_all()

u1 = User(username='yesgirl', password='ofcourse', email='yesgirl101@gmail.com', first_name='Kate', last_name='Walsh')
u2 = User(username='noboy', password='definitelynot', email='notarealemail@yahoo.com', first_name='Lamar', last_name='Odom')
u3 = User(username='dreamComeTrue67', password='hoopdream$', email='startbasketballplayer@hoops.net', first_name='Kobe', last_name='Bryant')
u4 = User(username='musicISLIFE', password='LYRICS', email='dodadum@piano.org', first_name='Alicia', last_name='Keys')

db.session.add_all([u1, u2, u3, u4])
db.session.commit()