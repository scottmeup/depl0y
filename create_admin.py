#!/usr/bin/env python3
"""Create default admin user if it doesn't exist"""
import sys
sys.path.insert(0, '/opt/depl0y/backend')

from app.core.database import SessionLocal
from app.models import User, UserRole
from app.core.security import get_password_hash

def create_admin_user():
    """Create default admin user with 2FA disabled"""
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == 'admin').first()
        if existing_admin:
            print("Admin user already exists - resetting password and disabling 2FA")
            # Reset password to default and ensure 2FA is disabled
            existing_admin.hashed_password = get_password_hash("admin")
            existing_admin.totp_enabled = False
            existing_admin.totp_secret = None
            existing_admin.is_active = True
            db.commit()
            print("✓ Admin password reset to: admin")
            print("✓ 2FA disabled")
            print("✓ Account activated")
            return

        # Create new admin user
        hashed_password = get_password_hash("admin")
        admin_user = User(
            username="admin",
            email="admin@localhost",
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            is_active=True,
            totp_enabled=False,  # Explicitly disable 2FA
            totp_secret=None
        )

        db.add(admin_user)
        db.commit()
        print("✓ Created default admin user")
        print("  Username: admin")
        print("  Password: admin")
        print("  2FA: DISABLED")

    except Exception as e:
        print(f"✗ Error with admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
