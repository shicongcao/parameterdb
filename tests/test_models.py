from app.modules.auth.models import User

def test_user_creation(db_session):
    new_user = User(username='testuser', email='test@example.com', password_hash='hashedpassword')
    db_session.add(new_user)
    db_session.commit()
    user_in_db = db_session.query(User).first()
    assert user_in_db.username == 'testuser'