from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', examples=['nitish', 'sayan'], description='Less than 50 characters')]
    portfolio: AnyUrl
    email: EmailStr
    age: int
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: bool = False
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

    # ✅ Model-level validation (runs after individual fields are validated)
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model

    # ✅ Email domain validation
    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, value):
        print("Class:", cls)
        print("Email value being validated:", value)
        valid_domains = ['nitrkl.ac.in', 'hdfc.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value

    # ✅ Capitalize name
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    # ✅ Age validation before type casting
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be between 0 and 100')

# ✅ Insert function
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.married)
    print(patient.portfolio)
    print('inserted')

# ✅ Update function
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.contact_details)
    print('updated')

# ✅ Example dictionaries
patient_info = {
    'name': 'shiladitya',
    'portfolio': 'https://lk.com',
    'email': 'shialdityam@hdfc.com',
    'age': 30,
    'weight': 75.2,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {'phone': '897536'}
}

patient_information = {
    'name': 'shiladitya',
    'portfolio': 'https://lk.com',
    'email': 'shialdityam@nitrkl.ac.in',
    'age': 70,
    'weight': 75.2,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'email': 'shialdityam@gmail.com',
        'phone': '897536',
        'emergency': '100'
    }
}

patient1 = Patient(**patient_info)
patient2 = Patient(**patient_information)

insert_patient_data(patient1)
insert_patient_data(patient2)
