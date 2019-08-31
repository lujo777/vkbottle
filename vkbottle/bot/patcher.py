class Patcher:
    def __init__(self, logger):
        self.logger = logger
        self.whitelist = list()

    async def add_whitelist(self, *user_id: int):
        self.whitelist.extend(user_id)
        await self.logger('Теперь WhiteList содержит: ', self.whitelist)

    async def remove_from_whitelist(self, *user_ids: int):
        for user_id in user_ids:
            if user_id in self.whitelist:
                self.whitelist.pop(self.whitelist.index(user_id))
            else:
                await self.logger.warn('User {} not in whitelist already'.format(user_id))
        return self.whitelist

    async def check_for_whitelist(self, obj):
        peer_id = obj['from_id']
        return self.whitelist is list() or peer_id in self.whitelist
