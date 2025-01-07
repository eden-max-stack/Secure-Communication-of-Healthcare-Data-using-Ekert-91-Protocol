# Secure Chat Application with File Encryption and Decryption

This project is a secure chat application where users can exchange encrypted messages and files. The backend encrypts the uploaded files and returns both the encrypted and decrypted contents. Users can view encrypted data in the frontend and download the decrypted version.

## Features
- **User Authentication**: Users can switch between different user roles (e.g., Healthcare Center A, Healthcare Center B).
- **File Encryption**: Uploaded files are encrypted using quantum cryptography techniques.
- **File Decryption**: The backend provides decrypted file content for download.
- **Real-Time Chat**: Exchange encrypted text messages in real-time.
- **File Handling**: Encrypted files are processed and saved on the server.

---

## Tech Stack
- **Frontend**: React (with Convex API and Axios)
- **Backend**: Flask (Python)
- **Encryption**: Quantum cryptography-based algorithms (Ekert91 and custom implementations)
- **Storage**: File system handling for encrypted and decrypted files
- **Cross-Origin Support**: Enabled using Flask-CORS

---

## Project Structure

### Frontend (React + Convex)
- **File**: `App.tsx`
  - Handles user interaction, message sending, and file upload.
  - Displays encrypted content in a textarea and provides a download link for decrypted files.

### Backend (Flask)
- **File**: `flask_code.py`
  - Processes incoming messages and files.
  - Encrypts and decrypts file content.
  - Returns JSON responses with encrypted and decrypted content.

### Helper Scripts
- **File**: `handling_files.py`
  - Manages file encryption, decryption, and storage.
  - Saves encrypted data in a folder and logs decrypted content in a separate file.

---

## Installation

### Prerequisites
- Node.js and npm
- Python (3.7+)
- Flask and related dependencies
- Convex SDK

### Setup

#### Backend
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/secure-chat.git
   cd secure-chat
