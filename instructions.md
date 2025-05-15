# Deploying Genre ELO Rating App to Heroku

## Prerequisites
- A GitHub account
- A Heroku account (Sign up at https://signup.heroku.com/ if you don't have one)

## Deployment Instructions

### Step 1: Push Your Code to GitHub
1. Create a new repository on GitHub
2. Push your local repository to GitHub using these commands:
   ```
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

### Step 2: Deploy to Heroku via GitHub
1. Go to [Heroku Dashboard](https://dashboard.heroku.com/)
2. Click "New" → "Create new app"
3. Choose a unique app name and select your region
4. Click "Create app"

### Step 3: Connect to GitHub
1. In your Heroku app dashboard, go to the "Deploy" tab
2. In the "Deployment method" section, select "GitHub"
3. Click "Connect to GitHub"
4. Search for your repository name
5. Click "Connect" next to your repository

### Step 4: Configure Deployment
1. Scroll down to the "Manual deploy" section
2. Choose the branch you want to deploy (usually 'main')
3. Click "Deploy Branch"
   - Alternatively, you can enable "Automatic Deploys" to deploy automatically when you push to GitHub

### Step 5: Verify Deployment
1. Wait for the build to complete
2. Once done, click "View" to see your live application

## Important Notes
- Your app already has the required files for Heroku deployment:
  - `Procfile` with the command `web: gunicorn main:app`
  - `requirements.txt` with all necessary dependencies
- The application is configured to use environment variables for any sensitive data

## Troubleshooting
If you encounter any issues:
1. Check the Heroku logs in your app dashboard under "More" → "View logs"
2. Ensure all dependencies are listed in `requirements.txt`
3. Verify that the `Procfile` is in the root directory
4. Make sure your app is properly configured for production use

## Monitoring Your App
- You can monitor your app's performance and logs through the Heroku Dashboard
- To view logs, go to "More" → "View logs" in your app's dashboard