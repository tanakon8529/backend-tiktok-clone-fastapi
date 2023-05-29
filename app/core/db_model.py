from sqlalchemy import Column, Integer, VARCHAR, Text, DateTime, Date, Float, JSON, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'user_profile'

    profile_name_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    profile_name = Column(VARCHAR(100), nullable=True)
    images_profile_uuid = Column(VARCHAR(36), nullable=True)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    username = Column(Text, nullable=False)
    bio = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    interests = Column(JSON, nullable=True)
    cookie_cache_key = Column(Text, nullable=True)

class Follower(Base):
    __tablename__ = 'follower'

    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), primary_key=True, nullable=False)
    follower_profile_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)

class Following(Base):
    __tablename__ = 'following'

    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), primary_key=True, nullable=False)
    following_profile_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)

class PersonalInformation(Base):
    __tablename__ = 'personal_information'

    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    gender = Column(VARCHAR(255), nullable=True)
    email = Column(VARCHAR(255), nullable=True)
    mobile_phone_number = Column(VARCHAR(255), nullable=True)
    password = Column(VARCHAR(255), nullable=True)
    birth_day = Column(Date, nullable=True)
    country_code = Column(VARCHAR(6), nullable=True)

class Consent_Collection(Base):
    __tablename__ = 'consent_collection'

    consent_collection_id = Column(Integer, primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    name = Column(Text, nullable=False)
    detail_consent = Column(Text, nullable=False)
    system_files_id = Column(Integer, ForeignKey('system_files.system_files_id'), nullable=True)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)

class Consent_Transaction(Base):
    __tablename__ = 'consent_transaction'

    consent_transaction_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    consent_collection_id = Column(Integer, ForeignKey('consent_collection.consent_collection_id'), nullable=False)
    create_date = Column(DateTime, nullable=False)
    expired_date = Column(DateTime, nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)

class System_Files(Base):
    __tablename__ = 'system_files'

    system_files_id = Column(Integer, primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    file_name = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    file_size_kb = Column(Integer, nullable=False)
    file_key_s3 = Column(Text, nullable=False)
    file_url_s3 = Column(Text, nullable=False)
    file_url_expire_date_s3 = Column(DateTime, nullable=False)
    type_upload = Column(VARCHAR, nullable=True)

class Countries(Base):
    __tablename__ = 'countries'

    country_code = Column(VARCHAR(6), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    country_name = Column(VARCHAR(255), nullable=False)

class TransactionHistory(Base):
    __tablename__ = 'transaction_history'

    transaction_history_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    transaction_name = Column(Text, nullable=True)
    transaction_detail = Column(Text, nullable=True)
    transaction_return = Column(JSON, nullable=True)

class ClipsProfile(Base):
    __tablename__ = 'clips_profile'

    clips_profile_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=True)
    file_name = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    file_size_kb = Column(Integer, nullable=False)
    file_key_s3 = Column(Text, nullable=False)
    file_url_s3 = Column(Text, nullable=False)
    file_url_expire_date_s3 = Column(DateTime, nullable=False)

class ClipsGroup(Base):
    __tablename__ = 'clips_group'

    clips_group_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    group_information_uuid = Column(VARCHAR(36), ForeignKey('group_information.group_information_uuid'), nullable=True)
    file_name = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    file_size_kb = Column(Integer, nullable=False)
    file_key_s3 = Column(Text, nullable=False)
    file_url_s3 = Column(Text, nullable=False)
    file_url_expire_date_s3 = Column(DateTime, nullable=False)

class ImagesProfile(Base):
    __tablename__ = 'images_profile'

    images_profile_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    file_name = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    file_size_kb = Column(Integer, nullable=False)
    file_key_s3 = Column(Text, nullable=False)
    file_url_s3 = Column(Text, nullable=False)
    file_url_expire_date_s3 = Column(DateTime, nullable=False)

class ImagesGroup(Base):
    __tablename__ = 'images_group'

    images_group_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    group_information_uuid = Column(VARCHAR(36), ForeignKey('group_information.group_information_uuid'), nullable=True)
    file_name = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    file_size_kb = Column(Integer, nullable=False)
    file_key_s3 = Column(Text, nullable=False)
    file_url_s3 = Column(Text, nullable=False)
    file_url_expire_date_s3 = Column(DateTime, nullable=False)

class VotingData(Base):
    __tablename__ = 'voting_data'

    voting_data_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    name_vote = Column(Text, nullable=False)
    type_vote = Column(VARCHAR(255), nullable=False)
    block_data = Column(Text, nullable=False)

class VotingMembers(Base):
    __tablename__ = 'voting_members'

    voting_data_uuid = Column(VARCHAR(36), ForeignKey('voting_data.voting_data_uuid'), primary_key=True)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)

    voting_data = relationship('VotingData', foreign_keys=[voting_data_uuid])

