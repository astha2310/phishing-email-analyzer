"""
Phishing Email Analyzer - live detection
Built by Astha Patel

Usage:
  python3 detect.py                 paste emails one at a time (blank line to quit)
  python3 detect.py "email text"    check one email
  python3 detect.py --real-world    run the real-world check from the README

Run phishing_analyzer.py first to train and save the model.
"""

import os
import sys

import joblib

MODEL_DIR = "models"

if not os.path.exists(os.path.join(MODEL_DIR, "model.pkl")):
    sys.exit("No trained model found. Run `python3 phishing_analyzer.py` first.")

vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.pkl"))
model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))

# Realistic messages from my phishing-awareness experiment (fictional company,
# fictional .example domains). Subject + body, as the model sees them.
REAL_WORLD_CHECK = [
    ("Fake IT password email", "phishing",
     "ACTION REQUIRED: Your password expires today. Your Brightline password expires in 2 hours. "
     "To avoid losing access to email and files, verify your account now. Accounts not verified by "
     "9:00 PM will be locked. http://brightline-it-helpdesk.example/verify"),
    ("Delivery text", "phishing",
     "ParcelGo: ACTION REQUIRED. We attempted to deliver your package today but were unsuccessful. "
     "Please verify your delivery information by Nov 23 at parcelgo-redelivery.example. If not resolved "
     "by the deadline, your package will be returned to the sender."),
    ("Hacked coworker invoice", "phishing",
     "RE: Invoice. Hi, please review the attached invoice and approve it today. The file is "
     "password-protected for security. Password: 1234. Thanks"),
    ("Real IT maintenance notice", "legitimate",
     "Scheduled maintenance: Saturday 10 PM-2 AM. Email and the employee portal will be unavailable "
     "Saturday, Nov 28, from 10 PM to 2 AM ET while we install updates. You don't need to do anything. "
     "Questions? Contact the IT Service Desk through the usual portal or call ext. 4357."),
    ("Real vendor invoice", "legitimate",
     "Your November invoice #INV-20481. Hi Brightline team, your November invoice ($249.00) is ready. "
     "You can view it by signing in to your CloudNest account as usual. No action is needed if you have "
     "auto-pay turned on. Questions? Reply to this email or call the number on your contract."),
]


def analyze_email(text):
    probs = model.predict_proba(vectorizer.transform([text]))[0]
    label = int(probs.argmax())
    return ("PHISHING" if label == 1 else "LEGITIMATE"), probs[label] * 100


def main(args):
    if args and args[0] == "--real-world":
        correct = 0
        for name, truth, text in REAL_WORLD_CHECK:
            verdict, conf = analyze_email(text)
            ok = (verdict == "PHISHING") == (truth == "phishing")
            correct += ok
            print(f"{name:<28} really {truth:<11} model says {verdict:<11} {conf:5.1f}%  {'OK' if ok else 'WRONG'}")
        print(f"\n{correct}/{len(REAL_WORLD_CHECK)} correct on real-world messages")
        return

    if args:
        verdict, conf = analyze_email(" ".join(args))
        print(f"RESULT: {verdict} | CONFIDENCE: {conf:.2f}%")
        return

    print("Paste an email (subject + body on one line) and press Enter. Blank line to quit.")
    while True:
        text = input("\nEmail> ").strip()
        if not text:
            break
        verdict, conf = analyze_email(text)
        print(f"RESULT: {verdict} | CONFIDENCE: {conf:.2f}%")


if __name__ == "__main__":
    main(sys.argv[1:])
