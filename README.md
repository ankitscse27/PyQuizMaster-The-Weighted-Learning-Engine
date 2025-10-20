# 🧠 PyQuizMaster: The Weighted Learning Engine

**A dual-platform (Desktop & Web) diagnostic quiz system designed for serious learners and intellectual performance tracking.**

PyQuizMaster moves beyond standard testing by implementing a powerful **Weighted Scoring Engine**, where question difficulty directly impacts point value (e.g., CS questions are worth more than GK), providing a true measure of specialized knowledge.

---

## ✨ Key Differentiators & Features

| Feature Category | Desktop Edition (Python/customtkinter) | Web Edition (HTML/JS/Tailwind CSS) | **Strategic Value** |
| :--- | :--- | :--- | :--- |
| **Scoring Engine** | **Weighted Scoring** based on category/difficulty. | **Weighted Scoring** (1, 2, or 3 points) based on category. | Provides a **diagnostic, weighted score** over a simple count of correct answers. |
| **UI/UX** | Desktop-grade UI with `customtkinter`. Fully responsive and compiled for a native feel. | Clean, **responsive design** using **Tailwind CSS**. Looks great on all devices (desktop/mobile). | Ensures an optimal learning experience regardless of the user's platform. |
| **Tracking** | **Persistent History** tracks and saves your last **10 sessions** locally. | **Local Storage History** saves up to the last **10 results** in the browser. | Allows users to track performance trends and identify knowledge gaps over time. |
| **Workflow** | **Rapid Hotkeys** (1-4, Enter) for instant answer selection and navigation. | **Hotkeys** (1-4, Enter) for highly efficient, keyboard-driven quizzes. | Maximizes focus and minimizes time spent on navigation. |
| **Post-Quiz Analysis** | Comprehensive post-quiz analysis and **mistake breakdown**. | Detailed **Mistakes Review** and a **Category Breakdown** of performance. | Facilitates targeted study by clearly isolating areas requiring improvement. |
| **Configuration** | Dedicated **Settings Window** for question count and category filtering (GK, Science, CS). | **Custom Quiz Configuration** via an intuitive slider and category checkboxes. | Enables highly personalized and focused study sessions. |

---

## 🛠️ Technical Stack

| Component | Desktop Edition | Web Edition |
| :--- | :--- | :--- |
| **Core Language** | **Python 3.8+** | **HTML5, JavaScript (Zero Dependencies)** |
| **UI Framework** | `customtkinter` (for modern desktop UI) | **Tailwind CSS** (via CDN for utility-first styling) |
| **Workflow** | Object-Oriented Programming (OOP) | Single-file application architecture |
| **Dependencies** | `pip install customtkinter` | None (relies on unpkg CDN links) |

---

## 🚀 Setup & Execution

### 💻 Desktop Edition (`QUIZ APP.py`)

1.  **Prerequisite:** Ensure Python 3.8+ is installed.
2.  **Install UI Library:**
    ```bash
    pip install customtkinter
    ```
3.  **Run:** Execute the main application file.
    ```bash
    python "QUIZ APP.py"
    ```

### 🌐 Web Edition (`index.html`)

1.  **Setup:** Copy the entire code block and save it as an **`index.html`** file.
2.  **Run:** Simply double-click the saved file to open it in any modern web browser.

---

## 🕹️ Usage Workflow

1.  **Configure:** Use the initial settings screen to select your desired **Number of Questions** and target **Categories** (GK, Science, CS).
2.  **Quiz:** Take the quiz using either clicks or **Hotkeys (1, 2, 3, 4, Enter)**. Utilize the **Review** feature to jump between questions.
3.  **Analyze:** Upon submitting, view the **Results Screen** showing your Weighted Score, Category Breakdown, and the historical record of your last 10 sessions.

---

## ⚖️ License & Author

This project is open-sourced under the **MIT License**.

**Creator:** [@ankitscse27](https://github.com/ankitscse27)
