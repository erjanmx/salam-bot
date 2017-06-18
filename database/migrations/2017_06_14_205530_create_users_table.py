from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.integer('id')
            table.string('name')
            table.string('gender', 1)
            table.tiny_integer('status').default(0)
            table.integer('chat_id').unique()
            table.string('lang', 2).default('ru')
            table.timestamps()

            table.primary('id')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
