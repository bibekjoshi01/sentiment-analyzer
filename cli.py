import typer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from passlib.hash import bcrypt
from datetime import datetime

app = typer.Typer()


@app.command()
def create_superuser(
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
    full_name: str = typer.Option(..., prompt=True),
):
    """Create a new superuser"""
    print(f"Creating superuser with email: {email}")
    db: Session = SessionLocal()

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        typer.echo("❌ User with this email already exists.")
        raise typer.Exit(code=1)

    hashed_password = bcrypt.hash(password)

    user = User(
        email=email,
        password=hashed_password,
        full_name=full_name,
        is_active=True,
        is_superuser=True,
        created_at=datetime.now(),
    )

    db.add(user)
    db.commit()
    typer.echo(f"✅ Superuser '{email}' created successfully!")


if __name__ == "__main__":
    app()
