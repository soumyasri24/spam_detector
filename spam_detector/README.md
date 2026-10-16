# Spam Message Detector

A minimal, beginner-friendly Streamlit app that:

- Checks a pasted message and labels it **Spam** or **Not Spam** using simple rules
  (links, password/payment requests, urgency, prize claims).
- Keeps a small **Spam Call Log** where you can report numbers and mark them as blocked.

No external APIs or accounts are needed. The app never opens or follows links.

## Setup

1. Install Python 3.9 or newer.
2. (Optional) create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run

```
streamlit run app.py
```

Your browser will open the app (usually at http://localhost:8501).

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit interface |
| `detector.py` | Rule-based message checker (edit `RULES` to tune it) |
| `storage.py` | Phone number validation and JSON storage |
| `spam_numbers.json` | Created automatically when you report a number |

## Important notes

- **Results can be incorrect.** This is a warning aid, not a guarantee.
  Avoid sharing sensitive information with suspicious senders.
- **"Block" is local only.** It records the number as blocked in
  `spam_numbers.json`. It does not block calls through your phone carrier or
  operating system. Use your phone's built-in blocking features for that.
