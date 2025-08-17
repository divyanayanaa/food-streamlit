
# Food Sharing — Streamlit App (MySQL)

This app connects to the `food_sharing` MySQL database and provides:
- 15 SQL analyses with filters (city, provider, food type, meal type)
- Provider contact directory
- CRUD for providers, food listings, and claims

## 1) Local Setup

1. Ensure your MySQL DB is ready (run your schema file in Workbench).
2. Create a `.env` file from template:
   ```bash
   cp .env.template .env
   # then edit DB_* values as needed
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run Streamlit:
   ```bash
   streamlit run app.py
   ```

## 2) Deployment (Streamlit Community Cloud)

1. Push these files to a GitHub repo.
2. On https://streamlit.io/cloud, create a new app pointing to your repo.
3. Set the following **secrets** in Streamlit Cloud (Settings → Secrets):
   ```toml
   DB_HOST="your-host"
   DB_PORT="3306"
   DB_USER="your-user"
   DB_PASS="your-password"
   DB_NAME="food_sharing"
   ```
4. Deploy.

Notes:
- The app uses cached reads (`@st.cache_data`) with TTL of 5 minutes.
- Filters apply to many analyses where appropriate.
- CRUD forms run parameterized queries.
