# SpeakNSave — Voice-Assisted Menu Inventory and Promo Recommendation System

*"Speak it. Find it. Save it."* — a voice-powered web application that helps customers discover menu items and promotions using natural language and voice commands while allowing administrators to efficiently manage inventory.

## Table of Contents

* About the Project
* Features
* Tech Stack
* Getting Started
* Environment Variables
* Usage
* Voice Commands
* CRUD Operations
* Known Limitations
* Future Improvements
* Team

---

## About the Project

SpeakNSave is a Flask-based web application designed to modernize menu browsing and inventory management through voice interaction and intelligent search. The system allows customers to search menu items and promotions using natural language or voice commands while enabling administrators to manage inventory through a dedicated admin panel.

The platform combines speech recognition, menu inventory management, promo discovery, and voice-assisted administration into a single user-friendly system.

Built as a final project for Applications Development and Emerging Technologies at Polytechnic University of the Philippines – Santa Rosa Campus (PUPSRC), Academic Year 2025–2026.

---

## Features

### Customer Features

* Voice-powered menu and promo search
* Natural language search queries
* Budget-based menu recommendations
* Serving size (pax) filtering
* Category-based menu browsing
* Promo discovery and filtering
* Responsive design for desktop and mobile users

### Administrator Features

* Add menu items with image uploads
* Edit menu information directly from the inventory table
* Delete menu items with confirmation modal
* Voice-assisted menu item creation
* Inventory status management
* Promo management
* Menu image management

### Core Features

* Voice command processing using Web Speech API
* Intelligent query interpretation
* Category-based filtering
* Budget-aware menu recommendations
* Serving size recommendation system
* Image upload and preview functionality
* Admin authentication system
* Real-time inventory management

---

## Tech Stack

| Layer             | Technology             |
| ----------------- | ---------------------- |
| Backend           | Flask (Python)         |
| Database          | PostgreSQL             |
| Frontend          | HTML5, CSS, JavaScript |
| Voice Recognition | Web Speech API         |
| Styling           | Custom CSS             |
| Icons             | Font Awesome           |
| Authentication    | Flask Sessions         |
| Image Upload      | Flask File Handling    |
| Deployment        | Railway                |

---

## Getting Started

### Prerequisites

* Python 3.10+
* PostgreSQL
* Git
* Google Chrome or Microsoft Edge (for voice features)

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/SpeakNSave.git
cd SpeakNSave
```

#### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file and follow the Environment Variables section below.

#### 5. Initialize the Database

Import the provided SQL database or run the required schema scripts.

#### 6. Run the Application

```bash
python app.py
```

Visit:

```text
http://127.0.0.1:5000
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
# Flask
SECRET_KEY=your_secret_key

# Database
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=speaknsave

# Optional AI Integration
GEMINI_API_KEY=your_api_key
```

**Important:** Never commit your `.env` file to GitHub.

---

## Usage

### Customer Search Examples

Users can search using text or voice commands.

#### Search by Category

```text
Burgers and drinks
```

#### Search by Budget

```text
Meals under 100 pesos
```

#### Search by Multiple Categories

```text
Platter and desserts
```

#### Search Promos

```text
All promos
```

#### Search by Category and Budget

```text
Desserts under 99 pesos
```

#### Combined Search

```text
Drinks under 50 and burgers above 100
```

#### Advanced Search

```text
Platter under 300 and desserts under 99
```

#### Multi-Category Search

```text
Rice meals and chicken under 200
```

#### Mixed Budget Search

```text
Burgers under 100 and drinks under 50
```

```

---

## Voice Commands

### Customer Commands

| Voice Command | Action |
|--------------|---------|
| "Burgers under 100" | Show burger menu items within a ₱100 budget |
| "Meals under 150 pesos" | Filter meals by budget |
| "Desserts and burgers under 100" | Filter multiple categories within a budget |
| "I want drinks and platters" | Show items from multiple categories |
| "Drinks under 50" | Show drinks within a ₱50 budget |

### Admin Commands

| Voice Command            | Action             |
| ------------------------ | ------------------ |
| "Add cheeseburger"       | Sets menu name     |
| "Price 120"              | Sets item price    |
| "Category burgers"       | Sets category      |
| "Serving size 2"         | Sets serving size  |
| "Promo buy one take one" | Sets promo details |
| "Status active"          | Sets item status   |
| "Add to menu"            | Saves item         |

---

## CRUD Operations

### Create

Administrators can add new menu items through:

* Manual form entry
* Voice-assisted input
* Image upload support

The data is submitted to the backend and stored in the database.

### Read

Menu items are retrieved from the database and displayed in a dynamic inventory table.

Displayed information includes:

* Item Name
* Category
* Serving Size
* Price
* Status
* Promo Details

### Update

Administrators can edit menu records directly within the inventory table.

Editable fields include:

* Name
* Category
* Serving Size
* Price
* Status
* Promo Information

Changes are sent through asynchronous requests and immediately reflected in the system.

### Delete

Items can be removed through a confirmation modal.

After confirmation:

* Record is deleted from the database
* Inventory table refreshes automatically

---

## Known Limitations

* Voice recognition depends on Web Speech API support
* Best performance on Google Chrome and Microsoft Edge
* Requires microphone permission for voice commands
* Background noise may affect recognition accuracy
* Voice recognition language is currently optimized for English
* Inventory updates require an active database connection

---

## Future Improvements

* AI-powered conversational ordering assistant
* Multilingual voice support (Filipino and English)
* Analytics dashboard for sales and inventory trends
* Progressive Web Application (PWA) support
* Real-time inventory notifications
* Automated receipt generation
* Cloud image storage integration
* Stock quantity tracking and alerts
* Full online ordering system integration

---

## Team

Developed by:

* Odessa Jen C. Caratihan
* Maria Angela C. Casacop
* Leonifel C. De Guzman
* Yanina Liro P. Tañala

Polytechnic University of the Philippines – Santa Rosa Campus

Applications Development and Emerging Technologies

Academic Year 2025–2026
