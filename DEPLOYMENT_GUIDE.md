# 🚀 Deployment Guide - Weekly Recipe Automation System

## Quick Start - Choose Your Platform

### 🆓 **FREE OPTION: Render**
**Best for**: Personal use, testing, demos
**Time to deploy**: 5 minutes
**Cost**: Free (with limitations)

```bash
1. Fork this repository to your GitHub account
2. Sign up at render.com with GitHub
3. Create new Web Service from your forked repo
4. Set root directory to: backend
5. Deploy automatically!
```
[📖 Detailed Render Guide](deployment_guide_render.md)

### 💰 **RECOMMENDED: Railway**
**Best for**: Production use, no sleep mode
**Time to deploy**: 3 minutes
**Cost**: $5/month

```bash
1. Sign up at railway.app with GitHub
2. Create new project from GitHub repo
3. Set root directory to: backend
4. Deploy with zero configuration!
```
[📖 Detailed Railway Guide](deployment_guide_railway.md)

### 🏢 **ENTERPRISE: DigitalOcean**
**Best for**: Professional applications, scaling
**Time to deploy**: 10 minutes
**Cost**: $5-20/month

```bash
1. Sign up at digitalocean.com
2. Create new App from GitHub repo
3. Add managed PostgreSQL database
4. Configure custom domain
```
[📖 Detailed DigitalOcean Guide](deployment_guide_digitalocean.md)

## Platform Comparison

| Feature | Render (Free) | Railway ($5/mo) | DigitalOcean ($20/mo) |
|---------|---------------|-----------------|----------------------|
| Sleep Mode | Yes (15 min) | No | No |
| Custom Domain | Yes | Yes | Yes |
| Database | SQLite | PostgreSQL | Managed PostgreSQL |
| Auto-Deploy | Yes | Yes | Yes |
| SSL/HTTPS | Yes | Yes | Yes |
| Support | Community | Email | Professional |
| Build Time | 2-5 min | 1-3 min | 3-7 min |

## Pre-Deployment Checklist

### ✅ Repository Setup
- [ ] Code is in GitHub repository
- [ ] `requirements.txt` is in `backend/` directory
- [ ] Flask app listens on `0.0.0.0:5000`
- [ ] CORS is enabled for frontend-backend communication
- [ ] Environment variables are configurable

### ✅ Configuration Files Ready
- [ ] `render.yaml` (for Render deployment)
- [ ] `railway.json` (for Railway deployment)
- [ ] `Dockerfile` (for containerized deployment)
- [ ] `docker-compose.yml` (for local testing)

### ✅ Testing
- [ ] App runs locally with `python src/main.py`
- [ ] Generate Fresh Recipes button works
- [ ] Recipe selection and grocery list generation work
- [ ] All API endpoints respond correctly

## Environment Variables

All platforms need these environment variables:

```bash
FLASK_ENV=production
PYTHONPATH=/app/backend  # Adjust path based on platform
PORT=5000
```

Optional for database upgrade:
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

## Database Options

### SQLite (Default)
- **Pros**: Simple, no setup required, included
- **Cons**: Single file, limited concurrent users
- **Best for**: Personal use, testing

### PostgreSQL (Recommended for Production)
- **Pros**: Robust, scalable, concurrent users
- **Cons**: Additional cost, setup required
- **Best for**: Production, multiple users

## Custom Domain Setup

### 1. Purchase Domain
- Namecheap, GoDaddy, Google Domains, etc.
- Choose something like: `myrecipes.com`

### 2. Configure DNS
Point your domain to your deployment platform:

**Render**: CNAME to `your-app.onrender.com`
**Railway**: CNAME to `your-app.up.railway.app`
**DigitalOcean**: CNAME to `your-app.ondigitalocean.app`

### 3. Add Domain in Platform
- Go to your app settings
- Add custom domain
- SSL certificate is automatically provisioned

## Performance Optimization

### Frontend Optimization
- Static files are served efficiently
- CSS and JS are minified in production
- Images are optimized for web

### Backend Optimization
- Database queries are optimized
- Recipe search results are cached
- API responses are compressed

### Monitoring
- Set up uptime monitoring (UptimeRobot, Pingdom)
- Monitor response times and errors
- Set up alerts for downtime

## Security Best Practices

### HTTPS Only
- All platforms provide automatic HTTPS
- Redirect HTTP to HTTPS
- Use secure cookies in production

### Environment Variables
- Never commit secrets to git
- Use platform environment variable management
- Rotate API keys regularly

### Database Security
- Use strong passwords
- Enable connection encryption
- Regular backups

## Troubleshooting Common Issues

### Build Failures
```bash
# Check these common issues:
1. requirements.txt in correct directory (backend/)
2. Python version compatibility
3. Missing system dependencies
4. Build timeout (increase if needed)
```

### Runtime Errors
```bash
# Check these common issues:
1. Flask app binding to 0.0.0.0:5000
2. Environment variables set correctly
3. Database permissions and connectivity
4. File system permissions for SQLite
```

### Performance Issues
```bash
# Optimization steps:
1. Upgrade to paid plan (removes sleep mode)
2. Add database indexes
3. Enable caching
4. Optimize web recipe search queries
```

## Scaling Considerations

### Traffic Growth
- **Low Traffic** (< 100 users): Free/Basic plans sufficient
- **Medium Traffic** (100-1000 users): Professional plans recommended
- **High Traffic** (1000+ users): Enterprise plans with load balancing

### Feature Expansion
- **User Accounts**: Add authentication system
- **Recipe Sharing**: Social features
- **Mobile App**: API-first architecture ready
- **Analytics**: Usage tracking and insights

## Backup and Recovery

### Database Backups
- **SQLite**: Download database file regularly
- **PostgreSQL**: Automated backups on managed platforms
- **Manual Backups**: Export recipe data as JSON

### Code Backups
- GitHub repository serves as code backup
- Tag releases for easy rollback
- Keep deployment configurations in version control

## Cost Optimization

### Free Tier Usage
- Use Render free tier for personal use
- Monitor build hours usage
- Optimize build times

### Paid Plan Optimization
- Choose right-sized instances
- Monitor resource usage
- Scale down during low usage periods

### Database Costs
- Start with SQLite, upgrade when needed
- Choose appropriate database size
- Monitor storage usage

## Next Steps After Deployment

### 1. Test Everything
- Generate fresh recipes
- Select 4 recipes
- Generate grocery list
- Test on mobile devices

### 2. Share Your App
- Share URL with family/friends
- Get feedback on usability
- Monitor for any issues

### 3. Monitor and Maintain
- Set up uptime monitoring
- Review logs regularly
- Update dependencies periodically

### 4. Enhance Features
- Add user accounts
- Implement recipe ratings
- Add meal planning calendar
- Create shopping list sharing

Your Weekly Recipe Automation System is ready for the world! 🍽️✨

## Support and Resources

- **Documentation**: This repository's docs/ folder
- **Issues**: GitHub Issues for bug reports
- **Community**: GitHub Discussions for questions
- **Updates**: Watch repository for new features

Happy cooking and meal planning! 👨‍🍳

