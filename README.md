<div align="center">
<img src="https://raw.githubusercontent.com/bsamarji/Keepr/main/docs/assets/keepr_logo.png" width=600 alt="Keepr Logo">
<h1>Keepr: A lightweight, end-to-end encrypted password manager for developers - built for the terminal.</h1>
<br/>
<a href="https://pypi.org/project/Keepr"><img src="https://img.shields.io/pypi/v/keepr.svg" alt="PyPI Version"></a>
<a href="https://bsamarji.github.io/Keepr/"><img src="https://img.shields.io/badge/official_docs-yellow.svg" alt="MIT License"></a>
<a href="https://pepy.tech/projects/keepr"><img src="https://static.pepy.tech/personalized-badge/keepr?period=total&units=ABBREVIATION&left_color=GREY&right_color=MAGENTA&left_text=downloads" alt="PyPI Downloads"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/built_with-python3-bright_green.svg" alt="Built with Python3"></a>
<a href="LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License badge"></a>
<a href="https://github.com/bsamarji/Keepr"><img src="https://img.shields.io/github/stars/bsamarji/Keepr?style=social" alt="GitHub stars"></a>
</div>

Keepr is a secure, cross-platform command-line password manager designed for software developers.
It stores your credentials in an encrypted [SQLCipher](https://www.zetetic.net/sqlcipher/) database that lives **entirely on your local machine**, ensuring complete control over your data. 
No servers, no cloud syncing — just strong, local encryption.

The vault is protected by a **Master Password** derived into a strong encryption key using an industry-standard PBKDF2-HMAC key derivation function (SHA256, 1.2M iterations).
Your data remains safe even if the database or key files are compromised.

---

## 🧠 Why Keepr?

As a developer, you constantly handle sensitive data — API keys, repository tokens, SSH passwords, and configuration secrets. 
Keepr was built to simplify that workflow by letting you **store, search, and retrieve secrets directly from the terminal**, without switching tools or exposing plaintext data.

---

## 📑 Official Docs

Visit the official docs for installation instructions, user guides, deep dives into Keepr's encryption or a full command reference.

👉 [**Full documentation**](https://bsamarji.github.io/Keepr/)

---

## ⚡ Quick Start

Install Keepr from [PyPI](https://pypi.org/project/keepr/):

```bash
pip install keepr

keepr login # Set or unlock the master password

keepr add github # Add a credential

keepr view github # Retrieve entry securely
```

That’s it — your credentials are stored locally, fully encrypted, and accessible only through your master key.

---

## 🧩 Features at a Glance

* 🔒 End-to-End Encryption — AES-256 via SQLCipher and Fernet.
* 🔑 Master Password — Derives a Key Encryption Key (KEK) with PBKDF2-HMAC.
* 🕒 Timed Sessions — Stay logged in for convenience, auto-lock after expiry.
* 🧭 Vault Management — Add, update, list, search, or delete credentials.
* 🧰 Password Generator — Cryptographically secure, configurable length.
* 🧼 Clipboard Copy — Automatically copy passwords to the clipboard when viewing an entry.
* 🎨 Custom Color Scheme — Clear, high-contrast terminal output.
* ⚙️ User configuration — Configure the session length, the terminal output color scheme and password generator settings. 

---

## 📦 Installation

Keepr supports macOS, Linux, and Windows.

Install from PyPI:

```bash
pip install keepr
```

Or download standalone binaries from the [github releases page](https://github.com/bsamarji/Keepr/releases).

For full installation instructions read the [docs guide](https://bsamarji.github.io/Keepr/).

---

## 🛡️ Security at a Glance

Keepr uses a two-key encryption system:
* KEK (Key Encryption Key) — derived from your Master Password
* PEK (Primary Encryption Key) — encrypts the SQLCipher vault
* The PEK is stored only in encrypted form; the KEK is never written to disk.

Read about the full encryption architecture in the [docs](https://bsamarji.github.io/Keepr/encryption/).

---

## 🤝 Contributing

Contributions, ideas, and bug reports are welcome.

Please read the [contributions](CONTRIBUTING.md) page for more details.

Please open an issue before submitting major changes.

---

## 👨‍🔧 Support

If you run into problems, the best way to get help is through the GitHub issue tracker.

- 🐛 **Bug Reports:**  
  Tag the issue with the `bug` label and include steps to reproduce.

- 💡 **Feature Requests:**  
  Use the `enhancement` label and describe what you’d like to see added or improved.

- ❓ **General Questions:**  
  Feel free to open an issue or reach out directly to the maintainers.

---

## 🗺 Roadmap

Planned future features and improvements:

- ⌨️ Shell autocompletion for Keepr commands and arguments.
- 🧪 Password strength checks.
- 🧵 Bulk import/export of entries.
- 🔄 A copy command, which copies a password for an entry to the clipboard, without displaying any info on screen.
- 🧩 A generate command, which just generates a password and displays it on screen (separate to the -g option for the add command).
- 🛡️ Optional Two-factor authentication.
- 💻 TUI (Terminal user interface)

If you want to help shape the roadmap, feel free to open an issue or submit proposals.

---

## 👤 Authors

- **Ben Samarji** — Active Maintainer  
  📧 bensamarji5637@gmail.com

---

## 📜 License

Keepr is offered under the **MIT License**.
See `LICENSE.md` for full details.

You are free to use, modify, and distribute the software as long as the license terms are respected.

---

## 🚀 Project Status

**Active development**

New features, performance improvements, and security enhancements are added regularly. 
Community feedback is always appreciated, and contributions are welcome!
