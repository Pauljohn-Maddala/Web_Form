
import os

class ForumMember:
    def __init__(self, member_id, access_key, nickname, moderator_status=False, mod_access_key=None, full_name=None):
        self.member_id = member_id
        self.access_key = access_key
        self.nickname = nickname
        self.moderator_status = moderator_status
        self.mod_access_key = mod_access_key if moderator_status else None
        self.full_name = full_name

class MemberManager:
    def __init__(self):
        self.members = {}
        self.id_counter = 0

    def create_forum_moderator(self, nickname, full_name):
        self.id_counter += 1
        member_access_key = os.urandom(24).hex()
        moderator_key = os.urandom(24).hex()
        new_member = ForumMember(self.id_counter, member_access_key, nickname, True, moderator_key, full_name)
        self.members[self.id_counter] = new_member
        return new_member

    def register_member(self, nickname, full_name):
        for member in self.members.values():
            if member.nickname == nickname:
                raise ValueError("Nickname already in use")

        self.id_counter += 1
        member_access_key = os.urandom(24).hex()
        new_member = ForumMember(self.id_counter, member_access_key, nickname, full_name=full_name)
        self.members[self.id_counter] = new_member
        return new_member

    def validate_member(self, member_id, provided_key):
        if member_id in self.members:
            return self.members[member_id].access_key == provided_key
        return False

    def get_member_info(self, member_id):
        if member_id in self.members:
            member = self.members[member_id]
            return {'nickname': member.nickname, 'full_name': member.full_name}
        return None