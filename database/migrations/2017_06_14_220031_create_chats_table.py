from orator.migrations import Migration


class CreateChatsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('chats') as table:
            table.increments('id')
            table.integer('user_1').unique()
            table.integer('user_2').unique()
            table.timestamp('started_at')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('chats')