class GroupInformation(Base):
    __tablename__ = 'group_information'

    group_information_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    group_name = Column(Text, nullable=False)
    group_leader_profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    group_voting_date_next_round = Column(DateTime, nullable=True)
    group_voting_history = Column(JSON, nullable=True)

class GroupMembers(Base):
    __tablename__ = 'group_members'

    group_information_uuid = Column(VARCHAR(36), ForeignKey('group_information.group_information_uuid'), primary_key=True)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)

    group_information = relationship('GroupInformation', foreign_keys=[group_information_uuid])

class GroupChatAndPostHistory(Base):
    __tablename__ = 'group_chat_and_post_history'

    group_chat_and_post_history_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    group_information_uuid = Column(VARCHAR(36), ForeignKey('group_information.group_information_uuid'), nullable=False)
    post_by_profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    content_text = Column(Text, nullable=True)
    clips_group_uuid = Column(VARCHAR(36), ForeignKey('clips_group.clips_group_uuid'), nullable=True)
    images_group_uuid = Column(VARCHAR(36), ForeignKey('images_group.images_group_uuid'), nullable=True)

class MessageChat(Base):
    __tablename__ = 'message_chat'

    message_chat_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)

class MessageMembers(Base):
    __tablename__ = 'message_members'

    message_chat_uuid = Column(VARCHAR(36), ForeignKey('message_chat.message_chat_uuid'), primary_key=True, nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)

    message_chat = relationship('MessageChat', foreign_keys=[message_chat_uuid])

class MessageChatHistory(Base):
    __tablename__ = 'message_chat_history'

    message_chat_history_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    message_chat_uuid = Column(VARCHAR(36), ForeignKey('message_chat.message_chat_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    content_text = Column(Text, nullable=True)
    clips_group_uuid = Column(VARCHAR(36), ForeignKey('clips_group.clips_group_uuid'), nullable=True)
    images_group_uuid = Column(VARCHAR(36), ForeignKey('images_group.images_group_uuid'), nullable=True)
    me_or_another = Column(Boolean, nullable=False)

class UserActivity(Base):
    __tablename__ = 'user_activity'

    user_activity_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    content = Column(JSON, nullable=True)
    likes = Column(Integer, nullable=True)
    clips_group_uuid = Column(VARCHAR(36), ForeignKey('clips_group.clips_group_uuid'), nullable=True)
    images_group_uuid = Column(VARCHAR(36), ForeignKey('images_group.images_group_uuid'), nullable=True)

class Comments(Base):
    __tablename__ = 'comments'

    comment_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    user_activity_uuid = Column(VARCHAR(36), ForeignKey('user_activity.user_activity_uuid'), nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    content_text = Column(Text, nullable=True)
    likes = Column(Integer, nullable=True)

class InComments(Base):
    __tablename__ = 'in_comments'

    in_comment_uuid = Column(VARCHAR(36), primary_key=True, nullable=False)
    comment_uuid = Column(VARCHAR(36), ForeignKey('comments.comment_uuid'), nullable=False)
    profile_name_uuid = Column(VARCHAR(36), ForeignKey('user_profile.profile_name_uuid'), nullable=False)
    create_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
    content_text = Column(Text, nullable=True)
    likes = Column(Integer, nullable=True)