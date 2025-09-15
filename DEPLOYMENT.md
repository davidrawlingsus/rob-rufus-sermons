# 🚀 Railway Deployment Guide

This guide will help you deploy the Rob Rufus Sermon Directory to Railway with a PostgreSQL database.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Push your code to GitHub
3. **Sermon Data**: Ensure you have `sermon_metadata.json` from running the scraper

## Step 1: Prepare Your Repository

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Flask web app for Railway deployment"
   git push origin main
   ```

2. **Verify Files**: Ensure these files are in your repository:
   - `app.py` - Flask application
   - `requirements.txt` - Python dependencies
   - `railway.toml` - Railway configuration
   - `Procfile` - Process configuration
   - `migrate_db.py` - Database migration script
   - `templates/` - HTML templates
   - `static/` - CSS and JavaScript files

## Step 2: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)

1. **Go to Railway**: Visit [railway.app](https://railway.app) and sign in
2. **New Project**: Click "New Project"
3. **Deploy from GitHub**: Select "Deploy from GitHub repo"
4. **Select Repository**: Choose your Rob Rufus Sermons repository
5. **Deploy**: Railway will automatically detect the Python app and deploy

### Option B: Deploy with Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize Project**:
   ```bash
   railway init
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

## Step 3: Set Up Database

1. **Add PostgreSQL**: In your Railway project dashboard:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically create a PostgreSQL database

2. **Get Database URL**: 
   - Go to your PostgreSQL service
   - Copy the `DATABASE_URL` from the Variables tab
   - This will be automatically set as an environment variable

## Step 4: Migrate Data

1. **Run Migration Locally** (before deployment):
   ```bash
   # Set the DATABASE_URL environment variable
   export DATABASE_URL="your_postgresql_url_here"
   
   # Run the migration
   python migrate_db.py
   ```

2. **Or Run Migration on Railway**:
   - Go to your Railway project
   - Open the terminal/console
   - Run: `python migrate_db.py`

## Step 5: Configure Environment Variables

In your Railway project dashboard, set these environment variables:

- `DATABASE_URL` - Automatically set by Railway PostgreSQL
- `FLASK_ENV` - Set to `production`
- `PORT` - Automatically set by Railway

## Step 6: Test Your Deployment

1. **Check Health**: Visit `https://your-app.railway.app/health`
2. **Test API**: Visit `https://your-app.railway.app/api/stats`
3. **View App**: Visit `https://your-app.railway.app/`

## Step 7: Custom Domain (Optional)

1. **Add Domain**: In Railway dashboard, go to Settings → Domains
2. **Add Custom Domain**: Enter your domain name
3. **Configure DNS**: Point your domain to Railway's servers

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Verify `DATABASE_URL` is set correctly
   - Check that PostgreSQL service is running
   - Ensure database tables are created

2. **Build Failures**:
   - Check `requirements.txt` for correct dependencies
   - Verify Python version compatibility
   - Check build logs in Railway dashboard

3. **App Not Loading**:
   - Check application logs in Railway dashboard
   - Verify `PORT` environment variable is set
   - Ensure `gunicorn` is in requirements.txt

### Useful Commands

```bash
# Check database stats
python migrate_db.py --stats

# View logs
railway logs

# Connect to database
railway connect

# Restart service
railway restart
```

## Performance Optimization

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Caching**: Implement Redis caching for better performance
3. **CDN**: Use Railway's CDN for static assets
4. **Monitoring**: Set up monitoring and alerts

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to Git
2. **Database Access**: Use connection pooling for production
3. **HTTPS**: Railway provides HTTPS by default
4. **Rate Limiting**: Consider implementing rate limiting for API endpoints

## Scaling

Railway automatically handles:
- **Horizontal Scaling**: Multiple instances based on traffic
- **Database Scaling**: PostgreSQL scaling options
- **Load Balancing**: Automatic load balancing
- **Health Checks**: Automatic health monitoring

## Cost Optimization

1. **Resource Limits**: Set appropriate CPU/memory limits
2. **Database Size**: Monitor database usage
3. **Traffic**: Monitor bandwidth usage
4. **Sleep Mode**: Configure sleep settings for development

## Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Community**: [Railway Discord](https://discord.gg/railway)
- **GitHub Issues**: Create issues in your repository

---

🎉 **Congratulations!** Your Rob Rufus Sermon Directory is now live on Railway with a scalable PostgreSQL database!
