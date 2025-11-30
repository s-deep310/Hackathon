from .base_model import BaseModel

class DepartmentModel(BaseModel):
    table = 'departments'
    fields = ['id', 'company_id', 'name', 'created_at', 'updated_at']

    def for_company_with_name(self):
        """Fetch all departments with company names"""
        sql = '''
        SELECT 
            d.id AS department_id,
            c.name AS company_name,
            d.name AS department_name,
            d.created_at
        FROM 
            departments d
        JOIN 
            companies c ON d.company_id = c.id
        '''
        cur = self.conn.execute(sql)
        return [dict(row) for row in cur.fetchall()]
