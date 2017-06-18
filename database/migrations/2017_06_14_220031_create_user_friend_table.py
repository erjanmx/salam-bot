from orator.migrations import Migration


class CreateUserFriendTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('user_friends') as table:
            table.increments('id')
            table.integer('user_1').unique()
            table.integer('user_2').unique()

            table.foreign('user_1').references('id').on('users')
            table.foreign('user_2').references('id').on('users')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('user_friends')
