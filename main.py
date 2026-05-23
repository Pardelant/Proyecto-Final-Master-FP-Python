from app import create_app

app = create_app()

if __name__ == "__main__":
    app.secret_key = "mi_clave_secreta_super_segura_123"  # <-- Pon esto aquí
    app.run(debug=True)
