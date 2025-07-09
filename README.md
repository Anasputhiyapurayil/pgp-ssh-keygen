# 🔐 KeyGen Script

A Python-based CLI tool to generate PGP and SSH keys and export them automatically into structured folders. Useful for automation, backups, and managing user access.

---

## ✨ Features

- Generate **PGP keys** (RSA) with optional expiry
- Choose **armored or binary** format
- Automatically **exports** both public and private keys
- Also supports **SSH key generation**
- Saves all keys in folders named after the key (in script directory)

---

## 📦 Requirements

- Python 3.x
- GPG (`gpg`) and SSH installed on system

You can install Python dependencies with:

```bash
pip install -r requirements.txt
```

> Note: GPG and SSH must be installed on your system but are not Python packages.

---

## 🚀 Usage

```bash
python3 keygen.py
```

Follow the prompts in the CLI to generate keys.

---

## 📂 Output

All keys are saved in folders like:

```
./<keyname>/
    ├── keyname.pub
    └── keyname_Private.key
```

---

## 🔐 Important Notes

- For PGP generation, GPG must be installed (`sudo apt install gnupg` on Debian/Ubuntu).
- The script uses batch generation, so no password protection is applied by default.
