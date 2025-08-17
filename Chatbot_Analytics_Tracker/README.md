# Task 1: Chatbot Analytics Dashboard

This task tracks chatbot usage and visualizes:
- Total queries
- Most common topics
- User ratings

## 📦 How to Use

1. Log data using:
```python
from chat_logger import log_chat
log_chat("user001", "What is diabetes?", "Health", 5)
