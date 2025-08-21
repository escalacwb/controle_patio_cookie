# auth_utils.py

import streamlit as st
import streamlit_authenticator as stauth
from database import get_connection, release_connection
import pandas as pd

def fetch_users_from_db():
    # ... (esta função permanece igual)
    conn = get_connection()
    if not conn:
        st.error("Falha ao conectar ao banco de dados para autenticação.")
        return None
    try:
        query = "SELECT nome, username, password_hash, role FROM usuarios"
        # A warning do pandas pode ser ignorada, não é a causa do erro.
        df_users = pd.read_sql(query, conn)
        
        credentials = {"usernames": {}}
        for index, row in df_users.iterrows():
            credentials["usernames"][row['username']] = {
                "name": row['nome'],
                "password": row['password_hash'],
                "role": row['role']
            }
        return credentials
    except Exception as e:
        st.error(f"Erro ao buscar usuários: {e}")
        return None
    finally:
        release_connection(conn)

def initialize_authenticator():
    """
    Inicializa o objeto de autenticação com os dados do banco.
    """
    cookie_config = st.secrets.get("cookie", {})
    credentials = fetch_users_from_db()
    
    if credentials and credentials.get("usernames"):
        # --- CORREÇÃO APLICADA AQUI ---
        # Os parâmetros do cookie agora são passados pelos seus nomes corretos.
        authenticator = stauth.Authenticate(
            credentials=credentials,
            cookie_name=cookie_config.get('name', 'some_cookie_name'),
            key=cookie_config.get('key', 'some_signature_key'),
            cookie_expiry_days=cookie_config.get('expiry_days', 30)
        )
        return authenticator
        
    return None

def hash_new_password(password):
    # ... (esta função permanece igual)
    return stauth.Hasher([password]).generate()[0]