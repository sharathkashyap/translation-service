<details>
<summary>Local Installation for using GPU</summary>

# Step 1: Install
pip install -r requirements/dev.txt

# Step 2: Configure (uses Local GPU by default)
cp .env.example .env

# Step 3: Run
uvicorn src.main:app --reload

# Visit: http://localhost:8000/docs
```

---

## 📋 **Project Structure**

translation-service/
├── src/
│   ├── core/                    # Configuration & exceptions
│   │   ├── config.py           # Settings (SWITCH ENGINE HERE!)
│   │   ├── enums.py            # Language codes
│   │   └── exceptions.py       # Custom errors
│   │
│   ├── integrations/            # Translation engines
│   │   ├── base.py             # Abstract interface
│   │   ├── google_translate.py  # Google provider
│   │   ├── openai_translate.py  # OpenAI provider
│   │   ├── local_translate.py   # Local GPU provider
│   │   └── factory.py           # Engine factory
│   │
│   ├── translation/             # API layer
│   │   ├── router.py           # Endpoints
│   │   ├── service.py          # Business logic
│   │   └── schemas.py          # Data models
│   │
│   └── main.py                  # FastAPI app
│
├── tests/                       # Test suite
├── requirements/                # Dependencies (base, dev, prod)
├── .env.example                # Configuration template
├── logging.ini                 # Logging setup
├── README.md                   # Full documentation
└── SETUP.md                    # Quick setup guide
```
</details>


<details>
<summary>Local Installation using Google API</summary>

═══════════════════════════════════════════════════════════════════════════════
🌍 TRANSLATION SERVICE WITH GOOGLE CLOUD TRANSLATE - SETUP STEPS
═══════════════════════════════════════════════════════════════════════════════

✨ WHAT YOU'LL HAVE AT THE END:
  ✅ Translation API running with Google Cloud Translate
  ✅ Supports 100+ languages
  ✅ Production-ready service
  ✅ API at http://localhost:8000/docs

═══════════════════════════════════════════════════════════════════════════════

📋 PART 1: GOOGLE CLOUD SETUP (15 minutes)
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Create Google Cloud Project
─────────────────────────────────────

1. Go to: https://console.cloud.google.com
2. Click the dropdown at the top (next to "Google Cloud")
3. Click "NEW PROJECT"
4. Enter project name: "translation-service"
5. Click "CREATE"
6. Wait for project to be created (1-2 minutes)
7. The new project will be automatically selected

What you'll see: "Project ID: xyz-123-456" at the top


STEP 2: Enable Cloud Translation API
─────────────────────────────────────

1. In Google Cloud Console, click the menu ☰ (top left)
2. Go to: "APIs & Services" → "Library"
3. In search box, type: "Cloud Translation"
4. Click on "Cloud Translation API"
5. Click the blue "ENABLE" button
6. Wait for it to enable (takes about 1 minute)

You should see: "Status: ENABLED"


STEP 3: Create Service Account
────────────────────────────────

1. In Google Cloud Console, go to: "APIs & Services" → "Credentials"
2. Click "CREATE CREDENTIALS" (blue button)
3. Select "Service Account" from dropdown
4. Fill in the form:
   - Service account name: "oan-translation-service"
   - Description: "Service account for translation API"
5. Click "CREATE AND CONTINUE"
6. On the next page, click "SELECT A ROLE"
7. Search for and select: "Cloud Translation API User"
8. Click "CONTINUE"
9. Click "DONE"

Result: Service account created


STEP 4: Generate JSON Credentials
──────────────────────────────────

1. In "APIs & Services" → "Credentials"
2. Under "Service Accounts", click on "oan-translation-service"
3. Click the "KEYS" tab
4. Click "ADD KEY" (blue button)
5. Select "Create new key"
6. Select "JSON" (should be default)
7. Click "CREATE"
8. A JSON file will automatically download

⚠️  IMPORTANT: Save this file in a safe location!


STEP 5: Get Your Project ID
───────────────────────────

You need the Project ID for configuration.

Option A (Easy):
  1. Look at top of Google Cloud Console
  2. You'll see: "Project ID: xyz-123-456"
  3. Copy the ID (xyz-123-456)

Option B (From JSON file):
  1. Open the downloaded JSON file
  2. Find the line: "project_id": "xyz-123-456"
  3. Copy the value: xyz-123-456

📝 Save your Project ID somewhere!

═══════════════════════════════════════════════════════════════════════════════

📋 PART 2: LOCAL SETUP (10 minutes)
═══════════════════════════════════════════════════════════════════════════════

STEP 6: Extract Translation Service
────────────────────────────────────

On your computer, open terminal/command prompt:

Mac/Linux:
  cd oan-translation-service

Windows (using PowerShell):
  # Extract the zip file first, then:
  cd oan-translation-service


STEP 7: Copy Google Credentials
───────────────────────────────

1. Take the JSON file you downloaded (google-credentials.json)
2. Copy it to the translation-service folder

Result: Your folder should contain:
  translation-service/
  ├── google-credentials.json    ← Your credentials file
  ├── src/
  ├── tests/
  └── ...


STEP 8: Create Python Virtual Environment
──────────────────────────────────────────

