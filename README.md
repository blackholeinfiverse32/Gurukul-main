# 🎓 Gurukul Learning Platform

A comprehensive AI-powered learning platform with authentication, chat interfaces, financial simulation, and personalized learning experiences.

## ✅ Authentication Fixed & Ready to Use!

All Clerk authentication issues have been resolved. The platform is fully functional with multiple login options including a **Demo Mode** for instant testing.

## 🚀 Quick Start (3 Steps)

### 1. Verify Setup
```bash
VERIFY_SETUP.bat
```

### 2. Start Platform
```bash
START_DEMO.bat
```

### 3. Access & Login
- Open: http://localhost:5173
- Click: **"Continue in Demo Mode"**
- ✅ Instant access!

## 🔐 Login Options

### Option 1: Demo Mode ⭐ (Recommended for Testing)
- No setup required
- Instant access
- Full feature access
- Perfect for development

### Option 2: Email/Password
- Create account with email
- Email verification required
- Secure authentication

### Option 3: Google OAuth
- One-click Google sign-in
- Fast and secure
- No password needed

## 📋 Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/)
- **Node.js 20+** - [Download](https://nodejs.org/)

## 🎯 Features

### Authentication & Security
- ✅ Clerk authentication integration
- ✅ Demo mode for testing
- ✅ Google OAuth support
- ✅ Protected routes
- ✅ Session management

### Learning Features
- 📚 Subject selection and management
- 💬 AI-powered chatbot tutor
- 📝 Quiz and assessment system
- 🎥 Video lectures
- 📊 Progress tracking
- 🎯 Personalized learning paths

### Advanced Features
- 💰 Financial simulator
- 🤖 AI agent simulator
- 📈 Forecasting dashboard
- 🎨 Avatar customization
- 🌐 Multi-language support
- 📱 Mobile responsive

## 🛠️ Installation

### First Time Setup

1. **Clone Repository**
```bash
cd Gurukul_new-main
```

2. **Install Backend Dependencies**
```bash
cd Gurukul_new-main\Backend
pip install -r requirements.txt
```

3. **Install Frontend Dependencies**
```bash
cd "..\new frontend"
npm install
```

4. **Verify Setup**
```bash
cd ..\..
VERIFY_SETUP.bat
```

## 🎮 Usage

### Start All Services
```bash
START_DEMO.bat
```

This will:
- ✅ Start backend on port 8000
- ✅ Start frontend on port 5173
- ✅ Open browser automatically

### Manual Start

**Backend:**
```bash
cd Gurukul_new-main\Backend
python main.py
```

**Frontend:**
```bash
cd "Gurukul_new-main\new frontend"
npm run dev
```

## 🌐 Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive API docs |
| Health Check | http://localhost:8000/health | Service status |

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[Authentication Fix](CLERK_AUTH_FIX.md)** - Complete auth setup guide
- **[Demo Credentials](DEMO_CREDENTIALS.md)** - Test accounts and access
- **[Solution Summary](AUTHENTICATION_SOLUTION.md)** - All fixes applied

## 🧪 Testing

### Verify All Services
```bash
test_full_stack.bat
```

### Test Backend Only
```bash
cd Backend
python test_backend.py
```

### Test Frontend
Open http://localhost:5173 and verify:
- ✅ Landing page loads
- ✅ Can navigate to sign-in
- ✅ Demo mode button works
- ✅ Dashboard accessible

## 🔧 Configuration

### Frontend (.env)
```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_aGlwLWdhdG9yLTMxLmNsZXJrLmFjY291bnRzLmRldiQ
VITE_API_BASE_URL=http://localhost:8000
VITE_CHAT_API_BASE_URL=http://localhost:8001
VITE_FINANCIAL_API_BASE_URL=http://localhost:8002
```

### Backend (.env)
```env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check port availability
netstat -ano | findstr :8000

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Won't Start
```bash
# Reinstall dependencies
cd "new frontend"
npm install

# Clear cache
npm cache clean --force
```

### Authentication Issues
**Solution**: Use Demo Mode
1. Go to sign-in page
2. Click "Continue in Demo Mode"
3. Instant access granted

### CORS Errors
1. Check backend .env has ALLOWED_ORIGINS
2. Restart backend server
3. Clear browser cache

## 📊 Project Structure

```
Gurukul_new-main/
├── Backend/                    # Python FastAPI backend
│   ├── main.py                # Main entry point
│   ├── Base_backend/          # Core API
│   ├── memory_management/     # Memory API
│   ├── Financial_simulator/   # Financial features
│   └── ...
├── new frontend/              # React frontend
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable components
│   │   ├── store/            # Redux store
│   │   └── api/              # API integration
│   └── package.json
├── START_DEMO.bat            # Quick start launcher
├── VERIFY_SETUP.bat          # Setup verification
├── test_full_stack.bat       # Service testing
└── Documentation files
```

## 🎯 Key Technologies

### Frontend
- React 18
- Redux Toolkit
- React Router
- Clerk Authentication
- TailwindCSS
- Vite

### Backend
- Python 3.8+
- FastAPI
- MongoDB
- Redis
- Supabase

### AI/ML
- Groq API
- OpenAI API
- Google Gemini
- Local LLM support

## 🔒 Security

- Clerk authentication
- JWT tokens
- CORS protection
- Environment variables
- Secure API endpoints

## 🚀 Deployment

### Development
```bash
START_DEMO.bat
```

### Production
See deployment guides:
- Backend: Render, AWS, Docker
- Frontend: Vercel, Netlify, Firebase

## 📈 Performance

- Lazy loading
- Code splitting
- API caching
- Optimized builds
- CDN ready

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 License

[Your License Here]

## 🆘 Support

### Quick Help
1. Run `VERIFY_SETUP.bat` to check configuration
2. Run `test_full_stack.bat` to test services
3. Check documentation in project root
4. Review browser console for errors

### Common Issues
- **Can't login**: Use Demo Mode
- **CORS errors**: Check backend ALLOWED_ORIGINS
- **Port in use**: Kill process or use different port
- **Dependencies**: Reinstall with npm/pip

## ✨ What's Fixed

- ✅ Clerk authentication fully configured
- ✅ Demo mode implemented
- ✅ CORS properly set up
- ✅ All dependencies installed
- ✅ Environment variables configured
- ✅ Error handling added
- ✅ Documentation complete
- ✅ Test scripts created

## 🎉 Ready to Use!

The platform is fully configured and tested. Start with:

```bash
START_DEMO.bat
```

Then open http://localhost:5173 and click **"Continue in Demo Mode"** for instant access!

---

**Status**: ✅ Fully Functional | **Version**: 1.0.0 | **Last Updated**: 2024

For detailed setup instructions, see [QUICK_START.md](QUICK_START.md)
