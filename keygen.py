#!/usr/bin/env python3
"""
==============================================================================
 🔐 KeyGen Script
------------------------------------------------------------------------------
 A simple Python CLI tool to generate PGP and SSH key pairs, export them to
 a local folder structure, and optionally manage GPG keyring entries.

 Author      : Anas
 Version     : 1.0
 License     : MIT
 Dependencies: gpg, ssh-keygen (available on most Unix systems)
==============================================================================
"""

import subprocess
import os

def generate_pgp_key():
    key_name = input("Enter key name (used for folder/filenames): ").strip()
    real_name = input("Enter real name: ").strip()
    email = input("Enter email: ").strip()
    expire_date = input("Enter key validity (e.g. 1y, 2m, 0 = never): ").strip()
    key_length = input("Enter key length (default 2048): ").strip() or "2048"
    armored = input("Export keys in armored format? (y/n): ").strip().lower() == "y"

    # Setup folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    key_dir = os.path.join(script_dir, key_name)
    os.makedirs(key_dir, exist_ok=True)

    # Create GPG key input file
    batch_file = os.path.join(key_dir, f"{key_name}_keygen_input")

    key_input = f"""
    Key-Type: RSA
    Key-Length: {key_length}
    Subkey-Type: RSA
    Subkey-Length: {key_length}
    Name-Real: {real_name}
    Name-Email: {email}
    Expire-Date: {expire_date}
    %no-protection
    %commit
    """

    with open(batch_file, "w") as f:
        f.write(key_input.strip())

    print("🔧 Generating PGP key...")
    subprocess.run(["gpg", "--batch", "--generate-key", batch_file], check=True)
    os.remove(batch_file)

    # Define export paths
    private_key_path = os.path.join(key_dir, f"{key_name}_Private.key")
    public_key_path = os.path.join(key_dir, f"{key_name}.pub")

    print("📤 Exporting keys to disk...")
    try:
        # Export public key
        with open(public_key_path, "wb") as pub_out:
            cmd_pub = ["gpg", "--armor" if armored else "--no-armor", "--export", email]
            subprocess.run(cmd_pub, stdout=pub_out, check=True)

        # Export private key
        with open(private_key_path, "wb") as priv_out:
            cmd_priv = ["gpg", "--armor" if armored else "--no-armor", "--export-secret-keys", email]
            subprocess.run(cmd_priv, stdout=priv_out, check=True)

        print(f"✅ PGP keys exported to folder: {key_dir}\n")
    except subprocess.CalledProcessError as e:
        print("❌ Export failed:", e)

def generate_ssh_key():
    key_name = input("Enter SSH key filename (without extension): ").strip()

    # Setup folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    key_dir = os.path.join(script_dir, key_name)
    os.makedirs(key_dir, exist_ok=True)

    key_path = os.path.join(key_dir, key_name)

    print("🔧 Generating SSH key pair...")
    subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "2048", "-f", key_path, "-N", ""])

    print(f"✅ SSH keys generated in folder:\n - Private: {key_path}\n - Public: {key_path}.pub\n")

def main_menu():
    print("=== KEY GENERATION SCRIPT ===")
    print("1) Generate PGP Key")
    print("2) Generate SSH Key")
    print("0) Exit")

    choice = input("Select an option: ").strip()
    if choice == "1":
        generate_pgp_key()
    elif choice == "2":
        generate_ssh_key()
    elif choice == "0":
        print("Exiting...")
        exit()
    else:
        print("❌ Invalid option, try again.")

if __name__ == "__main__":
    while True:
        main_menu()
