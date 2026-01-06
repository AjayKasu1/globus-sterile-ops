# Deployment Guide: Streamlit Cloud

Follow these steps to deploy the **Globus Medical Sterile Operations Suite** to the web for free using Streamlit Cloud. This allows you to share a live link with recruiters.

## 1. Prepare GitHub Repository
1. Create a new **public** repository on GitHub (e.g., `globus-sterile-ops`).
2. Upload all project files:
   - `app.py`
   - `data_processor.py`
   - `pages/` (folder)
   - `requirements.txt`
   - `Dataset/` (folder - *Important: Data must be in repo unless you use S3/DB*)
   - `README.md`
   - *Note: You can exclude `globus_sterile.db` and `reports/` if you want the app to regenerate them, but it's faster to include the `.db` if static.*

## 2. Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Log in with GitHub.
3. Click **"New app"**.
4. Select your repository (`globus-sterile-ops`), branch (`main`), and main file (`app.py`).
5. Click **"Deploy"**.

## 3. Configuration (Optional)
If the app needs to generate the database on startup (because you didn't commit `globus_sterile.db`):
- Add a line to the top of `app.py`:
  ```python
  import os
  if not os.path.exists('globus_sterile.db'):
      import data_processor
      data_processor.main()
  ```
- *However, for this project, I recommend committing the `globus_sterile.db` file directly to GitHub for faster load times.*

## 4. Share the Link
- Copy the URL (e.g., `https://globus-sterile-ops-ajaykasu.streamlit.app`).
- Add this link to your Resume header and Application "Website" field.

---
**Troubleshooting:**
- **Error: File not found**: Ensure the `Dataset/` folder structure in GitHub matches exactly what is in the code.
- **Dependencies**: Ensure `requirements.txt` includes `xlsxwriter`, `plotly`, `openpyxl`.
