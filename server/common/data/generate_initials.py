class GenerateInitials:
    @classmethod
    def generate_theorist_data(cls, self):
        from server.apps.theorist.models import TheoristProfileSettings, TheoristFriendshipBlackList
        from server.apps.theorist_chat.models import TheoristChatGroupConfiguration
        from server.apps.theorist_drafts.models import TheoristDraftsConfiguration
        from server.apps.game_area.models import MathQuizScoreboard

        TheoristProfileSettings.objects.create(theorist=self)
        TheoristDraftsConfiguration.objects.create(theorist=self)
        TheoristChatGroupConfiguration.objects.create(theorist=self)
        TheoristFriendshipBlackList.objects.create(owner=self)
        MathQuizScoreboard.objects.create(solved_by=self)
