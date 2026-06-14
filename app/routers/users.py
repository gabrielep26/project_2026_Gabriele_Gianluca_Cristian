@router.get("/")
def get_all_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

