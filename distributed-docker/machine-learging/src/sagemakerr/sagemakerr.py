from sagemaker import get_execution_role, Session
from sagemaker.sklearn import SKLearnModel
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

entry_point_path = os.path.join(os.getcwd(), "src/sagemakerr/inference.py")

# Cargar las variables de entorno
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.getenv("aws_secret_access_key")
ROLE = os.getenv("ROL_ARN")

model_key = "model/model.tar.gz"
model_s3_path = f"s3://{BUCKET_NAME}/{model_key}"

# Crear la sesión de SageMaker
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-2',
)

sagemaker_session = Session(
    boto_session=boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2',
    )
)

# Crear el cliente de SageMaker
sagemaker_client = sagemaker_session.boto_session.client('sagemaker')

class SageMakerr:
    def __init__(self):
        self.region = 'us-east-2'
        self.role = ROLE
        self.model_path = model_s3_path
        self.client = boto3.client('sagemaker', region_name=self.region)
        self.sagemaker_session = sagemaker_session
    
    def deploy_model(self):
        sklearn_model = SKLearnModel(
            model_data=self.model_path,
            role=self.role,
            entry_point=entry_point_path,  # Asegúrate de que esté en el lugar correcto
            framework_version="0.23-1",
            py_version="py3",
            sagemaker_session=self.sagemaker_session,
        )

        predictor = sklearn_model.deploy(
            instance_type="ml.m5.large",
            initial_instance_count=1
        )

        print(f"Modelo desplegado en el endpoint: {predictor.endpoint_name}")
        return predictor