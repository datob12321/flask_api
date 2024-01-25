from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import Session, declarative_base
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData,  Column, String, Integer

engine = create_engine("mysql+mysqlconnector://root:dato.123.mysql@localhost/school")

connection = engine.connect()

Base = declarative_base()

class Students(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(50), nullable=False)
    student_last_name = Column(String(50), nullable=False)

Base.metadata.create_all(engine)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form['last_name']
        try:
            with Session(engine) as session:
                session.add(Students(student_name=name, student_last_name=lastname))
                session.commit()
                return redirect(url_for('table'))
        except:
            return 'There was an error with adding'
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/table')
def table():
    with Session(engine) as session:
        info = session.query(Students).all()

    return render_template('tables.html', student_info=info)


if __name__ == '__main__':
    app.run(debug=True)
