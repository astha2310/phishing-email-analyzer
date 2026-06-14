# Phishing Email Analyzer — ML Email Classification

Built by Astha Patel | M.S. Information Technology, Arizona State University

---

## Why I Built This

Email is still the most common attack vector in cybersecurity. Most phishing classifiers I found online used small curated datasets that do not reflect the real variety of phishing attempts in the wild. I wanted to build something on a large real dataset and understand what actually distinguishes a phishing email from a legitimate one at the text level.

---

## What It Does

The analyzer takes an email's text content and classifies it as phishing or legitimate. It uses TF-IDF vectorization to convert raw email text into numerical features, then applies a Logistic Regression classifier trained on 82,000 plus real emails. A live detection mode lets you paste any email text and get a classification with a confidence score immediately.

---

## The Data

82,486 real emails total. 65,988 used for training and 16,498 used for testing. A mix of verified phishing emails and legitimate emails from public datasets.

82,000 emails is meaningful scale. It means the model has seen enough variation in how phishing emails are written — from urgent bank alerts to password reset scams to prize notifications — that it generalizes well beyond simple keyword matching.

---

## Results

| Metric | Value |
|---|---|
| Accuracy | 98.04% |
| Precision | 0.98 |
| Recall | 0.98 |
| F1 Score | 0.98 |

Consistent precision and recall means the model is not just getting lucky on the majority class. It is genuinely distinguishing phishing from legitimate email.

---

## How It Works

Raw email text is cleaned and lowercased first. TF-IDF vectorization then converts the cleaned text into numerical feature vectors — words that appear frequently in phishing emails but rarely in legitimate ones get high weights, while generic words get low weights. A Logistic Regression classifier uses those vectors to make predictions. The model outputs a probability score, not just a binary label, so a 0.97 phishing probability gets treated differently from a 0.61.

---

## Tech Stack

Python 3, scikit-learn, pandas, NumPy, matplotlib, seaborn

---

## How to Run It

```bash
git clone https://github.com/astha2310/phishing-email-analyzer.git
cd phishing-email-analyzer

pip3 install scikit-learn pandas numpy matplotlib seaborn

python3 phishing_analyzer.py
python3 detect.py
```

---

## What I Learned

The most interesting discovery was how specific the vocabulary of phishing emails is. Words like "verify," "urgent," "suspended," and "click" appear at dramatically higher rates in phishing emails. But the model also picks up subtler signals like unusual capitalization and the absence of personal context you would expect in a real email.

I also learned that recall matters more than precision for a security use case. A missed phishing email is more dangerous than flagging a legitimate one. Tuning the classification threshold to favor recall over precision is the right operational choice here.

---

## What Could Be Added Next

Header analysis covering SPF, DKIM, and DMARC validation to catch spoofed sender domains, URL extraction and scanning within email bodies, real-time Gmail integration to classify incoming emails automatically, and a browser extension that flags suspicious emails in webmail clients.

---

Astha Patel | github.com/astha2310 | linkedin.com/in/asthap23
