from .base_model import BaseModel

class DepartmentUserModel(BaseModel):
    table = 'department_users'
    fields = ['id', 'department_id', 'user_id', 'created_at']

    def for_user(self, user_id):
        """
        Fetch all department assignments for a given user
        Returns a list of dicts
        """
        cur = self.conn.execute('''
            SELECT du.*, d.name as department_name
            FROM department_users du
            JOIN departments d ON d.id = du.department_id
            WHERE du.user_id = ?
        ''', (user_id,))
        return [dict(r) for r in cur.fetchall()]