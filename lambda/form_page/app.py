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
      max-width: 720px;
      margin: 24px auto;
      padding: 14px;
      background: #f8fafc;
      color: #0f172a;
      line-height: 1.5;
    }}
    .card {{
      background: white;
      padding: 24px;
      border-radius: 16px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }}
    h1 {{
      margin-top: 0;
      margin-bottom: 8px;
      font-size: 28px;
    }}
    .subtitle {{
      margin-top: 0;
      margin-bottom: 18px;
      color: #475569;
    }}
    .section {{
      margin-top: 28px;
      padding-top: 18px;
      border-top: 1px solid #e2e8f0;
    }}
    .section h2 {{
      margin: 0 0 8px 0;
      font-size: 20px;
    }}
    .section p {{
      margin-top: 0;
      color: #475569;
      font-size: 14px;
    }}
    label {{
      display: block;
      margin-top: 16px;
      font-weight: bold;
    }}
    textarea, input {{
      width: 100%;
      margin-top: 6px;
      padding: 12px;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      box-sizing: border-box;
      font-size: 16px;
      background: #fff;
    }}
    textarea {{
      min-height: 90px;
      resize: vertical;
    }}
    .scale {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      margin-top: 10px;
    }}
    .scale label {{
      margin-top: 0;
      font-weight: normal;
      text-align: center;
      border: 1px solid #cbd5e1;
      border-radius: 10px;
      padding: 10px 6px;
      cursor: pointer;
      background: #f8fafc;
      transition: 0.15s ease;
      user-select: none;
    }}
    .scale label:hover {{
      border-color: #2563eb;
      background: #eff6ff;
    }}
    .scale input[type="radio"] {{
      display: none;
    }}
    .scale input[type="radio"]:checked + span {{
      font-weight: bold;
      color: #1d4ed8;
    }}
    .helper {{
      font-size: 13px;
      color: #64748b;
      margin-top: 6px;
    }}
    button {{
      margin-top: 24px;
      width: 100%;
      padding: 14px 18px;
      border: none;
      border-radius: 10px;
      background: #2563eb;
      color: white;
      cursor: pointer;
      font-size: 16px;
      font-weight: bold;
    }}
    button:hover {{
      background: #1d4ed8;
    }}
    button:disabled {{
      background: #94a3b8;
      cursor: not-allowed;
    }}
    .success {{
      margin-top: 20px;
      padding: 14px;
      border-radius: 10px;
      background: #dcfce7;
      color: #166534;
    }}
    .error {{
      margin-top: 20px;
      padding: 14px;
      border-radius: 10px;
      background: #fee2e2;
      color: #991b1b;
    }}
    .pill {{
      display: inline-block;
      margin-bottom: 14px;
      padding: 6px 10px;
      border-radius: 999px;
      background: #e0f2fe;
      color: #075985;
      font-size: 13px;
      font-weight: bold;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="pill">Quick daily reflection</div>
    <h1>Daily Check-In</h1>
    <p class="subtitle">A quick snapshot of how today went. This should only take a couple of minutes.</p>
    <p><strong>Date:</strong> {date}</p>

    <form id="checkinForm">
      <input type="hidden" name="token" value='{token}' />
      <input type="hidden" name="date" value='{date}' />

      <div class="section">
        <h2>🍽 Nutrition</h2>
        <p>How did food and hydration go today?</p>

        <label>Nutrition score</label>
        <div class="scale">
          <label>
            <input type="radio" name="nutrition_score" value="1" required>
            <span>😬<br>1</span>
          </label>
          <label>
            <input type="radio" name="nutrition_score" value="2">
            <span>😕<br>2</span>
          </label>
          <label>
            <input type="radio" name="nutrition_score" value="3">
            <span>😐<br>3</span>
          </label>
          <label>
            <input type="radio" name="nutrition_score" value="4">
            <span>🙂<br>4</span>
          </label>
          <label>
            <input type="radio" name="nutrition_score" value="5">
            <span>😄<br>5</span>
          </label>
        </div>
        <div class="helper">1 = rough day, 5 = felt really good</div>

        <label for="nutrition_notes">Nutrition notes</label>
        <textarea name="nutrition_notes" id="nutrition_notes" placeholder="What went well? Meals, snacks, water, cravings, or anything you want to remember."></textarea>

        <label for="sleep_hours">How many hours of sleep did you get?</label>
        <input type="number" id="sleep_hours" name="sleep_hours" step="0.1" min="0" max="24" value="7" required>
      </div>

      <div class="section">
        <h2>💰 Finances</h2>
        <p>A quick check on spending and financial stress.</p>

        <label for="money_spent">How much money did you spend today?</label>
        <input type="number" id="money_spent" name="money_spent" step="0.01" min="0" placeholder="0.00" required>

        <label>Finances score</label>
        <div class="scale">
          <label>
            <input type="radio" name="finances_score" value="1" required>
            <span>😬<br>1</span>
          </label>
          <label>
            <input type="radio" name="finances_score" value="2">
            <span>😕<br>2</span>
          </label>
          <label>
            <input type="radio" name="finances_score" value="3">
            <span>😐<br>3</span>
          </label>
          <label>
            <input type="radio" name="finances_score" value="4">
            <span>🙂<br>4</span>
          </label>
          <label>
            <input type="radio" name="finances_score" value="5">
            <span>😄<br>5</span>
          </label>
        </div>
        <div class="helper">1 = very stressful, 5 = felt in control</div>

        <label for="finances_notes">Finance notes</label>
        <textarea name="finances_notes" id="finances_notes" placeholder="Any spending, wins, concerns, or budgeting notes from today?"></textarea>
      </div>

      <div class="section">
        <h2>🧠 Mental wellbeing</h2>
        <p>How are you doing emotionally and mentally today?</p>

        <label>Mental wellbeing score</label>
        <div class="scale">
          <label>
            <input type="radio" name="mental_score" value="1" required>
            <span>😬<br>1</span>
          </label>
          <label>
            <input type="radio" name="mental_score" value="2">
            <span>😕<br>2</span>
          </label>
          <label>
            <input type="radio" name="mental_score" value="3">
            <span>😐<br>3</span>
          </label>
          <label>
            <input type="radio" name="mental_score" value="4">
            <span>🙂<br>4</span>
          </label>
          <label>
            <input type="radio" name="mental_score" value="5">
            <span>😄<br>5</span>
          </label>
        </div>
        <div class="helper">1 = low, 5 = strong/good day</div>

        <label for="mental_notes">Mental wellbeing notes</label>
        <textarea name="mental_notes" id="mental_notes" placeholder="What’s been on your mind today? Anything stressful, encouraging, or worth noting?"></textarea>
      </div>

      <button type="submit" id="submitButton">Submit Check-In</button>
    </form>

    <div id="result"></div>
  </div>

  <script>
    const form = document.getElementById("checkinForm");
    const resultDiv = document.getElementById("result");
    const submitButton = document.getElementById("submitButton");

    form.addEventListener("submit", async (event) => {{
      event.preventDefault();

      const payload = {{
        token: form.elements["token"].value,
        date: form.elements["date"].value,
        nutrition_score: Number(form.querySelector('input[name="nutrition_score"]:checked')?.value),
        nutrition_notes: form.elements["nutrition_notes"].value.trim(),
        sleep_hours: Number(form.elements["sleep_hours"].value),
        money_spent: Number(form.elements["money_spent"].value),
        finances_score: Number(form.querySelector('input[name="finances_score"]:checked')?.value),
        finances_notes: form.elements["finances_notes"].value.trim(),
        mental_score: Number(form.querySelector('input[name="mental_score"]:checked')?.value),
        mental_notes: form.elements["mental_notes"].value.trim()
      }};

      resultDiv.innerHTML = "";

      if (!payload.nutrition_score || !payload.finances_score || !payload.mental_score) {{
        resultDiv.innerHTML = `<div class="error">Please choose a score for each section.</div>`;
        return;
      }}

      if (payload.sleep_hours < 0 || payload.sleep_hours > 24) {{
        resultDiv.innerHTML = `<div class="error">Sleep hours must be between 0 and 24.</div>`;
        return;
      }}

      if (payload.money_spent < 0) {{
        resultDiv.innerHTML = `<div class="error">Money spent cannot be negative.</div>`;
        return;
      }}

      if (!confirm("Submit your check-in for today?")) {{
        return;
      }}

      submitButton.disabled = true;
      submitButton.textContent = "Submitting...";

      try {{
        const response = await fetch("{SUBMIT_URL}", {{
          method: "POST",
          headers: {{
            "Content-Type": "application/json"
          }},
          body: JSON.stringify(payload)
        }});

        const text = await response.text();
        let data = {{}};

        try {{
          data = JSON.parse(text);
        }} catch (e) {{
          throw new Error(text || "Invalid server response");
        }}

        if (response.ok) {{
          form.style.display = "none";
          resultDiv.innerHTML = `
            <div class="success">
              ✅ Check-in complete!
              <br><br>
              Great job staying consistent today.
            </div>
          `;
        }} else {{
          resultDiv.innerHTML = `<div class="error">${{data.message || data.error || "Submission failed."}}</div>`;
          submitButton.disabled = false;
          submitButton.textContent = "Submit Check-In";
        }}
      }} catch (error) {{
        resultDiv.innerHTML = `<div class="error">Submission failed: ${{error.message}}</div>`;
        submitButton.disabled = false;
        submitButton.textContent = "Submit Check-In";
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