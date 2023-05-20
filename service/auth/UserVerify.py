from datetime import datetime
from random import randint
from dataclasses import asdict
# from sqlalchemy import insert


# def check_user(user_obj):
#     session = Session()
#     user = None
#     try:
#         user = session.query(User).filter(User.email == user_obj.get("email")).first()
#     except Exception as e:
#         logConfig.logError("Error in check user  => " + str(e))
#     finally:
#         session.close()
#         return user


# def GetUserGroup(user_id):
#     session = Session()
#     temp = []
#     try:
#         groups = (
#             session.query(EntityRelation, Entity)
#             .join(Entity, Entity.entityid == EntityRelation.following_entity)
#             .filter(EntityRelation.follower_entity == user_id)
#             .all()
#         )
#         temp = [{**asdict(group[0]), **asdict(group[1])} for group in groups]

#     except Exception as e:
#         logConfig.logError("Error in check user  => " + str(e))
#     finally:
#         session.close()
#         return temp


# def InsertUser(user_obj):
#     date = datetime.utcnow()

#     # checks user
#     user = check_user(user_obj)
#     data = {}
#     session = Session()
#     groups = []
#     try:
#         if user != None:
#             # User Exist
#             entity = (
#                 session.query(Entity).filter(Entity.entityid == user.entityid).first()
#             )
#             entity.last_active = date
#             data = {
#                 **asdict(entity),
#                 "location": asdict(entity.location),
#                 **asdict(user),
#             }
#             groups = GetUserGroup(user.entityid)
#             session.add(entity)
#             pass
#         else:
#             # User Not Exist
#             username_temp = user_obj.get("user_name").replace(" ", "") + str(
#                 randint(10, 99999)
#             )

#             entity = Entity(
#                 entity_type=EntityType.User,
#                 unique_name=username_temp,
#                 display_name=user_obj.get("user_name"),
#                 picture=user_obj.get("picture"),
#                 about="",
#             )
#             entity.last_active = date
#             entity.created_at = date
#             session.add(entity)
#             session.flush()
#             user_res_obj = User(entityid=entity.entityid, email=user_obj.get("email"))
#             data = {
#                 **asdict(entity),
#                 "location": asdict(entity.location),
#                 **asdict(user_res_obj),
#             }
#             groups = GetUserGroup(entity.entityid)
#             session.add(user_res_obj)

#         data = {"profile": data, "groups": groups}
#         session.commit()
#     except Exception as e:
#         logConfig.logError("Error in User Registration  => " + str(e))
#     finally:
#         session.close()
#         return data
