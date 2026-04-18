import json
import os

SUBMIT_URL = os.environ.get("SUBMIT_URL", "")


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters") or {}
    token = query_params.get("token", "")
    date = query_params.get("date", "")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Daily Check-In</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      max-width: 700px;
      margin: 40px auto;
      padding: 20px;
      background: #f8fafc;
      color: #0f172a;
    }}
    .card {{
      background: white;
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }}
    h1 {{
      margin-top: 0;
    }}
    label {{
      display: block;
      margin-top: 16px;
      font-weight: bold;
    }}
    textarea, select, input {{
      width: 100%;
      margin-top: 6px;
      padding: 10px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      box-sizing: border-box;
      font-size: 14px;
    }}
    textarea {{
      min-height: 90px;
      resize: vertical;
    }}
    button {{
      margin-top: 20px;
      padding: 12px 18px;
      border: none;
      border-radius: 8px;
      background: #2563eb;
      color: white;
      cursor: pointer;
      font-size: 15px;
    }}
    button:hover {{
      background: #1d4ed8;
    }}
    .success {{
      margin-top: 20px;
      padding: 12px;
      border-radius: 8px;
      background: #dcfce7;
      color: #166534;
    }}
    .error {{
      margin-top: 20px;
      padding: 12px;
      border-radius: 8px;
      background: #fee2e2;
      color: #991b1b;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Daily Check-In</h1>
    <p><strong>Date:</strong> {date}</p>

    <form id="checkinForm">
      <input type="hidden" name="token" value='{token}' />
      <input type="hidden" name="date" value='{date}' />

      <label for="nutrition_score">Nutrition (1-5)</label>
      <select name="nutrition_score" id="nutrition_score" required>
        <option value="">Select a score</option>
        <option value="1">1 - Very Poor</option>
        <option value="2">2</option>
        <option value="3">3 - Okay</option>
        <option value="4">4</option>
        <option value="5">5 - Great</option>
      </select>

      <label for="nutrition_notes">Nutrition Notes</label>
      <textarea name="nutrition_notes" id="nutrition_notes" placeholder="Anything about meals, water, habits, etc."></textarea>

      <label for="finances_score">Finances (1-5)</label>
      <select name="finances_score" id="finances_score" required>
        <option value="">Select a score</option>
        <option value="1">1 - Very Stressful</option>
        <option value="2">2</option>
        <option value="3">3 - Neutral</option>
        <option value="4">4</option>
        <option value="5">5 - Great</option>
      </select>

      <label for="finances_notes">Finance Notes</label>
      <textarea name="finances_notes" id="finances_notes" placeholder="Anything about spending, budgeting, concerns, etc."></textarea>

      <label for="mental_score">Mental Wellbeing (1-5)</label>
      <select name="mental_score" id="mental_score" required>
        <option value="">Select a score</option>
        <option value="1">1 - Very Low</option>
        <option value="2">2</option>
        <option value="3">3 - Okay</option>
        <option value="4">4</option>
        <option value="5">5 - Great</option>
      </select>

      <label for="mental_notes">Mental Wellbeing Notes</label>
      <textarea name="mental_notes" id="mental_notes" placeholder="How are you feeling today?"></textarea>

      <button type="submit">Submit Check-In</button>
    </form>

    <div id="result"></div>
  </div>

  <script>
    const form = document.getElementById("checkinForm");
    const resultDiv = document.getElementById("result");

    form.addEventListener("submit", async (event) => {{
      event.preventDefault();

      const formData = new FormData(form);
      const payload = Object.fromEntries(formData.entries());

      resultDiv.innerHTML = "";

      try {{
        const response = await fetch("{SUBMIT_URL}", {{
          method: "POST",
          headers: {{
            "Content-Type": "application/json"
          }},
          body: JSON.stringify(payload)
        }});

        const data = await response.json();

        if (response.ok) {{
          form.style.display = "none";
          resultDiv.innerHTML = `<div class="success">${{data.message || "Submitted successfully."}}</div>`;
        }} else {{
          resultDiv.innerHTML = `<div class="error">${{data.message || "Submission failed."}}</div>`;
        }}
      }} catch (error) {{
        resultDiv.innerHTML = `<div class="error">Submission failed: ${{error.message}}</div>`;
      }}
    }});
  </script>
</body>
</html>
"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8"
        },
        "body": html
    }