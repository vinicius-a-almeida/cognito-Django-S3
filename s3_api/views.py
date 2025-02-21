from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
import json
from django.shortcuts import render
import hmac
import hashlib
import base64


def generate_secret_hash(client_id, client_secret, username):
    message = username + client_id
    dig = hmac.new(client_secret.encode('utf-8'), 
                   msg=message.encode('utf-8'), 
                   digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def index(request):
    return render(request, 'index.html')

# Configurações do AWS
COGNITO_USER_POOL_ID = 'us-east-1_gWwD2oeUK'  # Substitua pelo seu User Pool ID
COGNITO_APP_CLIENT_ID = '7bplru60bvb9872gu82tp0p9tm'  # Substitua pelo seu App Client ID
COGNITO_APP_CLIENT_SECRET = 'kcaogr5cfe46idcg9hdnhrin9u63nl19fai2i9m6g49n11qkb0h'
AWS_REGION = 'us-east-1'  # Substitua pela sua região
S3_BUCKET_NAME = 'jm-proof'  # Substitua pelo nome do seu bucket
S3_OBJECT_KEY = 'WhatsApp Image 2024-07-23 at 5.13.58 PM.jpeg'  # Substitua pelo caminho do objeto

# Cliente Cognito
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)

# Cliente S3
s3_client = boto3.client('s3', region_name=AWS_REGION)

@csrf_exempt
def get_signed_url(request):
    if request.method == 'POST':
        try:
            # Ler os dados do corpo da requisição
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Gerar SECRET_HASH
            secret_hash = generate_secret_hash(COGNITO_APP_CLIENT_ID, COGNITO_APP_CLIENT_SECRET, username)

            # Autenticar o usuário no Cognito
            response = cognito_client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SECRET_HASH': secret_hash  # Adicione o SECRET_HASH aqui
                },
                ClientId=COGNITO_APP_CLIENT_ID
            )

            # Gerar o URL assinado para o objeto no S3
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': S3_OBJECT_KEY
                },
                ExpiresIn=3600  # URL válido por 1 hora
            )

            return JsonResponse({
                'status': 'success',
                'signedUrl': signed_url
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido'
    }, status=405)