In the translation-service folder, run:

Mac/Linux:
  python3 -m venv venv
  source venv/bin/activate

Windows (Command Prompt):
  python -m venv venv
  venv\Scripts\activate

Windows (PowerShell):
  python -m venv venv
  venv\Scripts\Activate.ps1

You should see (venv) at the start of your command prompt


STEP 9: Install Dependencies
──────────────────────────────

In the activated virtual environment, run:

  pip install -r requirements/dev.txt

Wait for installation to complete (takes 2-3 minutes)


STEP 10: Configure Environment Variables
─────────────────────────────────────────

1. Make a copy of the template:

   Mac/Linux:
     cp .env.example .env

   Windows:
     copy .env.example .env

2. Open the .env file in a text editor

3. Find and replace these lines:

   BEFORE:
   ───────
   # Translation Engine Configuration
   TRANSLATION_ENGINE=local
   GOOGLE_PROJECT_ID=""
   GOOGLE_CREDENTIALS_PATH=""

   AFTER:
   ──────
   # Translation Engine Configuration
   TRANSLATION_ENGINE="google"
   GOOGLE_PROJECT_ID="YOUR_PROJECT_ID"
   GOOGLE_CREDENTIALS_PATH="./google-credentials.json"

   💡 Replace "YOUR_PROJECT_ID" with your actual project ID!
      Example: GOOGLE_PROJECT_ID="my-translation-project-123456"

4. Save the .env file


STEP 11: Verify File Structure
───────────────────────────────

Your translation-service folder should now have:

  translation-service/
  ├── google-credentials.json    ← Downloaded from GCP
  ├── .env                       ← Configuration
  ├── src/
  │   ├── main.py
  │   ├── core/
  │   ├── integrations/
  │   └── translation/
  ├── tests/
  ├── requirements/
  └── README.md

═══════════════════════════════════════════════════════════════════════════════

🚀 PART 3: RUN THE SERVICE (5 minutes)
═══════════════════════════════════════════════════════════════════════════════

STEP 12: Start the Application
───────────────────────────────

Make sure:
  1. You're in the translation-service folder
  2. Virtual environment is activated (you see (venv) in prompt)

Run:
  uvicorn src.main:app --reload

You should see output like:
  ✅ INFO:     Uvicorn running on http://127.0.0.1:8000
  ✅ INFO:     Application startup complete
  ✅ INFO:     Translation engine: google


STEP 13: Test the Service
──────────────────────────

Option A: Use Browser UI (Easiest)
  1. Open: http://localhost:8000/docs
  2. Click "POST /api/translate/"
  3. Click "Try it out"
  4. Enter:
     {
       "text": "Hello world",
       "source_language": "en",
       "target_language": "es"
     }
  5. Click "Execute"
  6. You should get: "Hola mundo"

Option B: Use cURL
  
  In another terminal window:
  
  curl -X POST http://localhost:8000/api/translate/ \
    -H "Content-Type: application/json" \
    -d '{"text":"Hello","source_language":"en","target_language":"es"}'
  
  Response should include: "translated_text": "Hola"

Option C: Check Health
  
  curl http://localhost:8000/api/translate/health
  
  Response should include: "healthy": true


STEP 14: Verify It's Working
──────────────────────────────

Look for these signs of success:

Console output:
  ✅ "Translation engine: google" or similar
  ✅ No error messages about credentials

API response:
  ✅ HTTP 200 OK status
  ✅ "translated_text" contains actual translation
  ✅ "engine": "GoogleTranslateProvider"

Health check:
  ✅ "healthy": true
  ✅ "engine": "GoogleTranslateProvider"

═══════════════════════════════════════════════════════════════════════════════

✅ YOU'RE DONE!
═══════════════════════════════════════════════════════════════════════════════

Your Translation Service is now running with Google Cloud Translate!

📊 WHAT YOU CAN DO NOW:

1. Translate single text:
   POST /api/translate/
   
2. Batch translate multiple texts:
   POST /api/translate/batch
   
3. Get supported languages:
   GET /api/translate/languages
   
4. Check service health:
   GET /api/translate/health

5. View API documentation:
   Visit: http://localhost:8000/docs


💰 IMPORTANT: Google Cloud Pricing
──────────────────────────────────

First 500,000 characters per month: FREE
After that: $16 per million characters

Monitor usage: Google Cloud Console → Billing → Reports


🆘 IF SOMETHING GOES WRONG
──────────────────────────

See: GCP_QUICK_REFERENCE.txt or GCP_SETUP_GUIDE.md

Common issues:
  • "Credentials not found" → Check google-credentials.json location
  • "Permission denied" → Check API is enabled and role is assigned
  • "Invalid project ID" → Verify GOOGLE_PROJECT_ID in .env


📚 NEXT STEPS
─────────────

1. Test more translations
2. Monitor API usage in GCP Console
3. Deploy to production (see README.md for Docker setup)
4. Integrate with your application


🎉 HAPPY TRANSLATING!
═══════════════════════════════════════════════════════════════════════════════

Your translation service supports 100+ languages via Google Cloud Translate!

API running at: http://localhost:8000/docs

</details>
