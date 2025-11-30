from .base_model import BaseModel

class CompaniesModel(BaseModel):
    table = 'companies'
    fields = ['id', 'name', 'created_at', 'updated_at']
