from .base_model import BaseModel

class CompanyUserModel(BaseModel):
    table = 'company_users'
    fields = ['id', 'company_id', 'user_id','role', 'created_at']

    def for_user(self, user_id):
        """
        Fetch all company assignments for a given user
        Returns a list of dicts
        """
        cur = self.conn.execute('''
            SELECT cu.*, c.name as company_name
            FROM company_users cu
            JOIN companies c ON c.id = cu.company_id
            WHERE cu.user_id = ?
        ''', (user_id,))
        return [dict(r) for r in cur.fetchall()]